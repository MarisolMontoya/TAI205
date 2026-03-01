
# 1. Importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel,Field

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

#Modelo de validaciones
class crear_usuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str= Field(..., min_length=3,max_length=50, example="Juanito")
    edad: int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")

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

@app.get("/v1/parametro0/{id}",tags=['Parametros'])    #especifica que traerá un usuario mediante un id
async def consultaUno(id:int):                      #parametro que obliga a que sea en formato int
    await asyncio.sleep(3)                
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200"
        }
          
@app.get("/v1/parametro1/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono Id"}
    
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])   
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "data":usuarios
    }

@app.post("/v1/usuarios/",tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }

@app.put("/v1/usuarios/",tags=['CRUD HTTP'])
async def actualiza_usuario(usuario:dict):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario.get("id"):
            usuarios[i]=usuario
            return{
            "mensaje":"Usuario actualizado correctamente",
            "status":"200",
            "usuario":usuario
        }
    raise HTTPException(
            status_code=400,
            detail="El id no existe"
    )


@app.delete("/v1/usuarios/",tags=['CRUD HTTP'])
async def eliminar_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.remove(usr)
            return{
                "mensaje":"Usuario eliminado correctamente",
                "status":"200",
                "usuario":usuario
             }
    raise HTTPException(
            status_code=400,
            detail="El id no existe"
    )


    