#!/usr/bin/env python
# coding: utf-8

# In[9]:


import re
import csv
import random
import os

# Regex

dni_nie_regex = re.compile(r'\b([XYZxyz]?\s?\d{7,8}[A-Za-z])\b')

email_regex = re.compile(r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b')

phone_regex = re.compile(r'(\+34\s?)?(\d[\d\s-]{8,})')

iban_regex = re.compile(r'\bES\d{22}\b')

name_regex = re.compile(
    r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\b'
)

# Anonimizadores según 

used_fake_names = set()
used_fake_phones = set()
used_fake_ibans = set()


def anonymize_dni_nie(value):
    numbers = re.findall(r'\d', value)
    if len(numbers) != 8:
        return value
    keep = numbers[3:7]
    return "***" + "".join(keep) + "*"


def anonymize_email(user, domain):
    domain_name, domain_tld = domain.split('.', 1)
    new_user = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=len(user)))
    new_domain = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=len(domain_name)))
    return f"{new_user}@{new_domain}.{domain_tld}"


def anonymize_phone(number):
    while True:
        new_number = ''.join(random.choice("0123456789") for _ in range(len(number)))
        if new_number not in used_fake_phones:
            used_fake_phones.add(new_number)
            return new_number


def anonymize_iban(iban):
    while True:
        new_iban = "ES" + "".join(random.choice("0123456789") for _ in range(22))
        if new_iban not in used_fake_ibans:
            used_fake_ibans.add(new_iban)
            return new_iban


def anonymize_name():
    num1, num2, num3 = random.randint(1000,9999), random.randint(1000,9999), random.randint(1000,9999)
    return f"Anon{num1} Doe{num2} Dupont{num3}"


# --------------------------
#  EXTRACCIÓN PRINCIPAL
# --------------------------

def extract_sensitive_data(messages):
    """
    messages: lista de strings o diccionarios de Gmail.
    Si es diccionario, se extrae 'text'.
    """
    sensitive_items = []

    for i, msg in enumerate(messages):
        if isinstance(msg, dict):
            text = msg.get("text", "")
        else:
            text = str(msg)

        # DNI / NIE
        for match in dni_nie_regex.finditer(text):
            full = match.group(0)
            dtype = "nie" if full[0].upper() in ["X","Y","Z"] else "dni"
            sensitive_items.append((dtype, anonymize_dni_nie(full)))

        # Email
        for user, domain in email_regex.findall(text):
            sensitive_items.append(("email", anonymize_email(user, domain)))

        # Teléfono
        for _, number in phone_regex.findall(text):
            sensitive_items.append(("numero", anonymize_phone(number)))

        # IBAN
        for iban in iban_regex.findall(text):
            sensitive_items.append(("iban", anonymize_iban(iban)))

        # Nombres
        for n1, n2, n3 in name_regex.findall(text):
            full_name = f"{n1} {n2} {n3}"
            sensitive_items.append(("nombre", anonymize_name()))

    # Generar CSV
    output_path = "data/sensitive_data.csv"
    os.makedirs("data", exist_ok=True)

    try:
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["dtype", "adata"])
            for dtype, masked in sensitive_items:
                writer.writerow([dtype, masked])
    except Exception as e:
        print(f"Error al escribir el CSV: {e}")
        return None

    return output_path





# In[ ]:




