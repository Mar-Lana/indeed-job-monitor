### (Optativa 3: Tópicos avanzados de Ingeniería del Software)
# 🔔 Indeed Job Monitor (Playwright + Email Alerts)

Un script automatizado en Python para monitorear ofertas de trabajo en **Indeed** en tiempo real. Utiliza **Playwright** para la navegación asíncrona, guarda el historial de empleos en formato JSON para evitar duplicados y envía notificaciones por correo electrónico (`smtplib`) cada vez que detecta una nueva publicación.

---

## 📌 Características

- **Scraping Asíncrono con Playwright:** Carga dinámicamente las tarjetas de empleo en Indeed evitando colgarse por peticiones de red o scripts de analíticas.
- **Alertas por Correo Electrónico:** Envío automático de notificaciones vía SMTP (Gmail) con el título, empresa y enlace directo a la postulación.
- **Control de Duplicados:** Almacenamiento local de identificadores de ofertas procesadas en `jobs_seen.json`.
- **Bucle Programado:** Ejecución continua cada 15 minutos.
- **Parada Controlada (Graceful Shutdown):** Salida limpia del programa al detectar un archivo bandera `STOP` en la carpeta raíz.

---

## 📁 Estructura del Proyecto

```text
indeed-job-monitor/
├── main.py              # Script principal con scraping, alertas y bucle
├── jobs_seen.json       # Historial JSON de ofertas ya procesadas
├── .env                 # Variables de entorno para credenciales
├── requirements.txt     # Dependencias de Python
└── README.md            # Documentación del proyecto
```

---

## 🛠️ Requisitos Previos
- Python 3.10+
- Una cuenta de Gmail con una Contraseña de Aplicación activada para el envío de correos vía SMTP.

---

## ⚙️ Instalación y Configuración
1. Clonar el repositorio y entrar a la carpeta:
```text
git clone [https://github.com/tu-usuario/indeed-job-monitor.git](https://github.com/tu-usuario/indeed-job-monitor.git)
cd indeed-job-monitor
```
2. Crear y activar el entorno virtual:
```text
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```
3. Instalar dependencias:
```text
pip install -r requirements.txt
playwright install chromium
```
5. Configurar las variables de entorno
Creá un archivo llamado .env en la raíz del proyecto con las siguientes variables:
```text
EMAIL_SENDER="tu_correo@gmail.com"
EMAIL_PASSWORD="xxxx xxxx xxxx xxxx"   # Contraseña de aplicación de Google
EMAIL_RECEIVER="tu_correo_destino@gmail.com"
```

---

## 🚀 Uso del Monitor
# Ejecución estándar en consola
Para iniciar el monitor en primer plano:
```text
python main.py
```
# Ejecución en segundo plano (Windows)
Si querés dejarlo corriendo en segundo plano sin mantener abierta la consola:
```text
Start-Process pythonw main.py
```

---

## 🛑 Cómo detener el programa
Para detener el ciclo de 15 minutos de forma limpia sin matar forzadamente el proceso:
1. Creá un archivo llamado STOP (sin extensión) en la raíz del proyecto (en la terminal):
```text
New-Item STOP
```
2. El script detectará la presencia del archivo en menos de un segundo, detendrá la ejecución, eliminará el archivo STOP y finalizará correctamente.

---

