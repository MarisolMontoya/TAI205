
# 1. Importaciones
from fastapi import FastAPI,status,HTTPException,Depends
from typing import Optional
import asyncio
from pydantic import BaseModel,Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 2. Inicialización APP
app=FastAPI(
    title='Mi API con JWT y OAuth2',
    description="Marisol Montoya Botello",
    version='2.0.0'
    )                  #para personalizar

# BD ficticia
usuarios=[
    {"id":1,"nombre":"Marisol","edad":20},
    {"id":2,"nombre":"Diego","edad":20},
    {"id":3,"nombre":"Ivan","edad":20},
]

#Confiuracion de OAuth2 Y JWT
SECRET_KEY ="mi_clave_secreta_segura"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 30 #tiempo que tendrá para expirarse (30 min)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#mi usuario para pruebas
fake_user={
    "username":"marisolmontoya",
    "password":"123456"
}

#Creación edl token (para crearlo)
def crear_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return token

#Modelo de validaciones
class crear_usuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str= Field(..., min_length=3,max_length=50, example="Juanito")
    edad: int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")


# 3. Endpoints

#ENPOINT para el login y generar el token
@app.post("/token")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException (status_code=401, detail="Credenciales incorrectas")

    access_token = crear_token({"sub":form_data.username})

    return{
        "access_token":access_token,
        "token_type": "bearer"
    }

# Funcion para validar el token
def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="El Token es inválido")
        return username
    except  JWTError:
        raise HTTPException(
            status_code=401,
            detail="El token es inválido o está expirado",
            headers={"WWW-Authenticate":"Bearer"}
        )
    

#ENDPOINT DE inicio
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
#Leer y obtener datos    
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])   
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "data":usuarios
    }

#Crear
@app.post("/v1/usuarios/",tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }
#actualizar
@app.put("/v1/usuarios/",tags=['CRUD HTTP'])
async def actualiza_usuario(usuario:dict, user:str=Depends(validar_token)):
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
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id:int, user: str=Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == id:
            index = usuarios.index(usr)
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {user}",
                "status": "200",
                "usuario_eliminado": usr
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

    