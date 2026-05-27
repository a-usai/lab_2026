from fastapi import FastAPI
from routers.books import books_router
from contextlib import asynccontextmanager
from data.db import init_database
from routers.users import users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #on create
    init_database()
    yield #tiene in sospeso la funzione
    #on close


app=FastAPI(lifespan=lifespan)

app.include_router(books_router)
app.include_router(users_router)