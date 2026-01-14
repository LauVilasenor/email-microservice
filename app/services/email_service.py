import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class EmailService:
    """Servicio para enviar correos electrónicos"""
    
    def __init__(self):
        # Leer configuración del archivo .env
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_name = os.getenv("SMTP_FROM_NAME")
    
    async def enviar_correo_simple(
        self,
        destinatario: str,
        asunto: str,
        cuerpo: str
    ) -> dict:
        """
        Envía un correo de texto simple
        
        Args:
            destinatario: Email del destinatario
            asunto: Asunto del correo
            cuerpo: Contenido del correo (texto plano)
            
        Returns:
            dict con status y mensaje
        """
        try:
            # Crear el mensaje
            mensaje = MIMEMultipart()
            mensaje["From"] = f"{self.from_name} <{self.smtp_user}>"
            mensaje["To"] = destinatario
            mensaje["Subject"] = asunto
            
            # Agregar el cuerpo del mensaje
            mensaje.attach(MIMEText(cuerpo, "plain"))
            
            # Enviar el correo
            await aiosmtplib.send(
                mensaje,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            return {
                "status": "success",
                "mensaje": f"Correo enviado exitosamente a {destinatario}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"Error al enviar correo: {str(e)}"
            }

# Crear una instancia global del servicio
email_service = EmailService()