import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../components/Button/Button";
import Input from "../../components/Input/Input";
import { createFolder, deleteFolder, getFolders, updateFolder } from "../../api/folders";
import { removeTokens } from "../../utils/token";
import useAuth from "../../hooks/useAuth";
import "./Folders.css";

const emptyFolder = { name: "", description: "", color: "#2563eb" };

function getErrorMessage(error) {
    const detail = error.response?.data?.detail;
    return typeof detail === "string" ? detail : "Something went wrong. Please try again.";
}

function Folders() {
    const navigate = useNavigate();
    const { setUser } = useAuth();
    const [folders, setFolders] = useState([]);
    const [formData, setFormData] = useState(emptyFolder);
    const [editingId, setEditingId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");

    async function loadFolders() {
        setLoading(true);
        setError("");
        try {
            const response = await getFolders();
            setFolders(response.data);
        } catch (requestError) {
            if ([401, 403].includes(requestError.response?.status)) {
                removeTokens();
                setUser(null);
                navigate("/login", { replace: true });
                return;
            }
            setError(getErrorMessage(requestError));
        } finally {
            setLoading(false);
        }
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
                    removeTokens();
                    setUser(null);
                    navigate("/login", { replace: true });
                    return;
                }
                setError(getErrorMessage(requestError));
            })
            .finally(() => {
                if (isCurrent) setLoading(false);
            });

        return () => {
            isCurrent = false;
        };
    }, [navigate, setUser]);

    function handleChange(event) {
        setFormData((current) => ({ ...current, [event.target.name]: event.target.value }));
    }

    function startEditing(folder) {
        setEditingId(folder.uid);
        setFormData({ name: folder.name, description: folder.description || "", color: folder.color });
        setError("");
    }

    function cancelEditing() {
        setEditingId(null);
        setFormData(emptyFolder);
        setError("");
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setSaving(true);
        setError("");
        try {
            if (editingId) {
                await updateFolder(editingId, formData);
            } else {
                await createFolder(formData);
            }
            cancelEditing();
            await loadFolders();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        } finally {
            setSaving(false);
        }
    }

    async function handleDelete(folderId) {
        if (!window.confirm("Delete this folder? This cannot be undone.")) return;
        setError("");
        try {
            await deleteFolder(folderId);
            setFolders((current) => current.filter((folder) => folder.uid !== folderId));
            if (editingId === folderId) cancelEditing();
        } catch (requestError) {
            setError(getErrorMessage(requestError));
        }
    }

    function handleLogout() {
        removeTokens();
        setUser(null);
        navigate("/login");
    }

    return (
        <main className="folders-page">
            <header className="folders-header">
                <div>
                    <p className="eyebrow">AI Notes</p>
                    <h1>Your folders</h1>
                    <p>Organize your notes into focused spaces.</p>
                </div>
                <div className="header-actions">
                    <Link className="text-link" to="/dashboard">Dashboard</Link>
                    <button className="text-button" type="button" onClick={handleLogout}>Log out</button>
                </div>
            </header>

            <section className="folders-content">
                <form className="folder-form" onSubmit={handleSubmit}>
                    <h2>{editingId ? "Edit folder" : "New folder"}</h2>
                    <Input label="Name" name="name" value={formData.name} onChange={handleChange} />
                    <label className="input-group">
                        <span>Description <small>(optional)</small></span>
                        <textarea name="description" value={formData.description} onChange={handleChange} rows="3" />
                    </label>
                    <label className="input-group color-input">
                        <span>Color</span>
                        <input name="color" type="color" value={formData.color} onChange={handleChange} />
                    </label>
                    {error && <p className="form-error">{error}</p>}
                    <Button type="submit" disabled={saving}>
                        {saving ? "Saving..." : editingId ? "Save changes" : "Create folder"}
                    </Button>
                    {editingId && <button className="cancel-button" type="button" onClick={cancelEditing}>Cancel</button>}
                </form>

                <section className="folders-list" aria-live="polite">
                    <div className="list-heading"><h2>All folders</h2><span>{folders.length}</span></div>
                    {loading ? <p className="empty-state">Loading folders...</p> : folders.length === 0 ? (
                        <p className="empty-state">Create your first folder to get organized.</p>
                    ) : (
                        <div className="folder-grid">
                            {folders.map((folder) => (
                                <article className="folder-card" key={folder.uid}>
                                    <span className="folder-color" style={{ backgroundColor: folder.color }} />
                                    <div className="folder-card-content"><h3>{folder.name}</h3><p>{folder.description || "No description"}</p></div>
                                    <div className="folder-actions">
                                        <button type="button" onClick={() => startEditing(folder)}>Edit</button>
                                        <button type="button" className="delete-button" onClick={() => handleDelete(folder.uid)}>Delete</button>
                                    </div>
                                </article>
                            ))}
                        </div>
                    )}
                </section>
            </section>
        </main>
    );
}

export default Folders;
