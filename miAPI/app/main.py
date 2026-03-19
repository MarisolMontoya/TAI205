# 1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios

# 2. Inicialización APP/Instancia de servidor
app=FastAPI(
    title='Mi Primer API',
    description="Marisol Montoya Botello",
    version='1.0.0'
    )                  #para personalizar
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
