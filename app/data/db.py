from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from schemas.book import BookDB #anche se non la uso

sqlite_file_name= "/Users/alessiousai/Desktop/libri/3-SC/Programmazione-Web/lab_2026/app/data/database.db"
sqlite_url=f"sqlit:///{sqlite_file_name}"
engine = create_engine(
    sqlite_url,
    connect_args={'check_same_thread': False},
    echo=True #log delle operazioni sul database
)

def init_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep: Annotated[Session,Depends(get_session)]

