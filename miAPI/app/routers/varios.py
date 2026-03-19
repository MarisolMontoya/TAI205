from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(tags=['Inicio'])

# 3. Endpoints
@routerV.get("/")    #etiqueta
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}
            # llave    #valor de la llave 

#que la función tenga otro nombre
@routerV.get("/bienvenidos")    #etiqueta
async def bien():
    return {"mensaje":"Bienvenidos"}
            # llave    #valor de la llave

@routerV.get("/v1/promedio")   #etiqueta
async def promedio():
    await asyncio.sleep(3)                    #Señala que habrá un tiempo de espera #peticion, consulta a una BD
    return {
        "Calificacion":"9.5",
        "estatus":"200"
        }

@routerV.get("/v1/parametro0/{id}")    #especifica que traerá un usuario mediante un id
async def consultaUno(id:int):                      #parametro que obliga a que sea en formato int
    await asyncio.sleep(3)                
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200"
        }
          
@routerV.get("/v1/parametro1/")
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono Id"}

