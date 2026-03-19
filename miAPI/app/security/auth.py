from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import status,HTTPException,Depends
import secrets

# Seguridad HTTP BASIC
seguridad=HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth=secrets.compare_digest(credenciales.username,"marisolmontoya")
    passAuth=secrets.compare_digest(credenciales.password,"123456")

    if not(userAuth and passAuth ):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas."
        )
    return credenciales.username
