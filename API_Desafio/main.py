from fastapi import FastAPI, HTTPException, status, Response, Path
from models import Dog
import requests


app = FastAPI()

dogs = {
    265: {
        "raca": "Brazilian Terrier",
        "tempo_vida": "13-16 years",
        "descricao": "A completely Brazilian breed that resulted in a fearless, energetic, very intelligent dog.",
        "foto": "https://www.petz.com.br/cachorro/racas/fox-paulistinha/img/fox-paulistinha-caracteristicas-guia-racas.webp"
    },
    266: {
        "raca": "Vira-lata",
        "tempo_vida": "15 anos",
        "descricao": "The vira-latas are very attached to humans and love the idea of ​​having a home full of love for them!",
        "foto": "https://www.petz.com.br/cachorro/racas/vira-lata/img/vira-lata-caracteristicas-guia-racas.webp"
    }  
}

@app.get("/all-dogs")
async def get_all_dogs():
    request = requests.get(f"https://api.thedogapi.com/v1/breeds/")
    return {"Message": [request.json(), dogs]}

@app.get("/dogs/{id}")
async def get_id(id:int):
    if id not in dogs:
        request = requests.get(f"https://api.thedogapi.com/v1/breeds/{id}")
        return {"Message": request.json()}  
    else:
        return {"Message": dogs[id]}
    
@app.post("/dogs/add")
async def post_dog(new_dog: Dog):
    dog_id = len(dogs) + 1 
    if dog_id not in dogs:
        dogs[dog_id] = new_dog
        del new_dog.id
        return new_dog, Response(status_code=status.HTTP_201_CREATED) 
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'A raça com id {dog_id} já exixte!')

@app.put('/dogs/update/{dog_id}')
async def put_dog(dog_id: int, dog: Dog):
    if dog_id in dogs:
        del dog.idtea
        dogs[dog_id] = dog
        return dogs
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Esta raça não existe')

@app.delete('/dogs/delete/{dog_id}')
async def delete_dog(dog_id: int):
    if dog_id in dogs:
        del dogs[dog_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT) 
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Esta raça não existe')
  
@app.get("/placa-car")
async def get_placa():
    url = "http://10.234.82.58:8000/"
    request = requests.get(url)
    return request.json()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)
    