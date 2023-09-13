from fastapi import FastAPI, HTTPException, status, Response, Path
from models import Cat
import cv2

app = FastAPI()
image = cv2.imread("./img/catbr.jpg")
img = cv2.imshow("image", image)

cats = {
    bshor: {
        "raca": "Brazilian Shorthair",
        "tempo_vida": "14-20 years",
        "descricao": "The Brazilian Shorthair is the only Brazilian feline breed to be recognized worldwide. It has a strong, agile physical condition and is medium in size.",
        "foto": url("./img/")
    },
    bshor: {
        "raca": "Brazilian Shorthair",
        "origem": "",
        "cod_pais": "10-12 years",
        "tempo_vida": "Friendly, confident",
        "descricao": "",
        "foto": cv2.im
    },
    
}