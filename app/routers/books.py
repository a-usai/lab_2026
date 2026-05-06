from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import BookCreate,BookPublic,BookDB
from typing import Annotated
from schemas.review import Review
from data.db import SessionDep
from sqlmodel import select,delete

books_router=APIRouter(prefix="/books", tags=["books"])

@books_router.get("/")
def get_all_books(
        #prima session siccome sort ha un parametro di default
        session: SessionDep,
        sort: Annotated[bool,Query(description="Sort books by their review")] = False

) -> list[BookPublic]:
    """Ruterns the list of available books."""
    books=session.exec(select(BookDB)).all()
    if sort:
        return sorted(books,key=lambda book: book.review)
    else:
        return list(books)

@books_router.get("/{id}")
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="the ID of the book to retrive")]
) -> BookPublic:
    """Ruterns the book with the given id"""
    book=session.get(BookDB, id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@books_router.post("/{id}/review")
def add_review(
        session: SessionDep,
        id: Annotated[int, Path(description="the ID of the book to retrive")],
        review: Review
):
    """Add a review to the book with the given id"""
    book=session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.review=review.review #aggiornamento campo review
    session.add(book)
    session.commit()

    return "Review added successfully"


@books_router.post("/")
def add_book(session: SessionDep,book:BookCreate):
    """Add a new book."""
    book_entry=BookDB.model_validate(book) #trasforma in un entità del database
    session.add(book_entry)
    session.commit() #rendiamo effettive le modifiche al database

    return "Book added successfully"

@books_router.put("/{id}")
def replace_book(
        session: SessionDep,
        id: Annotated[int, Path(description="the ID of the book to update")],
        new_Book: BookCreate
):
    """Replace the book with the given id"""
    book=session.get(BookDB, id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title=new_Book.title
    book.review=new_Book.review
    book.author=new_Book.author
    session.add(book)
    session.commit()

    return "Book replaced successfully"

@books_router.delete("/")
def delete_all_books(session: SessionDep):
    """Remove all books from the database"""
    session.exec(delete(BookDB))
    session.commit()
    return "Books removed successfully"

@books_router.delete("/{id}")
def delete_book(
        session: SessionDep,
        id: Annotated[int, Path(description="the ID of the book to delete")]
):
    """Remove the book with the given id"""
    book=session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book) #elimina una riga
    session.commit()
    return "Book deleted successfully"