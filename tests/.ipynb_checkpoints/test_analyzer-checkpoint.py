#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pytest
from analyzer import dlp_analyzer

def test_dni_detection():
    texto = "El usuario con DNI 12345678Z ha solicitado acceso."
    match = dlp_analyzer.dni_nie_regex.search(texto)
    assert match is not None
    assert "12345678Z" in match.group(0)

def test_num_detection():
    texto = "Mi número de teléfono es: 601234567"
    match = dlp_analyzer.phone_regex.search(texto)
    assert match is not None

def test_iban_detection():
    texto = "Transferencia a la cuenta ES1234567890123456789012"
    match = dlp_analyzer.iban_regex.search(texto)
    assert match is not None

def test_email_detection():
    texto = "Contacto: info@empresa.com"
    match = dlp_analyzer.email_regex.search(texto)
    assert match is not None

def test_no_sensitive_data():
    texto = "Este es un mensaje ordinario sin datos sensibles."
    assert dlp_analyzer.dni_nie_regex.search(texto) is None
    assert dlp_analyzer.email_regex.search(texto) is None
    assert dlp_analyzer.iban_regex.search(texto) is None
    assert dlp_analyzer.phone_regex.search(texto) is None

def test_all_sensitive_data():
    texto = (
        "Hola, mi DNI es 12345678Z "
        "Puedes escribirme a usuario@ejemplo.com "
        "o llamarme al 601234567 "
        "Mi cuenta es ES1234567890123456789012"
    )
    assert dlp_analyzer.dni_nie_regex.search(texto) is not None
    assert dlp_analyzer.email_regex.search(texto) is not None
    assert dlp_analyzer.phone_regex.search(texto) is not None
    assert dlp_analyzer.iban_regex.search(texto) is not None

def test_some_sensitive_data():
    texto = (
        "Hola, mi DNI es 12345678Z "
        "Puedes escribirme a mi direccion de correo "
        "o llamarme al 61234567 "
        "Mi cuenta es esta"
    )
    assert dlp_analyzer.dni_nie_regex.search(texto) is not None
    assert dlp_analyzer.email_regex.search(texto) is None
    assert dlp_analyzer.phone_regex.search(texto) is not None
    assert dlp_analyzer.iban_regex.search(texto) is None

def test_anonymization_logic():
    dni_falso = "12345678Z"
    anonimizado = dlp_analyzer.anonymize_dni_nie(dni_falso)
    assert "*" in anonimizado
    assert "123" not in anonimizado