from pydantic import BaseModel


class MediaTypeBase(BaseModel):
    media_type: str
    description: str


class MediaTypeIn(MediaTypeBase):
    pass


class MediaType(MediaTypeBase):
    class Config:
        orm_mode = True
