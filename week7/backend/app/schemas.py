from datetime import datetime

from pydantic import BaseModel, constr


NonEmptyStr = constr(strip_whitespace=True, min_length=1)


class NoteCreate(BaseModel):
    title: NonEmptyStr
    content: NonEmptyStr


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: NonEmptyStr | None = None
    content: NonEmptyStr | None = None


class ActionItemCreate(BaseModel):
    description: NonEmptyStr


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: NonEmptyStr | None = None
    completed: bool | None = None


