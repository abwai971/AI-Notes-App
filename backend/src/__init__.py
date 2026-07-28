from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.auth.routes import auth_router
from src.folders.routes import folder_router
from src.notes.routes import note_router
from src.ai.routes import ai_router
# from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting ...")
    # await init_db()
    yield
    print(f"Server is shutting down ...")

version = "v1"
app = FastAPI(
    title="AI Notes App",
    description="A Notes taking app with AI integration",
    version=version,
    lifespan=life_span
    )

# Vite's default development address. Add deployed frontend origins here when
# the application is published.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=["auth"])
app.include_router(folder_router,prefix=f"/api/{version}/folders",tags=["Folders"])
app.include_router(note_router,prefix=f"/api/{version}/notes",tags=["Notes"])
app.include_router(ai_router,prefix=f"/api/{version}/ai",tags=["AI"])



@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
