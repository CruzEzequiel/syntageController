import os
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from controllers import syntage_data_controller
from middlewares.authMiddleware import validate_access_token

load_dotenv()

app = FastAPI(
    dependencies=[Depends(validate_access_token)] #asegura que siempre se valide el token de acceso
)

# Configuración de CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

print(allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Usar los orígenes desde el archivo .env
    allow_credentials=True,
    allow_methods=["GET", "POST","DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

# Middleware personalizado para verificar el token de acceso


app.include_router(syntage_data_controller.router)
