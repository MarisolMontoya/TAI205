# 1. Importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio


# 2. Inicialización APP
app=FastAPI(
    title='Mi Primer API',
    description="Marisol Montoya Botello",
    version='1.0.0'
    )                  #para personalizar

# BD ficticia
usuarios=[
    {"id":1,"nombre":"Marisol","edad":20},
    {"id":2,"nombre":"Diego","edad":20},
    {"id":3,"nombre":"Ivan","edad":20},
]

# 3. Endpoints
@app.get("/",tags=['Inicio'])    #etiqueta
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}
            # llave    #valor de la llave 

#que la función tenga otro nombre
@app.get("/bienvenidos", tags=['Inicio'])    #etiqueta
async def bien():
    return {"mensaje":"Bienvenidos"}
            # llave    #valor de la llave

@app.get("/v1/promedio", tags=['Calificaciones'])   #etiqueta
async def promedio():
    await asyncio.sleep(3)                    #Señala que habrá un tiempo de espera #peticion, consulta a una BD
    return {
        "Calificacion":"9.5",
        "estatus":"200"
        }

@app.get("/v1/usuario/{id}",tags=['Parametros'])    #especifica que traerá un usuario mediante un id
async def consultaUno(id:int):                      #parametro que obliga a que sea en formato int
    await asyncio.sleep(3)                
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200"
        }
          
@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono Id"}