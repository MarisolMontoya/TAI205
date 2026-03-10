# 1. Importaciones
from fastapi import FastAPI,status,HTTPException,Depends,BaseModel
from typing import Optional
from datetime import datetime
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Inicializar API
app = FastAPI (
    title='Examen 2do Parcial'
)

# Listas para reservas
Reservas =[]

# Funcion para credenciales
seguridad = HTTPBasic

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth=secrets.compare_digest(credenciales.username,"hotel")
    passAuth=secrets.compare_digest(credenciales.password,"r2026")

    if not(userAuth and passAuth ):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas."
        )
    return credenciales.username

#Modelos:
#Huesped
class reserva(BaseModel):
    id:int = field(..., gt=1)
    nombre:str= Field(..., min_length=5, example="Maria")
    fecha_entrada: int = Field(...,le=datetime.now().year)
    fecha_salida:int = field(..., gt=fecha_entrada)
    t_habitacion:literal ["sencilla", "doble", "suite"] = "sencilla"
    estancia: int = field(..., gl=7)
    status:literal ["confirmado","cancelado"] = "confirmado"


#Endpoints
# CREAR reserva (POST) con SEGURIDAD
@app.post("/v1/crear_reserva", tags=["CRUD Hotel"])
async def crear_reserva(reserva: Reserva,userAuth: str = Depends(verificar_peticion)):
    for l in Reservas:
        if l.id() == reserva.id():
            raise HTTPException(
                status_code=400,
                detail="La reserva ya existe"
            )
    Reservas.append(reserva)
    return {
        "mensaje": "La reserva fue agregada correctamente",
        "Reserva": reserva
    }

# LISTAR RESERVAS (GET)
@app.get("/v1/ver_reservas", tags = ["CRUD Hotel"])
async def listar_reservas():
    return{
        "status": "200",
        "total": len(Reservas),
        "data":Reservas
    }

#Consultar por ID (GET{id})
@app.get("/v1/consultar_reserva_id{id}", tags = ["CRUD Hotel"])
async def consultar_reservas(id:int):
    for reserva in Reservas:
        if reserva.id()== id():
            return reserva
    raise HTTPException(
        status_code = 400,
        detail="Id no encontrado"
    )

# Confirmar reserva (PUT: actualizar estado)
@app.put("/v1/confirmar_reserva {id}",tags=["CRUD Hotel"])
async def confirmar_reserva(id:int):
    for l in Reservas:
        if l.id() == reserva.id():
            id.status = "confirmado"
            return {
                "mensaje": "Reserva confirmada",
                "status": "200"
                }
   

#Cancelar reservas (put: actualizar estado) con SEGURIDAD
@app.put("/v1/cancelar_reserva{id}", tags=["CRUD Hotel"])
async def cancelar_reserva(id: int,userAuth: str = Depends(verificar_peticion)):
    for l in Reservas:
        if l.id() == reserva.id():
            id.status = "cancelado"
            return{
                "mensaje":"Reserva confirmada",
                "status":"200"
            }
    raise HTTPException(
        status_code=409,
        detail="No existe un registro de esta reserva."
    )