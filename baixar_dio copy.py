from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import yt_dlp

# === CONFIGURAÇÕES ===
URL_DIO = "https://web.dio.me/track/bradesco-java-cloud-native/course/introducao-banco-de-dados/learning/be90be08-cf35-45d0-a4d4-79b07fc25eb1?autoplay=1"
TEMPO_ESPERA = 5  # segundos para esperar cada página carregar

# === CONFIGURAR O NAVEGADOR ===
options = Options()

options.add_argument("--window-size=1920,1080")

service = Service(executable_path=r"C:\Users\ext.eduardo.nunes\OneDrive - BK Brasil\Área de Trabalho\Python\Baixador de videos automatico\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.dio.me/track/bradesco-java-cloud-native/course/introducao-banco-de-dados/learning/be90be08-cf35-45d0-a4d4-79b07fc25eb1?autoplay=1")
time.sleep(TEMPO_ESPERA)

# === LOGIN MANUAL SE NECESSÁRIO ===
input("Faça login na plataforma DIO manualmente e pressione Enter...")

# === RASTREAR LINKS DOS VÍDEOS ===
iframe_elements = driver.find_elements(By.TAG_NAME, "iframe")

video_links = []
for iframe in iframe_elements:
    src = iframe.get_attribute("src")
    if "youtube.com/embed/" in src:
        video_id = src.split("/embed/")[1].split("?")[0]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        video_links.append(youtube_url)

driver.quit()

print(f"{len(video_links)} vídeos encontrados.")

# === BAIXAR OS VÍDEOS COM yt-dlp ===
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'videos/%(title)s.%(ext)s',
}

for link in video_links:
    print(f"Baixando {link}...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
