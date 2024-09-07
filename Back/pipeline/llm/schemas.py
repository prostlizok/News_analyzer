from pydantic import BaseModel, Field
from typing import List


class InvoiceJson(BaseModel):
    city: str = Field(description="City in which we detect explosions")
    explosion: bool = Field(description="Is there an explosion")
    num_of_explosions: int = Field(description="Number of explosions") 
    damage: bool = Field(description="Are there any damage") 
    victims: bool = Field(description="Are there any victims")
    num_of_victims: int = Field(description="Number of victims")




