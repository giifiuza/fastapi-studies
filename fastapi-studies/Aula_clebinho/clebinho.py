from fastapi import FastAPI, HTTPException, status, Response, Path
from models import Curso

app = FastAPI()

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
async def get_cursos(curso_id: int = Path(dafault=None, title='ID do Curso', description='Deve estar entre 1 e 2', gt=0, lt=3)):
    try:
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
        return {"message": curso}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')

@app.post("/cursos/adicionar")
async def post_cursos(curso: Curso):
    curso.id = len(cursos) + 1
    if curso.id not in cursos:
        cursos[curso.id] = curso
        return curso, Response(status_code=status.HTTP_201_CREATED) 
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'O curso com id {curso.id} já exixte!')
        

@app.put('cursos/atualizar/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Este curso não existe')


@app.delete("/cursos/apagar/{curso_id}")
async def apagar_cursos(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT) 
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Curso não existe')
  
  
@app.get('/calculadora')
async def calcular(a: int, b: int, c: int):
    soma = a + b + c
    return{"result": soma} 


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
    