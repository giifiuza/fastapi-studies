from fastapi import APIRouter
from api.v1.endpoints import dog

api_router = APIRouter()
api_router.include_router(dog.router, prefix='/dog', tags=["Cachorros"])