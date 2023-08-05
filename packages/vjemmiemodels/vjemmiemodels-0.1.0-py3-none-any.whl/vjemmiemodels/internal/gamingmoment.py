from pydantic import BaseModel


class GamingMomentsBase(BaseModel):
    user_id: str
    count: int


class GamingMomentsIn(GamingMomentsBase):
    pass


class GamingMoments(GamingMomentsBase):
    class Config:
        orm_mode = True
