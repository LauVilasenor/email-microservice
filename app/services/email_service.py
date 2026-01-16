import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import aiosmtplib
from app.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_name = settings.SMTP_FROM_NAME

    async def enviar_correo_con_adjunto(
        self,
        destinatarios: list,
        asunto: str,
        cuerpo: str, # Este es el texto que mandará el Back
        archivo_base64: str = None,
        nombre_archivo: str = "reporte.pdf"
    ) -> dict:
        try:
            mensaje = MIMEMultipart()
            mensaje["From"] = f"{self.from_name} <{self.smtp_user}>"
            mensaje["To"] = ", ".join(destinatarios)
            mensaje["Subject"] = asunto

            # --- AQUÍ CREAMOS EL DISEÑO BONITO (HTML) ---
            # He usado el color azul de tu barra lateral (#2c3e50 / #34495e)
            
            




            # --- DISEÑO MEJORADO: LOGO EN LA FRANJA AZUL ---
            html_template = f"""
            <html>
            <body style="margin: 0; padding: 0; font-family: sans-serif; background-color: #f4f7f6;">
                <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f4f7f6; padding: 20px;">
                    <tr>
                        <td align="center">
                            <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                                
                                <tr style="background-color: #1e3a8a;">
                                    <td style="padding: 20px;">
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                            <tr>
                                                <td align="left" style="vertical-align: middle;">
                                                    <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Iron Tigers - Sistema de Gestión</h1>
                                                </td>
                                                <td align="right" style="vertical-align: middle; padding-left: 15px;">
    <img src="https://github.com/LauVilasenor/email-microservice/blob/main/app/logo-iron-tigers.png?raw=true" 
         width="180" 
         style="display: block; border: 0; filter: drop-shadow(0px 8px 6px rgba(0,0,0,0.5));">
</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="padding: 40px; color: #333333; line-height: 1.6;">
                                        <h2 style="color: #1e3a8a; margin-top: 0;">Notificación de Reporte</h2>
                                        <p style="font-size: 16px;">{cuerpo}</p>
                                        <p style="font-size: 14px; color: #666666; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
                                            Este es un correo automático, por favor no respondas a esta dirección.
                                        </p>
                                    </td>
                                </tr>
                                
                                <tr style="background-color: #f8fafc;">
                                    <td align="center" style="padding: 15px; font-size: 11px; color: #94a3b8;">
                                        &copy; 2024 Iron Tigers | Departamento de TI
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            # Cambiamos "plain" por "html" para que Gmail entienda el diseño
            mensaje.attach(MIMEText(html_template, "html"))

            # Lógica del archivo adjunto (se queda igual)
            if archivo_base64:
                contenido_binario = base64.b64decode(archivo_base64)
                adjunto = MIMEApplication(contenido_binario)
                adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
                mensaje.attach(adjunto)

            await aiosmtplib.send(
                mensaje,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            return {"status": "success", "mensaje": "Correo con diseño enviado"}
            
        except Exception as e:
            return {"status": "error", "mensaje": str(e)}

email_service = EmailService()