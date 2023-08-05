from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SubredditAliasBase(BaseModel):
    subreddit: str
    alias: str


class SubredditAlias(BaseModel):
    alias: str

    class Config:
        orm_mode = True


class SubredditBase(BaseModel):
    subreddit: str
    is_text: bool
    submitter: str


class SubredditIn(SubredditBase):
    aliases: List[str] = []


class Subreddit(SubredditBase):
    submitted: datetime
    aliases: List[SubredditAlias] = []

    class Config:
        orm_mode = True


class SubredditAliasUpdate(BaseModel):
    # We receive the subreddit implicitly through the endpoint
    alias: str
    remove: bool = False


class SubredditUpdate(BaseModel):
    is_text: Optional[bool] = None
    aliases: List[SubredditAliasUpdate] = []
