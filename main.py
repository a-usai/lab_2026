from fastapi import FastAPI, Request #con Request importiamo il tipo di dato
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app=FastAPI()
templates=Jinja2Templates(directory="templates") #diciamo in che cartella si trovano i templates

@app.get("/", response_class=HTMLResponse)
def home(request: Request): #request viene passato direttamente da fastapi, rappresenta la richiesta get

    text={
        "title": "Home Page",
        "content": "Welcome to the home page!"

    }
    #context serve a passare il contenuto da back a frontend
    context={
        "text": text, "sequence": ["a","b","c"]
    }

    #non ha alcun senso però request dobbiamo passaro sempre
    #home rappresenta il ile all'interno della cartella indicata prima
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context
    )