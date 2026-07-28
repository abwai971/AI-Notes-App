import api from "./axios";

export const generateSummary = (noteId) =>
    api.post(`/ai/notes/${noteId}/summary`);

export const generateTags = (noteId) =>
    api.post(`/ai/notes/${noteId}/tags`);

export const askQuestion = (noteId, question) =>
    api.post(`/ai/notes/${noteId}/questions`, { question });
