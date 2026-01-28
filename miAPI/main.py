# 1. Importaciones
from fastapi import FastAPI


# 2. Inicialización APP
app=FastAPI()


# 3. Endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}
            # llave    #valor de la llave 

#que la función tenga otro nombre
@app.get("/bienvenidos")
async def bien():
    return {"mensaje":"Bienvenidos"}
            # llave    #valor de la llave 