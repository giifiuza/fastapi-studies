from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
import requests

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 

from models.dog_models import DogModel
from schemas.dog_schemas import DogSchema
from core.deps import get_session

router = APIRouter()

@router.get('/', response_model=List[DogSchema])
async def get_cachorros(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(DogModel)
    result = await session.execute(query)
    dogs: List[DogModel] = result.scalars().all()
    return dogs
  

@router.get('/{dog_id}', response_model=DogSchema, status_code=status.HTTP_200_OK)
async def get_cachorro(dog_id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(DogModel).filter(DogModel.id == dog_id)
    result = await session.execute(query)
    dog = result.scalar_one_or_none()
    if dog:
      return dog
    else:
      raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cachorro não encontrado!'))  
    
  
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DogSchema)
async def post_cachorro(dog: DogSchema, db:AsyncSession = Depends(get_session)):
  novo_cachorro = DogModel(id = 0,
                          raca = dog.raca,
                          tempo_vida = dog.tempo_vida,
                          descricao = dog.descricao)
  
  db.add(novo_cachorro)
  await db.commit()
  return novo_cachorro

@router.put('/{dog_id}', response_model=DogSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_cachorro(dog_id: int, dog: DogSchema, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(DogModel).filter(DogModel.id == dog_id)
    result = await session.execute(query)
    dog_up = result.scalar_one_or_none()
    if dog_up:
      dog_up.raca = dog.raca
      dog_up.tempo_vida = dog.tempo_vida
      dog_up.descricao = dog.descricao
      await session.commit()
      return dog_up
      
@router.delete('/{dog_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cachorro(dog_id: int, db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(DogModel).filter(DogModel.id == dog_id)
    result = await session.execute(query)
    dog_del = result.scalar_one_or_none()
    if dog_del:
      await session.delete(dog_del)
      await session.commit()
      return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
      raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cachorro não encontrado!'))
  
@router.get('/', status_code=status.HTTP_404_NOT_FOUND, tags=["Consumindo"])
async def get_api():
  request = requests.get(f"https://api.thedogapi.com/v1/breeds/")
  print(request)
  return request.json()
