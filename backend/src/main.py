from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routes import auth_router


app = FastAPI(title="AI Notes API", version="1.0.0")

# Vite's default development address. Add deployed frontend origins here when
# the application is published.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
