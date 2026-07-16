from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.auth.routes import auth_router
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
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=["auth"])