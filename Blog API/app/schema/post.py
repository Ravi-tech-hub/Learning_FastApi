from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int

class PostResponse(PostCreate):
    id: int
    image: str | None

    class Config:
        from_attributes = True
