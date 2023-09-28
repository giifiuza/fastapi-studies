from fastapi import FastAPI, HTTPException, status, Response, Path, Depends
import schemas
import models 
import requests
from database import SessionLocal
from sqlalchemy.orm import Session
import numpy as np

# Cria sessão para consultar o banco de dados

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

app = FastAPI()

"""
    ID começa com 265 para continuar os IDs da API que está sendo consumida
"""

# dogs = {
#     265: {
#         "raca": "Brazilian Terrier",
#         "tempo_vida": "13-16 years",
#         "descricao": "A completely Brazilian breed that resulted in a fearless, energetic, very intelligent dog.",
#         "foto": "https://www.petz.com.br/cachorro/racas/fox-paulistinha/img/fox-paulistinha-caracteristicas-guia-racas.webp"
#     },
#     266: {
#         "raca": "Vira-lata",
#         "tempo_vida": "15 anos",
#         "descricao": "The vira-latas are very attached to humans and love the idea of ​​having a home full of love for them!",
#         "foto": "https://www.petz.com.br/cachorro/racas/vira-lata/img/vira-lata-caracteristicas-guia-racas.webp"
#     }  
# }

@app.get("/all-dogs")
async def get_all_dogs(db: Session = Depends(get_db)):
    request = requests.get(f"https://api.thedogapi.com/v1/breeds/")
    dogs_db = db.query(models.Dogs).all()
    return {"Message": request.json() + dogs_db}

@app.get("/dogs/{id}")
async def get_id(id:int, db: Session = Depends(get_db)):
    if id > 255:
        dog = db.query(models.Dogs).filter(models.Dogs.id == id).first()
        if dog:
            return {"Message": dog}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Raça não foi encontrada")
    else:
        request = requests.get(f"https://api.thedogapi.com/v1/breeds/{id}")
        return {"Message": request.json()}  
    
@app.post("/dogs/add")
async def post_dog(new_dog: schemas.Dog, db: Session = Depends(get_db)):
    db_dog = models.Dogs(raca=new_dog.raca, tempo_vida=new_dog.tempo_vida, descricao=new_dog.descricao, foto=new_dog.foto)
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return new_dog, Response(status_code=status.HTTP_201_CREATED) 


@app.put('/dogs/update/{dog_id}')
async def put_dog(dog_id: int, dog: schemas.Dog, db: Session = Depends(get_db)):
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



@app.delete('/dogs/delete/{dog_id}')
async def delete_dog(dog_id: int, db: Session = Depends(get_db)):
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
    
  
@app.get("/placa-car")
async def get_placa():
    url = "http://10.234.82.58:8000/"
    request = requests  .get(url)
    return request.json()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)
    
