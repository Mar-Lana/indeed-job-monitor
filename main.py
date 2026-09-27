import asyncio
import json
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

# ================== CONFIGURACIÓN ==================
SEARCH_URL = "https://ar.indeed.com/jobs?q=analista+programador&l=&from=searchOnHP&vjk=9461472c05844952"

# Archivo donde se guardan las ofertas ya vistas
SEEN_FILE = Path("jobs_seen.json")

# Configuración de email (Gmail recomendado)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")          # tu correo
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")      # contraseña de aplicación
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")      # a dónde quieres recibir las alertas

# ===================================================

# Intervalo en segundos (15 minutos = 15 * 60 = 900 segundos)
INTERVAL_SECONDS = 15 * 60

# Archivo bandera para detener la ejecución
STOP_FILE = Path("STOP")

def load_seen_jobs():
    if SEEN_FILE.exists():
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_seen_jobs(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)

def send_email(new_jobs):
    if not new_jobs:
        return

    subject = f"🔔 {len(new_jobs)} nueva(s) oferta(s) de trabajo encontrada(s)"

    body = "Se encontraron las siguientes ofertas nuevas:\n\n"
    for job in new_jobs:
        body += f"📌 {job['title']}\n"
        body += f"   Empresa: {job['company']}\n"
        body += f"   Link: {job['link']}\n\n"

    body += "\n— Job Monitor con Playwright"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Correo enviado con {len(new_jobs)} oferta(s)")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")

async def scrape_jobs():
    seen = load_seen_jobs()
    new_jobs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("🔍 Buscando ofertas...")
        await page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=60000)

        try:
            await page.wait_for_selector("div.job_seen_beacon, td.resultContent, div.cardOutline", timeout=15000)
        except Exception:
            print("⚠️ No se detectaron tarjetas a tiempo o la página solicitó verificación.")

        job_cards = await page.query_selector_all("div.job_seen_beacon, td.resultContent, div.cardOutline")
        print(f"📊 Tarjetas encontradas en el DOM: {len(job_cards)}")

        for card in job_cards:
            try:
                title_elem = await card.query_selector("h2.jobTitle a, a[data-jk], a.jxf413")
                company_elem = await card.query_selector("[data-testid='company-name'], span.companyName, div.company_location")

                if not title_elem:
                    continue

                title = (await title_elem.inner_text()).strip()
                link = await title_elem.get_attribute("href")

                if not link:
                    continue

                company = (await company_elem.inner_text()).strip() if company_elem else "No especificada"

                if link.startswith("/"):
                    link = "https://ar.indeed.com" + link

                job_id = link
                if "jk=" in link:
                    job_id = link.split("jk=")[1].split("&")[0]

                if job_id not in seen:
                    new_jobs.append({
                        "title": title,
                        "company": company,
                        "link": link
                    })
                    seen.add(job_id)

            except Exception as e:
                print(f"Error procesando una oferta: {e}")
                continue

        await browser.close()

    save_seen_jobs(seen)
    return new_jobs

async def main():
    print("🚀 Iniciando el monitor de empleos en bucle (cada 15 minutos)...")
    print("💡 Para detener el script de forma limpia, creá un archivo llamado 'STOP' en esta carpeta.")

    while True:
        # 1. Comprobación antes de ejecutar la tarea
        if STOP_FILE.exists():
            print("🛑 Archivo 'STOP' detectado. Finalizando el programa de forma limpia...")
            try:
                STOP_FILE.unlink()  # Elimina el archivo STOP para no interferir en futuras ejecuciones
            except Exception:
                pass
            break

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{now}] 🔄 Ejecutando búsqueda de ofertas...")

        try:
            new_jobs = await scrape_jobs()

            if new_jobs:
                print(f"🎉 Se encontraron {len(new_jobs)} oferta(s) nueva(s)")
                for job in new_jobs:
                    print(f"   - {job['title']} | {job['company']}")
                send_email(new_jobs)
            else:
                print("😴 No hay ofertas nuevas por ahora")

        except Exception as e:
            print(f"❌ Error durante el scraping: {e}")

        print("⏳ Esperando 15 minutos para la próxima revisión...")

        # 2. Espera interactiva: revisa la existencia de STOP cada 1 segundo durante los 15 minutos
        for _ in range(INTERVAL_SECONDS):
            if STOP_FILE.exists():
                break
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())