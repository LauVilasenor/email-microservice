from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.services.email_service import email_service
app = FastAPI(
    title="Microservicio de Correos - Iron Tigers",
    description="API para envio de correos electrónicos",
    version="1.0.0"
)
class EmailRequest(BaseModel):
    destinatarios: List[EmailStr]  
    asunto: str
    cuerpo: str
    archivo_base64: Optional[str] = None  
    nombre_archivo: Optional[str] = None  
    
    class Config:
        json_schema_extra = {
            "example": {
                "destinatarios": [
                    "ejemplo1@gmail.com",
                    "ejemplo2@gmail.com"
                ],
                "asunto": "Reporte de Asistencias - Semana 03",
                "cuerpo": "Adjunto encontrarás el reporte de asistencias de la semana.",
                "archivo_base64": None,
                "nombre_archivo": "Reporte_Asistencias.xlsx"
            }
        }

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
       
        resultado = await email_service.enviar_correo_con_adjunto(
            destinatarios=email_request.destinatarios, 
            archivo_base64=email_request.archivo_base64,
            asunto=email_request.asunto,
            cuerpo=email_request.cuerpo,
            nombre_archivo=email_request.nombre_archivo 
        )
        
        if resultado["status"] == "success":
            return {
                "success": True,
                "mensaje": resultado["mensaje"],
                "enviados": resultado.get("enviados", []),
                "errores": resultado.get("errores", [])
                
            }
        else:
            raise HTTPException(
                status_code=500,
                detail={
                "mensaje": resultado["mensaje"],
                "enviados": resultado.get("enviados", []),
                "errores": resultado.get("errores", [])
        }
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