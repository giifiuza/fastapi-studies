from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str 
#     price: float
#     tax: float 

cursos = {
    1: {
        "nome": "python",
        "aulas": 20,
        "horas": 80,
        "instrutor": "Cleber"
    },
    2: {
        "nome": "Java",
        "aulas": 15,
        "horas": 60,
        "instrutor": "Leonardo"
    },
}

@app.get("/cursos/{curso_id}")
async def get_cursos(curso_id: int):
    try:
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
        return {"message": curso}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)