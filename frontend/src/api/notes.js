import api from "./axios";

export const getNotes = (folderId = null) =>
    api.get("/notes/", {
        params: folderId ? { folder_uid: folderId } : undefined,
    });

export const getNote = (noteId) => api.get(`/notes/${noteId}`);

export const createNote = (data) => api.post("/notes/", data);

export const updateNote = (noteId, data) => api.patch(`/notes/${noteId}`, data);

export const deleteNote = (noteId) => api.delete(`/notes/${noteId}`);
