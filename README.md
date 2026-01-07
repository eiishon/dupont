# dupont: Herramienta DLP de Código Abierto para Entornos PYME 
dupont es una herramienta de prevención de pérdida de datos (DLP) desarrollada en Python y diseñada específicamente para facilitar la ciberseguridad en pequeñas y medianas empresas (PYMEs) ya que se enfoca en mitigar los "data leaks" o fugas de datos accidentales causadas por configuraciones incorrectas o errores humanos.
Al integrarse con la infraestructura de Google Workspace, dupont actúa como un DLP en la nube para supervisar y proteger la información sensible en Gmail y Google Drive.

Características Principales
Monitoreo de Google Workspace: Escaneo automático de correos electrónicos y archivos en Drive mediante las APIs oficiales de Google.
Detección de Datos Sensibles: Identificación precisa de información personal (PII) mediante patrones de expresiones regulares (Regex) de alta eficiencia:
DNI y NIE (España).
Números de cuenta bancaria (IBAN).
Números de teléfono y tarjetas de crédito.
Direcciones de correo electrónico.

Autenticación Segura: Uso del estándar OAuth2 para acceder a los recursos sin comprometer las credenciales del usuario.

Gestión de Auditoría: Sistema de logging persistente que registra cada incidencia en el fichero dlp_system.log.

Arquitectura del Sistema

El proyecto sigue una arquitectura modular estricta para garantizar la escalabilidad y el mantenimiento:
dupont/auth/: Gestión de credenciales y flujo OAuth2.
dupont/scanner/: Módulo de adquisición de datos (Gmail y Drive).
dupont/analyzer/: Núcleo de detección y clasificación de patrones.
dupont/alerts/: Generación de informes, registros y notificaciones.
dupont/data/: Almacenamiento de datos anonimizados.
dupont/config/: Centralización de la configuración global (config.yaml).

 Instalación y Configuración
 Requisitos Previos
 Disponer de una cuenta en Google Cloud Platform.
 Tener instalado Anaconda (o un entorno Python 3.11+).Configuración del Entorno
 Desde el Anaconda Prompt, ejecute los siguientes comandos para preparar las dependencias:
 Bash
 conda create -n google-env python=3.11 -y
 conda install -c conda-forge google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 -y
 
Configuración de Google API
Para que la herramienta funcione, debe habilitar el acceso en su consola de Google Cloud:
Habilite las APIs de Gmail y Google Drive.
Configure la pantalla de consentimiento de OAuth.
Cree un ID de cliente de App de escritorio.
Descargue el archivo JSON, renombrelo como credenciales.json y guárdelo en dupont/auth/.
Aspectos Legales y Éticos (RGPD)
dupont ha sido diseñado bajo el principio de privacidad por diseño y responsabilidad proactiva.
Anonimización: La herramienta aplica técnicas de anonimización irreversibles para los datos detectados, eliminándolos del ámbito de aplicación estricto del RGPD para mayor comodidad en el tratamiento.
Control de Acceso: Implementa un modelo RBAC (Control de Acceso Basado en Roles) para asegurar que solo los administradores autorizados gestionen los incidentes.

Licencia
Este proyecto está bajo la licencia GNU Free Documentation License, Version 1.3.

Autor: Elena Ferrer Campos 
Institución: Universitat Oberta de Catalunya (UOC)
Repositorio: github.com/eiishon/dupont 
