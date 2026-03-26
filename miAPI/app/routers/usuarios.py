from fastapi import status,HTTPException,Depends,APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

#Leer y obtener datos    
@routerU.get("/")   
async def consultaT(db:Session=Depends(get_db)):
    queryUsuarios= db.query(usuarioDB).all()
    return{
        "status":"200",
        "total":len(queryUsuarios),
        "usuarios":queryUsuarios
    }
#Crear
@routerU.post("/" ,status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:crear_usuario,db:Session=Depends(get_db)):

    usuarioNuevo= usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuarioP
    }

#actualizar
@routerU.put("/{id}")
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

# DELETE          Modificamos 
@routerU.delete("/{id}")
async def eliminar_usuario(id: int,userAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            index = usuarios.index(usr)
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {userAuth}",
                "status": "200",
                "usuario_eliminado": usr
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

    