import api from "./axios";

export const getFolders = () => api.get("/folders/");

export const getFolder = (folderId) => api.get(`/folders/${folderId}`);

export const createFolder = (data) => api.post("/folders/", data);

export const updateFolder = (folderId, data) =>
    api.patch(`/folders/${folderId}`, data);

export const deleteFolder = (folderId) => api.delete(`/folders/${folderId}`);
