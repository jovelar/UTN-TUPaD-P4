from sqlmodel import SQLModel


class WeaponCreate(SQLModel):
    name: str


class WeaponRead(SQLModel):
    id: int
    name: str