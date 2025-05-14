from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import yt_dlp
import time
import os

# === CONFIGURAÇÕES ===
URL_CURSO = "https://web.dio.me/track/bradesco-java-cloud-native/course/introducao-banco-de-dados/learning/be90be08-cf35-45d0-a4d4-79b07fc25eb1?autoplay=1"
TEMPO_ESPERA = 5  # tempo entre etapas
PASTA_SAIDA = "videos"

# Cria pasta de saída se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

# === CONFIGURAR O NAVEGADOR ===
options = Options()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")  # Ative se quiser rodar sem abrir o navegador

service = Service(executable_path=r"C:\Users\ext.eduardo.nunes\OneDrive - BK Brasil\Área de Trabalho\Python\Baixador de videos automatico\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Acessa a URL do curso
driver.get(URL_CURSO)
time.sleep(TEMPO_ESPERA)

# === LOGIN MANUAL ===
input("🟡 Faça login na plataforma DIO e pressione Enter para continuar...")

# === LOOP DE DOWNLOAD ===
while True:
    try:
        print("🔎 Buscando iframe do vídeo...")
        time.sleep(TEMPO_ESPERA)

        # Pega o link do vídeo YouTube
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        src = iframe.get_attribute("src")
        if "youtube.com/embed/" not in src:
            print("⚠️ Vídeo não encontrado no formato esperado.")
            break

        video_id = src.split("/embed/")[1].split("?")[0]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"🎬 Link encontrado: {youtube_url}")

        # Verifica se o vídeo já foi baixado (baseado no ID)
        arquivo_existente = any(video_id in f for f in os.listdir(PASTA_SAIDA))
        if arquivo_existente:
            print("✅ Vídeo já baixado. Pulando...")
        else:
            # Baixa o vídeo com yt-dlp
            print("⬇️ Baixando vídeo...")
            ydl_opts = {
                'format': 'bv*[height<=1080]+ba/best',
                'outtmpl': f'{PASTA_SAIDA}/%(title)s [%(id)s].%(ext)s',
                'quiet': False
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            print("✅ Download concluído!")

        # Tenta clicar no botão "Próxima Aula"
        time.sleep(2)
        next_button = driver.find_element(By.CSS_SELECTOR, "button.sc-hSWFJi.eZqXgY")
        print("➡️ Indo para a próxima aula...")
        next_button.click()

    except NoSuchElementException:
        print("🛑 Fim do curso ou botão 'Próxima Aula' não encontrado.")
        break
    except Exception as e:
        print(f"❌ Erro: {e}")
        break

# === ENCERRAR ===
driver.quit()
print("✅ Processo finalizado.")
