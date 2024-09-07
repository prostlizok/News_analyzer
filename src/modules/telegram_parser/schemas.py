from pydantic import BaseModel, Field
from typing import List


class RegionInfo(BaseModel):
    city: str = Field(description="City in which we detect explosions.The city should be in the nominative case in Ukrainian with a capital letter. For example, Павлоград")
    explosion: bool = Field(description="Is there an explosion")
    num_of_explosions: int = Field(description="Number of explosions") 
    damage: bool = Field(description="Are there any damage") 
    victims: bool = Field(description="Are there any victims(injured and dead)")
    num_of_victims: int = Field(description="Number of victims(injured and dead)")

class InvoiceJson(BaseModel):
    info: List[RegionInfo] = Field(description="Info collected about each region mentioned in the text")


class RegionInfoUpd(BaseModel):
    city: str = Field(description="City in which we detect explosions.The city should be in the nominative case in Ukrainian with a capital letter. For example, Павлоград")
    damage: bool = Field(description="Are there any damage") 
    victims: bool = Field(description="Are there any victims(injured and dead)")
    num_of_victims: int = Field(description="Number of victims(injured and dead)")

class InvoiceJsonUpd(BaseModel):
    info: List[RegionInfoUpd] = Field(description="Info collected about each region mentioned in the text to update")