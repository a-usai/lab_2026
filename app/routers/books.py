from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import Book,books
from typing import Annotated
from schemas.review import Review

books_router=APIRouter(prefix="/books", tags=["books"])

@books_router.get("/")
def get_all_books(
        sort: Annotated[bool,Query(description="Sort books by their review")] = False
) -> list[Book]:
    """Ruterns the list of available books."""
    if sort:
        return sorted(books.values(),key=lambda book: book.review)
    else:
        return list(books.values())

@books_router.get("/{id}")
def get_book_by_id(id: Annotated[int, Path(description="the ID of the book to retrive")]) -> Book:
    try:
        return books[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@books_router.post("/{id}/review")
def add_review(
        id: Annotated[int, Path(description="the ID of the book to retrive")],
        review: Review
):
    """Add a review to the book with the given id"""
    try:
        books[id].review=review.review #primo=pydantic secondo= campi json
        return "Review added successfully"
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@books_router.post("/")
def add_book(book:Book):
    """Add a new book."""
    if book.id in books:
        raise HTTPException(status_code=403, detail="Book already exists")
    books[book.id]=book
    return "Book added successfully"

@books_router.put("/{id}")
def replace_book(
        id: Annotated[int, Path(description="the ID of the book to update")],
        book: Book
):
    """Replace the book with the given id"""
    if not id in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[id]=book #rimpiazzo la risorsa
    return "Book replaced successfully"

@books_router.delete("/")
def delete_all_books():
    """Remove all books from the database"""
    books.clear()
    return "Books removed successfully"

@books_router.delete("/{id}")
def delete_book(
        id: Annotated[int, Path(description="the ID of the book to delete")]
):
    """Remove the book with the given id"""
    if id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[id]
    return "Book deleted successfully"