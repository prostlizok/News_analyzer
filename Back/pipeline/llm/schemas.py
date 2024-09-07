from pydantic import BaseModel, Field
from typing import List


class RequiredInformation(BaseModel):
    city: str = Field(description="City in which we detect explosions")
    explosion: bool = Field(description="Is there an explosion")
    num_of_explosions: int = Field(description="Number of explosions") 
    damage: bool = Field(description="Are there any damage") 
    victims: bool = Field(description="Are there any victims")
    num_of_victims: int = Field(description="Number of victims")


class InvoiceJson(BaseModel):
    # text: str = Field(description="Text of news post")
    # date: str = Field(description="Date of news post")
    # channel: str = Field(description="Name of the channel with news")
    # link: str = Field(description="Link of the channel")

    emergency_info: List[RequiredInformation] = Field(default_factory=list, description="The list of collected info.")




