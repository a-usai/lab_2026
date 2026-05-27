#from pydantic import BaseModel,Field importiamo Field nell'sqlmodel
from typing import Annotated
from sqlmodel import SQLModel,Field

class BookBase(SQLModel):
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)] = None


#usata nelle post
class BookCreate(BookBase):
    pass

#inserisco l'id perchè è utile al client
class BookPublic(BookBase):
    id: int

#TABLE=TRUE
class BookDB(BookBase, table=True):
    #impostazione dell'id come chiave primaria
    id: int=Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="userdb.id") #collegamento con la tabella userdb