from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from schemas.book import BookDB #anche se non la uso
from schemas.users import UserDB
from faker import Faker
import os


sqlite_file_name= "/Users/alessiousai/Desktop/libri/3-SC/Programmazione-Web/lab_2026/app/data/database.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"
engine = create_engine(
    sqlite_url,
    connect_args={'check_same_thread': False},
    echo=True #log delle operazioni sul database
)

def init_database():
    ds_exists=os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f=Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):
                book=BookDB(
                    title=f.sentence(nb_words=5),
                    author=f.name(),
                    review=f.pyint(min_value=1, max_value=5),
                    user_id=f.pyint(min_value=1, max_value=10)

                )
                session.add(book)
            for i in range(10):
                user= UserDB(
                    name=f.name(), #nome casuale
                    birth_date=f.birth_date(),
                    city=f.city()

                )
                session.add(user)

            session.commit()


def get_session():
    with Session(engine) as session:
        yield session

SessionDep= Annotated[Session,Depends(get_session)]

