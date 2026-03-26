# 1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

# 2. Inicialización APP/Instancia de servidor
app=FastAPI(
    title='Mi Primer API',
    description="Marisol Montoya Botello",
    version='1.0.0'
    )                  #para personalizar
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
