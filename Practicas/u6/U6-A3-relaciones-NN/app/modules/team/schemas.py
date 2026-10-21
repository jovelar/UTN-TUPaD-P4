from sqlmodel import SQLModel


class TeamRead(SQLModel):
    id: int
    name: str
    headquarters: str
