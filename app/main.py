from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.email_service import email_service

app = FastAPI(
    title="Microservicio de Correos - Iron Tigers",
    description="API para envio de correos electrónicos",
    version="1.0.0"
)
class EmailRequest(BaseModel):
    destinatario: EmailStr
    asunto: str
    cuerpo: str

@app.get("/")
def read_root():
    return {
        "mensaje": "!Microservicios de correos funcionando!",
        "version": "1.0.0",
        "endpoints": [
            "GET /",
            "POST /enviar-correo",
            "GET /docs"
       ]
    }

@app.post("/enviar-correo")
async def enviar_correo(email_request: EmailRequest):

    try:
       
        resultado = await email_service.enviar_correo_simple(
            destinatario=email_request.destinatario,
            asunto=email_request.asunto,
            cuerpo=email_request.cuerpo
        )
        
        if resultado["status"] == "success":
            return {
                "success": True,
                "mensaje": resultado["mensaje"]
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=resultado["mensaje"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar correo: {str(e)}"
        )

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "email-microservice"
    }