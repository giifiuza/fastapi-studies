from fastapi import FastAPI, Header, Response, Cookie
from models import Product
from typing import Optional

app = FastAPI()

database_list = []

@app.get("/product/get-all")
def list_product():
  return database_list

@app.get("/products/price_total")
def price_total():
  valor = sum([produto.valor * produto.quantidade for produto in database_list])
    
  return {"total": valor}

@app.post("/product")
def add_product(product: Product):
  database_list.append(product)
  return product


  
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("firstapi:app", host='127.0.0.1', port=8000, log_level="info", reload=True) 
