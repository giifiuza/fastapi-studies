from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Curso(BaseModel):
    id: Optional[int]
    name: str
    aulas: float 
    horas: float
    instrutor: str 

cursos = {
    1: {
        "name": "python",
        "aulas": 20,
        "horas": 80,
        "instrutor": "Cleber"
    },
    2: {
        "name": "Java",
        "aulas": 15,
        "horas": 60,
        "instrutor": "Leonardo"
    },
}


@app.get("/")
async def get_all_cursos():
    return cursos


@app.get("/cursos/{curso_id}")
async def get_cursos(curso_id: int):
    try:
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
        return {"message": curso}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')

@app.post("/cursos/adicionar")
async def post_cursos(curso: Curso):
    curso.id = len(cursos) + 1
    cursos[curso.id] = curso
    return curso

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)