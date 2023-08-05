from typing import List, Optional
from pydantic import BaseModel


class PFMMemeBase(BaseModel):
    topic: str
    title: str
    content: str
    media_type: str
    description: Optional[str] = None


class PFMMemeIn(PFMMemeBase):
    pass


class PFMMeme(PFMMemeBase):
    class Config:
        orm_mode = True


class MemeList:  # NOTE: unused
    topic: str
    memes: List[PFMMeme] = []
