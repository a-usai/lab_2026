from fastapi import FastAPI, Request, Form #con Request importiamo il tipo di dato
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from typing import Annotated
from pydantic import Field, BaseModel

class Product(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)] | None = None,
    price: Annotated[float, Field(gt=0)] | None = None,
    location: Annotated[str, Field(min_length=3)] | None = None

product= Product.model_validate(
    {"name": "notebook DELL","price":2999.99,"location":"Cagliari"}
)
print(product.model_dump_json())

app=FastAPI()
templates=Jinja2Templates(directory="templates") #diciamo in che cartella si trovano i templates
app.mount("/static",StaticFiles(directory="static"),name="static")

product_list=[
    {"name": "notebook DELL","price":2999.99,"location":"Cagliari"},
    {"name": "telefono SAMSUNG","price":999.99,"location":"Cagliari"},
    {"name": "tablet APPLE","price":1299.99,"location":"Cagliari"}
]

@app.get("/", response_class=HTMLResponse)
def home(request: Request): #request viene passato direttamente da fastapi, rappresenta la richiesta get

    #non ha alcun senso però request dobbiamo passaro sempre
    #home rappresenta il ile all'interno della cartella indicata prima
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"text":"Welcome to the store"}
    )

@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"product_list": product_list}
    )

@app.get("/add_product", response_class=HTMLResponse)
def add_product(request: Request):

    #restituisco la mia pagina web
    return templates.TemplateResponse(
        request=request,
        name="add_product.html",
    )

@app.post("/insert_product")
def insert_product(
        product: Annotated[Product, Form()]
):
    product_list.append(product.model_dump())

    return "product added successfully"

@app.post("/insert_product_json")
def insert_product_json(
    product:Product
):
    print(product)