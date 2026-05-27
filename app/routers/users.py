from fastapi import APIRouter, HTTPException
from data.db import SessionDep
from schemas.users import UserDB, UserPublic
from sqlmodel import select
from schemas.book import BookDB, BookPublic
from schemas.book_user_link import BookUserLink
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
    user=session.get(UserDB, id)
    if not user:
        raise HTTPException(404, detail="User not found")
    statement= select(BookDB).join(BookUserLink).where(BookUserLink.user_id==id) #query da eseguire
    result=session.exec(statement).all() #risultato della query
    return result
