from fastapi import APIRouter
from data.db import SessionDep
from schemas.users import UserDB, UserPublic
from sqlmodel import select
from schemas.book import BookDB, BookPublic

users_router= APIRouter(prefix="/users")

@users_router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]: #questa tipizzazione permette la censura della password
    #siccome in UserPublic non è presente quel campo
    """Returns all users"""
    users=session.exec(select(UserDB)).all()
    return users

@users_router.get("/{id}/books")
def get_user_books(
        id: int,
        session: SessionDep
) ->list[BookPublic]:
    """Returns all book held by the given user"""
    statement= select(BookDB).join(UserDB).where(UserDB.id==id) #query da eseguire
    result=session.exec(statement).all() #risultato della query
    return result