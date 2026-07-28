import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getFolders } from "../../api/folders";
import { createNote, deleteNote, getNote, getNotes, updateNote } from "../../api/notes";
import { askQuestion, generateSummary, generateTags } from "../../api/ai";
import useAuth from "../../hooks/useAuth";
import { removeTokens } from "../../utils/token";
import "./Notes.css";

const emptyDraft = {
    title: "",
    content: "",
    folder_uid: null,
};

function getErrorMessage(error) {
    const detail = error.response?.data?.detail;
    return typeof detail === "string" ? detail : "Something went wrong. Please try again.";
}

function formatUpdatedAt(dateString) {
    if (!dateString) return "";
    return new Intl.DateTimeFormat(undefined, {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
    }).format(new Date(dateString));
}

function Notes() {
    const navigate = useNavigate();
    const { setUser } = useAuth();
    const [folders, setFolders] = useState([]);
    const [notes, setNotes] = useState([]);
    const [selectedFolderId, setSelectedFolderId] = useState(null);
    const [selectedNote, setSelectedNote] = useState(null);
    const [draft, setDraft] = useState(emptyDraft);
    const [foldersLoading, setFoldersLoading] = useState(true);
    const [notesLoading, setNotesLoading] = useState(true);
    const [noteLoading, setNoteLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [summaryGenerating, setSummaryGenerating] = useState(false);
    const [tagsGenerating, setTagsGenerating] = useState(false);
    const [question, setQuestion] = useState("");
    const [questionLoading, setQuestionLoading] = useState(false);
    const [conversationsByNote, setConversationsByNote] = useState({});
    const [reloadKey, setReloadKey] = useState(0);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const latestConversationRef = useRef(null);

    const conversation = selectedNote
        ? conversationsByNote[selectedNote.uid] || []
        : [];

    const signOut = useCallback(() => {
        removeTokens();
        setUser(null);
        navigate("/login", { replace: true });
    }, [navigate, setUser]);

    function refreshNotes() {
        setNotesLoading(true);
        setReloadKey((current) => current + 1);
    }

    function selectFolder(folderId) {
        setSelectedFolderId(folderId);
        setSelectedNote(null);
        setDraft(emptyDraft);
        setNotesLoading(true);
        setError("");
    }

    useEffect(() => {
        let isCurrent = true;

        getFolders()
            .then((response) => {
                if (isCurrent) setFolders(response.data);
            })
            .catch((requestError) => {
                if (!isCurrent) return;
                if ([401, 403].includes(requestError.response?.status)) {
                    signOut();
                    return;
                }
                setError(getErrorMessage(requestError));
            })
            .finally(() => {
                if (isCurrent) setFoldersLoading(false);
            });

        return () => {
            isCurrent = false;
        };
    }, [signOut]);

    useEffect(() => {
        let isCurrent = true;

        getNotes(selectedFolderId)
            .then((response) => {
                if (!isCurrent) return;
                const sortedNotes = [...response.data].sort((first, second) =>
                    Number(second.is_pinned) - Number(first.is_pinned)
                );
                setNotes(sortedNotes);
            })
            .catch((requestError) => {
                if (!isCurrent) return;
                if ([401, 403].includes(requestError.response?.status)) {
                    signOut();
                    return;
                }
                setError(getErrorMessage(requestError));
            })
            .finally(() => {
                if (isCurrent) setNotesLoading(false);
            });

        return () => {
            isCurrent = false;
        };
    }, [reloadKey, selectedFolderId, signOut]);

    useEffect(() => {
        if (conversation.length > 0) {
            latestConversationRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
    }, [conversation.length, selectedNote?.uid]);

    async function handleSelectNote(noteId) {
        setNoteLoading(true);
        setError("");
        try {
            const response = await getNote(noteId);
            setSelectedNote(response.data);
            setDraft({
                title: response.data.title,
                content: response.data.content,
                folder_uid: response.data.folder_uid,
            });
        } catch (requestError) {
            if ([401, 403].includes(requestError.response?.status)) {
                signOut();
                return;
            }
            setError(getErrorMessage(requestError));
        } finally {
            setNoteLoading(false);
        }
    }

    async function handleNewNote() {
        setSaving(true);
        setError("");
        setMessage("");
        try {
            const response = await createNote({
                title: "Untitled note",
                content: "",
                folder_uid: selectedFolderId,
            });
            setSelectedNote(response.data);
            setDraft({
                title: response.data.title,
                content: response.data.content,
                folder_uid: response.data.folder_uid,
            });
            setMessage("New note created.");
            refreshNotes();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    function handleDraftChange(event) {
        setDraft((current) => ({ ...current, [event.target.name]: event.target.value }));
    }

    async function saveChanges() {
        if (!selectedNote) return;

        const changes = {};
        if (draft.title !== selectedNote.title) changes.title = draft.title;
        if (draft.content !== selectedNote.content) changes.content = draft.content;
        if (Object.keys(changes).length === 0) {
            setMessage("No changes to save.");
            return;
        }

        setSaving(true);
        setError("");
        setMessage("");
        try {
            const response = await updateNote(selectedNote.uid, changes);
            setSelectedNote(response.data);
            setDraft({
                title: response.data.title,
                content: response.data.content,
                folder_uid: response.data.folder_uid,
            });
            setMessage("Saved.");
            refreshNotes();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    async function handleFolderMove(event) {
        if (!selectedNote) return;

        const folderUid = event.target.value || null;
        if (folderUid === selectedNote.folder_uid) return;

        setSaving(true);
        setError("");
        setMessage("");
        try {
            const response = await updateNote(selectedNote.uid, { folder_uid: folderUid });
            setSelectedNote(response.data);
            setDraft((current) => ({ ...current, folder_uid: response.data.folder_uid }));
            setMessage("Folder updated.");
            refreshNotes();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    async function togglePin() {
        if (!selectedNote) return;

        setSaving(true);
        setError("");
        try {
            const response = await updateNote(selectedNote.uid, { is_pinned: !selectedNote.is_pinned });
            setSelectedNote(response.data);
            setMessage(response.data.is_pinned ? "Note pinned." : "Note unpinned.");
            refreshNotes();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    async function archiveNote() {
        if (!selectedNote) return;

        setSaving(true);
        setError("");
        try {
            await updateNote(selectedNote.uid, { is_archived: true });
            setSelectedNote(null);
            setDraft(emptyDraft);
            setMessage("Note archived.");
            refreshNotes();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    async function removeNote() {
        if (!selectedNote || !window.confirm("Delete this note? This cannot be undone.")) return;

        setSaving(true);
        setError("");
        try {
            await deleteNote(selectedNote.uid);
            setSelectedNote(null);
            setDraft(emptyDraft);
            setMessage("Note deleted.");
            refreshNotes();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    async function handleGenerateSummary() {
        if (!selectedNote) return;

        setSummaryGenerating(true);
        setError("");
        setMessage("");
        try {
            const response = await generateSummary(selectedNote.uid);
            setSelectedNote((current) => ({ ...current, summary: response.data.summary }));
            setMessage("AI summary ready.");
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSummaryGenerating(false);
        }
    }

    async function handleGenerateTags() {
        if (!selectedNote) return;

        setTagsGenerating(true);
        setError("");
        setMessage("");
        try {
            const response = await generateTags(selectedNote.uid);
            setSelectedNote((current) => ({ ...current, tags: response.data.tags }));
            setMessage("AI tags ready.");
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setTagsGenerating(false);
        }
    }

    async function handleAskQuestion(event) {
        event.preventDefault();
        const trimmedQuestion = question.trim();
        if (!selectedNote || !trimmedQuestion) {
            setError("Enter a question before asking AI.");
            return;
        }

        const noteId = selectedNote.uid;
        setQuestionLoading(true);
        setError("");
        setMessage("");
        try {
            const response = await askQuestion(noteId, trimmedQuestion);
            setConversationsByNote((current) => ({
                ...current,
                [noteId]: [
                    ...(current[noteId] || []),
                    { question: trimmedQuestion, answer: response.data.answer },
                ],
            }));
            setQuestion("");
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setQuestionLoading(false);
        }
    }

    return (
        <main className="notes-workspace">
            <aside className="notes-sidebar">
                <div className="notes-sidebar-header">
                    <Link className="notes-brand" to="/dashboard">AI Notes</Link>
                    <Link className="notes-dashboard-link" to="/dashboard">Dashboard</Link>
                </div>
                <button
                    className={`folder-nav-item ${selectedFolderId === null ? "active" : ""}`}
                    type="button"
                    onClick={() => selectFolder(null)}
                >
                    <span>All notes</span>
                </button>
                <p className="sidebar-label">Folders</p>
                {foldersLoading ? <p className="sidebar-loading">Loading folders…</p> : folders.map((folder) => (
                    <button
                        className={`folder-nav-item ${selectedFolderId === folder.uid ? "active" : ""}`}
                        type="button"
                        key={folder.uid}
                        onClick={() => selectFolder(folder.uid)}
                    >
                        <i style={{ backgroundColor: folder.color }} />
                        <span>{folder.name}</span>
                    </button>
                ))}
                <div className="sidebar-footer">
                    <Link to="/folders">Manage folders</Link>
                    <button type="button" onClick={signOut}>Log out</button>
                </div>
            </aside>

            <section className="notes-list-panel">
                <div className="notes-list-header">
                    <div>
                        <p className="panel-label">Notes</p>
                        <h1>{selectedFolderId ? folders.find((folder) => folder.uid === selectedFolderId)?.name || "Folder" : "All notes"}</h1>
                    </div>
                    <button className="new-note-button" type="button" onClick={handleNewNote} disabled={saving}>+ New</button>
                </div>
                {notesLoading ? <p className="panel-status">Loading notes…</p> : notes.length === 0 ? (
                    <p className="panel-status">No notes here yet. Create one to get started.</p>
                ) : (
                    <div className="notes-list">
                        {notes.map((note) => (
                            <button
                                className={`note-list-item ${selectedNote?.uid === note.uid ? "active" : ""}`}
                                type="button"
                                key={note.uid}
                                onClick={() => handleSelectNote(note.uid)}
                            >
                                <span className="note-list-title">{note.is_pinned && <b title="Pinned">📌</b>}{note.title || "Untitled note"}</span>
                                <small>{formatUpdatedAt(note.updated_at)}</small>
                            </button>
                        ))}
                    </div>
                )}
            </section>

            <section className="note-editor-panel">
                {error && <p className="notes-alert error" role="alert">{error}</p>}
                {message && <p className="notes-alert success">{message}</p>}
                {noteLoading ? <p className="editor-placeholder">Loading note…</p> : !selectedNote ? (
                    <div className="editor-placeholder"><h2>Select a note</h2><p>Choose a note from the list or create a new one.</p></div>
                ) : (
                    <div className="note-editor">
                        <input className="note-title-input" name="title" value={draft.title} onChange={handleDraftChange} placeholder="Untitled note" aria-label="Note title" />
                        <textarea className="note-content-input" name="content" value={draft.content} onChange={handleDraftChange} placeholder="Write your note…" aria-label="Note content" />
                        <section className="ai-insights" aria-label="AI note insights">
                            <article className="ai-insight-card">
                                <div className="ai-card-header">
                                    <div>
                                        <p className="ai-card-kicker">AI</p>
                                        <h2>AI Summary</h2>
                                    </div>
                                    <button
                                        type="button"
                                        className="ai-action-button"
                                        onClick={handleGenerateSummary}
                                        disabled={summaryGenerating || saving}
                                    >
                                        {summaryGenerating && <span className="ai-spinner" aria-hidden="true" />}
                                        {summaryGenerating ? "Generating..." : selectedNote.summary ? "Regenerate Summary" : "Generate Summary"}
                                    </button>
                                </div>
                                {selectedNote.summary ? (
                                    <p className="ai-summary-text">{selectedNote.summary}</p>
                                ) : (
                                    <p className="ai-empty-text">Create a concise overview of this note when you are ready.</p>
                                )}
                            </article>

                            <article className="ai-insight-card">
                                <div className="ai-card-header">
                                    <div>
                                        <p className="ai-card-kicker">AI</p>
                                        <h2>AI Tags</h2>
                                    </div>
                                    <button
                                        type="button"
                                        className="ai-action-button"
                                        onClick={handleGenerateTags}
                                        disabled={tagsGenerating || saving}
                                    >
                                        {tagsGenerating && <span className="ai-spinner" aria-hidden="true" />}
                                        {tagsGenerating ? "Generating..." : selectedNote.tags?.length ? "Regenerate Tags" : "Generate Tags"}
                                    </button>
                                </div>
                                {selectedNote.tags?.length ? (
                                    <div className="ai-tags" aria-label="Generated tags">
                                        {selectedNote.tags.map((tag) => <span key={tag}>{tag}</span>)}
                                    </div>
                                ) : (
                                    <p className="ai-empty-text">Generate tags to make this note easier to find later.</p>
                                )}
                            </article>
                        </section>
                        <section className="ai-assistant-card" aria-label="Ask AI about this note">
                            <div className="ai-assistant-header">
                                <div>
                                    <p className="ai-card-kicker">AI Assistant</p>
                                    <h2>Ask AI About This Note</h2>
                                </div>
                                <span>Fresh answers</span>
                            </div>
                            <form className="ai-question-form" onSubmit={handleAskQuestion}>
                                <textarea
                                    value={question}
                                    onChange={(event) => setQuestion(event.target.value)}
                                    placeholder="Ask anything about this note..."
                                    aria-label="Question about this note"
                                    disabled={questionLoading}
                                    rows="3"
                                />
                                <button type="submit" className="ask-ai-button" disabled={questionLoading || !question.trim()}>
                                    {questionLoading && <span className="ai-spinner" aria-hidden="true" />}
                                    {questionLoading ? "Thinking..." : "Ask AI"}
                                </button>
                            </form>

                            {conversation.length > 0 && (
                                <div className="ai-conversation" aria-live="polite">
                                    {conversation.map((item, index) => (
                                        <article className="ai-exchange" key={`${item.question}-${index}`}>
                                            <div className="conversation-message question-message">
                                                <strong>You</strong>
                                                <p>{item.question}</p>
                                            </div>
                                            <div className="conversation-message answer-message">
                                                <strong>AI Answer</strong>
                                                <p>{item.answer}</p>
                                            </div>
                                        </article>
                                    ))}
                                    <div ref={latestConversationRef} />
                                </div>
                            )}
                        </section>
                        <div className="editor-footer">
                            <label>
                                Folder
                                <select value={draft.folder_uid || ""} onChange={handleFolderMove} disabled={saving}>
                                    <option value="">No Folder</option>
                                    {folders.map((folder) => <option key={folder.uid} value={folder.uid}>{folder.name}</option>)}
                                </select>
                            </label>
                            <div className="editor-actions">
                                <button type="button" className="secondary-action" onClick={togglePin} disabled={saving}>{selectedNote.is_pinned ? "Unpin" : "Pin"}</button>
                                <button type="button" className="secondary-action" onClick={archiveNote} disabled={saving}>Archive</button>
                                <button type="button" className="danger-action" onClick={removeNote} disabled={saving}>Delete</button>
                                <button type="button" className="save-action" onClick={saveChanges} disabled={saving}>{saving ? "Saving…" : "Save"}</button>
                            </div>
                        </div>
                    </div>
                )}
            </section>
        </main>
    );
}

export default Notes;
