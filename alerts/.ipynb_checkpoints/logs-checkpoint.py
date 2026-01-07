#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging
import base64
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def setup_logger():
    """Configura el logger para auditoría en archivo."""
    logger = logging.getLogger('DLPSystem')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_file = 'alerts/dlp_system.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def run_alerts(service, destinatario, csv_path, threshold=20):
    logger = setup_logger()
    log_file_path = 'alerts/dlp_system.log'
    
    # 1. Registro inicial en el log
    logger.info(f"Iniciando análisis de alertas sobre: {csv_path}")
    
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            num_incidencias = len(df)
            
            # 2. Crear el diccionario de conteo por tipo (dni, email, etc.)
            if 'dtype' in df.columns:
                conteo_tipos = df['dtype'].value_counts().to_dict()
            else:
                conteo_tipos = {"desconocido": num_incidencias}
        else:
            num_incidencias = 0
            conteo_tipos = {}

        # 3. Evaluar umbral
        if num_incidencias >= threshold:
            # Log de alertas encontradas con el diccionario
            logger.info(f"Alertas encontradas: {conteo_tipos}. Procediendo a enviar correo...")
            
            # Log de resumen de incidencias 
            logger.info(f"ALERTA: {num_incidencias} incidencias detectadas (Umbral: {threshold})")

            # Preparar el correo (Multipart para adjuntar el LOG)
            mensaje = MIMEMultipart()
            mensaje['to'] = destinatario
            mensaje['from'] = 'me'
            subject = "Alerta DLP: Resumen de datos sensibles"
            mensaje['subject'] = subject

            # Cuerpo del mensaje con el desglose
            lineas_detalles = [f"- {k}: {v}" for k, v in conteo_tipos.items()]
            detalles_str = "\n".join(lineas_detalles)
            
            cuerpo = (f"Resumen de datos sensibles detectados:\n\n"
                      f"{detalles_str}\n\n"
                      f"Total: {num_incidencias} incidencias.\n"
                      f"Se adjunta el archivo de auditoría log.")
            
            mensaje.attach(MIMEText(cuerpo, 'plain'))

            # 4. Adjuntar el archivo LOG
            if os.path.exists(log_file_path):
                with open(log_file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= dlp_system.log")
                mensaje.attach(part)

            # Enviar
            raw_message = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()
            service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
            
            # 5. Log final de confirmación de envío
            logger.info(f"Correo enviado a {destinatario}: {subject}")
            print(f"Alerta y LOG enviados con éxito a {destinatario}")
            
        else:
            logger.info(f"Análisis finalizado: Total de incidencias ({num_incidencias}) por debajo del umbral.")
            print(f"Sin alertas (Umbral no alcanzado).")

    except Exception as e:
        logger.error(f"Error en el sistema de alertas: {e}", exc_info=True)
        print(f"Error: {e}")