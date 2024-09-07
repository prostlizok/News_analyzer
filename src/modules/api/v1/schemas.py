from pydantic import BaseModel

class RegionInfoCreate(BaseModel):
    city: str
    explosion: bool
    num_of_explosions: int
    damage: bool
    victims: bool
    num_of_victims: int

class RegionInfo(RegionInfoCreate):
    id: int

    class Config:
        orm_mode = True
