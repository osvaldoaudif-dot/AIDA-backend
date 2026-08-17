from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import json
import os

app = FastAPI()

ARCHIVO_DATOS = "usuarios.json"

# Inicializar o cargar la base de datos local JSON
if not os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump({"Usuario 1": "Sin registrar", "Usuario 2": "Sin registrar"}, f)

class RegistroUsuario(BaseModel):
    perfil: str
    nombre: str

@app.post("/guardar-nombre")
def recibir_nombre(datos: RegistroUsuario):
    # Cargar datos existentes
    with open(ARCHIVO_DATOS, "r") as f:
        db = json.load(f)
    
    # Guardar nuevo dato
    db[datos.perfil] = datos.nombre
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(db, f)

    print("\n" + "="*40)
    print(f" [!] REGISTRO GUARDADO PERMANENTEMENTE")
    print(f"     Perfil: {datos.perfil}")
    print(f"     Nombre: {datos.nombre}")
    print("="*40 + "\n")
    
    return {"status": "exito", "mensaje": f"{datos.perfil} guardado como '{datos.nombre}'"}

@app.get("/obtener-usuarios")
def obtener_usuarios():
    with open(ARCHIVO_DATOS, "r") as f:
        db = json.load(f)
    return db

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)