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
optativa-3/
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
3. 
