from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import subprocess

# ====== CONFIGURAÇÕES ======
EMAIL = "eduardofrancisco110@gmail.com"
SENHA = "@Edu460006"

LOGIN_URL = "https://web.dio.me/sign-in"
CURSO_URL = "https://web.dio.me/track/bradesco-java-cloud-native/course/introducao-banco-de-dados/learning/65db3105-7f66-4960-bb05-2ddba629e2eb?autoplay=1"

PASTA_VIDEOS = os.path.join(os.getcwd(), "videos")
os.makedirs(PASTA_VIDEOS, exist_ok=True)

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Opcional
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

# ====== FUNÇÕES ======

def login():
    driver.get(LOGIN_URL)
    
    # Espera os campos aparecerem
    campo_email = wait.until(EC.presence_of_element_located((By.ID, "email")))
    campo_senha = driver.find_element(By.ID, "password")

    campo_email.send_keys(EMAIL)
    campo_senha.send_keys(SENHA + Keys.RETURN)

    # Espera ser redirecionado após o login
    wait.until(lambda d: "dio.me" in d.current_url)
    time.sleep(3)

def pegar_url_iframe():
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        return iframe.get_attribute("src")
    except:
        return None

def baixar_video(video_url):
    print(f"\n⬇️  Baixando: {video_url}")
    comando = [
        "yt-dlp",
        "-o", os.path.join(PASTA_VIDEOS, "%(title)s.%(ext)s"),
        video_url
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode != 0:
        print("❌ Erro no download:", resultado.stderr)
        return False
    print("✅ Download finalizado!")
    return True

def clicar_proximo(url_atual):
    try:
        botoes = driver.find_elements(By.CLASS_NAME, "sc-hSWFJi")
        if len(botoes) < 2:
            return None

        botao_proximo = botoes[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
        time.sleep(1)
        botao_proximo.click()
        print("➡️ Clicou em 'Próximo'.")

        # Aguarda a mudança da URL do iframe
        timeout = 20
        inicio = time.time()
        while time.time() - inicio < timeout:
            nova_url = pegar_url_iframe()
            if nova_url and nova_url != url_atual:
                return nova_url
            time.sleep(1)
        return None
    except Exception as e:
        print("❌ Erro ao clicar em próximo:", e)
        return None

def main():
    login()
    driver.get(CURSO_URL)
    time.sleep(5)

    url_atual = pegar_url_iframe()
    numero = 1

    while url_atual:
        print(f"\n🎬 Aula {numero}")
        if not baixar_video(url_atual):
            break

        nova_url = clicar_proximo(url_atual)
        if not nova_url:
            print("🏁 Fim das aulas ou erro ao avançar.")
            break

        url_atual = nova_url
        numero += 1

    driver.quit()
    print("\n✅ Todos os vídeos foram baixados.")

if __name__ == "__main__":
    main()
