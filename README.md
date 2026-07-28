# 🧠 AI Notes App

An AI-powered note-taking application built with **FastAPI**, **React**, **PostgreSQL**, and **Google Gemini**. It combines traditional note management with AI features such as automatic summaries, intelligent tagging, and question answering.

> 🚧 This project is currently under active development.

---

## ✨ Features

### 🔐 Authentication
- JWT Authentication
- Access & Refresh Tokens
- Secure password hashing
- Token revocation with Redis

### 📝 Notes Management
- Create, edit, and delete notes
- Pin and archive notes
- Organize notes into folders
- Rich note organization

### 🤖 AI Features
- AI-generated note summaries
- AI-generated tags
- Ask questions about individual notes using AI
- Automatic caching of AI-generated summaries and tags

---

## 🛠 Tech Stack

### Backend
- FastAPI
- SQLModel
- SQLAlchemy (Async)
- PostgreSQL (Neon)
- Alembic
- Redis
- Google Gemini API
- JWT Authentication

### Frontend
- React
- TypeScript
- Tailwind CSS
- Axios

---

## 📂 Project Structure

```
AI-Notes-App/
│
├── backend/
│   ├── src/
│   │   ├── ai/
│   │   ├── auth/
│   │   ├── folders/
│   │   ├── notes/
│   │   ├── db/
│   │   └── ...
│   └── alembic/
│
├── frontend/
│
└── README.md
```

---

## 🤖 AI Capabilities

### 1. AI Summary

Generate concise summaries for any note.

Example:

> FastAPI uses JWT authentication with Redis-backed token revocation. Passwords are securely hashed using bcrypt, and SQLModel is used as the ORM.

---

### 2. AI Tags

Automatically generate relevant tags.

Example:

```
FastAPI
JWT
Redis
SQLModel
Authentication
Python
```

---

### 3. AI Q&A

Ask questions about a note.

Example:

**Question**

> How are revoked tokens handled?

**Answer**

> Revoked JWT identifiers (JTIs) are stored in Redis and checked during authentication.

---

## 🚀 Getting Started

### Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn src:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
DATABASE_URL=
JWT_SECRET=
JWT_ALGORITHM=
REDIS_HOST=
REDIS_PORT=
GEMINI_API_KEY=
GEMINI_MODEL=
```

---

## 📈 Roadmap

### ✅ Completed

- User Authentication
- Folder Management
- Notes CRUD
- AI Summaries
- AI Tags
- AI Question Answering

### 🚧 In Progress

- Semantic Search using Embeddings

### 🔜 Planned

- AI Chat across Notes (RAG)
- Similar Notes Recommendation
- AI Rewrite & Grammar Correction
- AI Note Translation
- Markdown Editor
- File Attachments
- Full-text Search

---

## 📸 Screenshots

Screenshots and demo GIFs will be added soon.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Abuno Waikhom**

If you like this project, consider giving it a ⭐ on GitHub.
