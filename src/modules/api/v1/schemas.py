from pydantic import BaseModel

class RegionInfoCreate(BaseModel):
    city: str
    explosion: bool
    num_of_explosions: int
    damage: bool
    victims: bool
    num_of_victims: int


class RequestInfoCreate(BaseModel):
    category: str
    city: str
    lat: float
    lng: float
    contact: str
    region: str


class RequestInfo(RequestInfoCreate):
    id: int

    class Config:
        orm_mode = True

class RegionInfo(RegionInfoCreate):
    id: int

    class Config:
        orm_mode = True
