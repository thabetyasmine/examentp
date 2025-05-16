from typing import List
from pydantic import BaseModel
class ActorBase(BaseModel):
    actor_name: str

class ActorPublic(ActorBase):
    id: int

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    year: int
    director: str
    actors: List[ActorBase]

class MoviePublic(BaseModel):
    id: int
    title: str
    year: int
    director: str
    actors: List[ActorPublic]

    class Config:
        orm_mode = True


class SummaryRequest(BaseModel):
    movie_id: int

class SummaryResponse(BaseModel):
    summary_text: str

