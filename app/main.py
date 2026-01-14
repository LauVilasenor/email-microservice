from fastapi import FastAPI

app = FastAPI(title="Microservicio de Correos")

@app.get("/")
def read_root():
    return {"mensaje": "¡Microservicio de correos funcionando!"}

@app.post("/enviar-correo")
def enviar_correo():
    return {
        "status": "success",
        "mensaje": "Correo enviado exitosamente (simulado)"
    }