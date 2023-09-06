from fastapi import FastAPI, Header, Response, Cookie
from models import Item
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root(user_agent: Optional[str] = Header(None)): 
  return {"user_agent": user_agent}

@app.get("/cookie")
def cookie(response: Response):
  response.set_cookie(key="mycookie", value='123456')
  return{"cookie": True}

@app.get("/get_cookie")
def get_cookie(mycookie: Optional[str] = Cookie(None)):
  return {"Cookie": mycookie}

@app.get("/items/{item_id}")
def read_item(item_id: int, p: bool, q: Optional[str] = None):
  return {"item_id": item_id, "q": q, "p": p}

@app.post("/item")
def add_item(new_item: Item):
  return new_item


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("aula01:app", host='127.0.0.1', port=8000, log_level="info", reload=True) 