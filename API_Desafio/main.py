from fastapi import FastAPI, HTTPException, status, Response, Path, Depends
import schemas
import models 
import requests
from database import SessionLocal
from sqlalchemy.orm import Session
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Optional
import pymysql
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from schemas import UserCreate
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from models import User

# Cria sessão para consultar o banco de dados

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

app = FastAPI()

# Sessão para authenticação (Gambiarra)
sessao = SessionLocal()

# Processador do HASH
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = bcrypt.using(rounds=12)


SECRET_KEY = "$2a$12$REaR6.e16SEgpyzCXQveIu4swjTeOKUX.Y1p7TUAgFkQvLGusDtX."

# Função que autentica, apartir do JWT

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user

# Função que gera o JWT

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=algorithm)
    return encoded_jwt

# Retorna se o usuario existe apartir do nome (Gambiarra, era pra ser email)

def get_user(name: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.name == name).first()
        return user

# Verifica se o token é valido

def verify_token(token: str):
    algorithm = "HS256"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

# Requere o usuario logado

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid Email or password")
    return user

# Requere que o usuario logado seja admin

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    return current_user

# Rota que retorna o TOKEN JWT

@app.post("/token", tags=["Auth Endpoints"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Email or password")
    token_data = {
        "sub": user.name,
        "admin": user.admin,
    }
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer", "admin": user.admin}

# Rota para criar usuarios

@app.post("/create_user", tags=["Auth Endpoints"])
async def create_user(user: UserCreate, current_user: User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password, admin=user.admin)
    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}

# Função que deleta o usuario pelo email

def delete_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Rota para deletar o usuario

@app.delete("/users/{email}", dependencies=[Depends(get_current_admin_user)], tags=["Auth Endpoints"])
def delete_existing_user(email: str, db: Session = Depends(get_db)):
      delete_user_by_email(email, db=db)
      return {"message": f"User {email} deleted successfully"}

# Rota que retorna todos os cachorros (API + Banco de Dados)

@app.get("/all-dogs", tags=["Dogs Endpoints"])
async def get_all_dogs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    request = requests.get(f"https://api.thedogapi.com/v1/breeds/")
    dogs_db = db.query(models.Dogs).all()
    return {"Message": request.json() + dogs_db}

# Rota que retorna um cachorro por id (API e BD)

@app.get("/dogs/{id}", tags=["Dogs Endpoints"])
async def get_id(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if id > 255:
        dog = db.query(models.Dogs).filter(models.Dogs.id == id).first()
        if dog:
            return {"Message": dog}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raça não foi encontrada")
    else:
        request = requests.get(f"https://api.thedogapi.com/v1/breeds/{id}")
        return {"Message": request.json()}  
    
# Rota que adiciona um cachorro

@app.post("/dogs/add", tags=["Dogs Endpoints"])
async def post_dog(new_dog: schemas.Dog, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_dog = models.Dogs(raca=new_dog.raca, tempo_vida=new_dog.tempo_vida, descricao=new_dog.descricao, foto=new_dog.foto)
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return new_dog, Response(status_code=status.HTTP_201_CREATED) 

# Rota que atualiza um cachorro (que não seja o id da API)

@app.put('/dogs/update/{dog_id}', tags=["Dogs Endpoints"])
async def put_dog(dog_id: int, dog: schemas.Dog, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    if dog_id > 255:
        query = db.query(models.Dogs).filter(models.Dogs.id == dog_id)
        dog_db = query.first()
        if dog_db:
            query.update({models.Dogs.descricao: dog.descricao, models.Dogs.foto: dog.foto, models.Dogs.raca: dog.raca, models.Dogs.tempo_vida: dog.tempo_vida})
            db.commit()
            db.refresh(dog_db)
            return dog_db
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Esta raça não existe')         
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não é possivel deletar essa raça")


# Rota que deleta um cachorro (que não seja o id da API)

@app.delete('/dogs/delete/{dog_id}', tags=["Dogs Endpoints"])
async def delete_dog(dog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    if dog_id > 255:
        dog = db.query(models.Dogs).filter(models.Dogs.id == dog_id).first()
        if dog:
            db.delete(dog)
            db.commit()
            return {'message':  'deleted sucessefully'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raça não encontrada")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não é possivel deletar essa raça")
    
  
# Consome API externa  
  
@app.get("/placa-car")
async def get_placa():
    url = "http://10.234.82.58:8000/"
    request = requests.get(url)
    return request.json()

@app.get("/dog-id/{id}", include_in_schema=False)
async def get_placa(id:int, db: Session = Depends(get_db)):
    request = requests.get(f"https://api.thedogapi.com/v1/breeds/{id}")
    return {"Message": request.json() }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)
    
