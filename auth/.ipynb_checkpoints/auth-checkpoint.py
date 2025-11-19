#!/usr/bin/env python
# coding: utf-8

# In[9]:


from __future__ import print_function
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# SCOPES: Gmail + Drive
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

def google_auth():
    """
    Autentica al usuario mediante OAuth2 para Gmail y Drive.
    """
    creds = None
    base_path = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
    cred_path = os.path.join(base_path, 'credentials.json')
    token_path = os.path.join(base_path, 'token.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Construimos los servicios
    gmail_service = build('gmail', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return {"gmail": gmail_service, "drive": drive_service}

