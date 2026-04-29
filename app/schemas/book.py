from pydantic import BaseModel,Field
from typing import Annotated

class BookPatch(BaseModel):
    title: str | None= None
    author: str | None= None
    author: str
    review: int


class Book(BaseModel):
    id: int
    title: str
    author: str
    review: Annotated[int, Field(ge=1,le=5)]= None

    model_config= {
        "json_schema_extra": {
            "examples": [
                {
                "id": 1,
                "title": "Il nome della rosa",
                "author": "Umberto Eco",
                "review": 5
                }
            ]
        }
    }

books= {
    0: Book(id=0, title="Il nome della rosa", author="Umberto Eco", review=5),
    1: Book(id=1, title="Il signore degli anelli", author="J.R.R. Tolkien", review=4),
    2: Book(id=2, title="Il codice da Vinci", author="Dan Brown", review=3)

}