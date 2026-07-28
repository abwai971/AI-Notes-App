from sqlmodel import Column, SQLModel, Field, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    ) 
    username: str = Field(sa_column=Column(pg.VARCHAR, unique=True, index=True))
    email: str = Field(sa_column=Column(pg.VARCHAR, unique=True, index=True))
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    password_hash: str = Field(exclude=True)
    is_active: bool = True
    folders: List["Folder"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    notes: List["Note"] = Relationship(back_populates="user")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

class Folder(SQLModel, table = True):
    __tablename__ = "folders"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    ) 
    name: str
    description: Optional[str] = None
    color: str
    user_uid: Optional[uuid.UUID] = Field(foreign_key="users.uid")
    user: Optional["User"] = Relationship(back_populates="folders")
    notes: List["Note"] = Relationship(back_populates="folders")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

class Note(SQLModel, table = True):
    __tablename__ = "notes"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    content: str
    is_pinned: bool = False
    is_archived: bool = False
    user_uid: Optional[uuid.UUID] = Field(foreign_key="users.uid")
    folder_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="folders.uid"
    )
    user: Optional["User"] = Relationship(back_populates="notes")
    folders: Optional["Folder"] = Relationship(back_populates="notes")
    summary: str | None = Field(default=None, sa_column=Column(pg.TEXT, nullable=True))
    tags: list[str] | None = Field(default=None, sa_column=Column(pg.JSONB))
    ai_updated_at: datetime | None = Field(default=None, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


