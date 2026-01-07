#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
from base64 import urlsafe_b64decode
from email import message_from_bytes


# Escanear todos los archivos de gmail

def scan_gmail(gmail_service, batch_size=200):

    correos = []
    next_page_token = None

    while True:
        results = gmail_service.users().messages().list(
            userId="me",
            maxResults=batch_size,
            pageToken=next_page_token
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            break

        # Obtener contenido de cada correo
        for msg in messages:
            msg_id = msg["id"]

            raw_msg = gmail_service.users().messages().get(
                userId="me",
                id=msg_id,
                format="raw"
            ).execute()

            raw_bytes = urlsafe_b64decode(raw_msg["raw"])
            email_message = message_from_bytes(raw_bytes)

            cuerpo = _extract_email_text(email_message)

            correos.append({
                "message_id": msg_id,
                "snippet": raw_msg.get("snippet", ""),
                "text": cuerpo
            })

        # Pasar a la siguiente página
        next_page_token = results.get("nextPageToken")
        if not next_page_token:
            break

    return correos



# Extraer texto del correo

def _extract_email_text(email_message):

    parts = []

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":
                try:
                    parts.append(part.get_payload(decode=True).decode("utf-8", errors="ignore"))
                except:
                    pass
    else:
        try:
            parts.append(email_message.get_payload(decode=True).decode("utf-8", errors="ignore"))
        except:
            pass

    return "\n".join(parts)

