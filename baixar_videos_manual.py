from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import subprocess

# Configurações
EMAIL = "eduardofrancisco110@gmail.com"
SENHA = "@Edu460006"
LOGIN_URL = "https://auth.dio.me/realms/master/protocol/openid-connect/auth?client_id=spa-core-client&redirect_uri=https%3A%2F%2Fweb.dio.me%2Ftrack%2Fbradesco-java-cloud-native%2Fcourse%2Fintroducao-banco-de-dados%2Flearning%2F65db3105-7f66-4960-bb05-2ddba629e2eb%3Fautoplay%3D1&response_mode=fragment&response_type=code&scope=openid"
CURSO_URL = "https://web.dio.me/track/bradesco-java-cloud-native/course/introducao-a-banco-de-dados-relacionais-sql/learning/bdaaa5d8-2d86-49e6-b166-ae890d0112b0?autoplay=1"

PASTA_VIDEOS = os.path.join(os.getcwd(), "videos")
os.makedirs(PASTA_VIDEOS, exist_ok=True)

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

contador = 1
modulo_atual = ""
ultima_url = ""

def login():
    driver.get(LOGIN_URL)
    time.sleep(3)
    driver.find_element(By.ID, "username").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(SENHA)
    driver.find_element(By.ID, "password").submit()
    time.sleep(5)

def get_iframe_url():
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        return iframe.get_attribute("src")
    except:
        return ""

def get_module_name():
    try:
        span = driver.find_element(By.CSS_SELECTOR, "span.sc-esYiGF.dscpfF")
        nome = span.text.strip()
        return "".join(c for c in nome if c.isalnum() or c in " _-")
    except:
        return "Modulo_Desconhecido"

def criar_pasta_modulo(nome):
    pasta = os.path.join(PASTA_VIDEOS, nome)
    os.makedirs(pasta, exist_ok=True)
    return pasta

def baixar_video(url, pasta, num):
    if not url or url.strip() == "":
        print("❌ URL inválida, pulando...")
        return False

    nome = os.path.join(pasta, f"{num:02d} - %(title)s.%(ext)s")
    print(f"⬇️ Baixando vídeo {num}: {url}")
    comando = ["yt-dlp", "-o", nome, url]
    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode != 0:
        print("❌ Erro no download:", resultado.stderr)
        return False

    print("✅ Download finalizado.")
    return True

def clicar_botao_proximo():
    try:
        botoes = driver.find_elements(By.CLASS_NAME, "sc-hSWFJi")
        for btn in botoes:
            svg = btn.find_element(By.TAG_NAME, "svg")
            path = svg.find_element(By.TAG_NAME, "path").get_attribute("d")
            if path.startswith("M285.476"):  # Botão próximo
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                return True
    except Exception as e:
        print(f"Erro ao clicar em próximo: {e}")
    return False

def obter_botao_avancar():
    botoes = driver.find_elements(By.CLASS_NAME, "sc-hSWFJi")
    for btn in botoes:
        try:
            svg = btn.find_element(By.TAG_NAME, "svg")
            path = svg.find_element(By.TAG_NAME, "path").get_attribute("d")
            if path.startswith("M285.476"):  # padrão do botão "próximo"
                return btn
        except:
            continue
    return None

def esperar_url_mudar(url_antiga, timeout=20):
    for _ in range(timeout):
        time.sleep(1)
        url_nova = get_iframe_url()
        if url_nova != url_antiga and url_nova != "":
            return url_nova
    return None
def pegar_url_iframe():
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        return iframe.get_attribute("src")
    except Exception as e:
        print("Erro ao pegar URL do iframe:", e)
        return ""

def main():
    login()
    driver.get(CURSO_URL)
    time.sleep(5)

    modulo_atual = ""
    pasta_modulo = ""
    contador = 1
    ultima_url = ""

    while True:
        # Detecta se mudou de módulo para criar nova pasta e resetar contador
        nome_modulo = get_module_name()
        if nome_modulo != modulo_atual:
            modulo_atual = nome_modulo
            pasta_modulo = os.path.join(PASTA_VIDEOS, modulo_atual)
            os.makedirs(pasta_modulo, exist_ok=True)
            contador = 1
            print(f"\n📁 Novo módulo: {modulo_atual}")

        # Pega URL do vídeo atual
        url_video = pegar_url_iframe()
        if not url_video:
            print("URL do vídeo vazia, aguardando...")
            time.sleep(2)
            continue

        # Se for o mesmo vídeo que já baixamos, aguarde o próximo vídeo carregar
        if url_video == ultima_url:
            print("⏳ Aguardando mudança de vídeo...")
            time.sleep(2)
            continue

        # Baixa o vídeo
        saida = os.path.join(pasta_modulo, f"{contador:02d} - %(title)s.%(ext)s")
        print(f"⬇️ Baixando vídeo #{contador}: {url_video}")
        proc = subprocess.run(["yt-dlp", "-o", saida, url_video])
        if proc.returncode != 0:
            print("❌ Erro no download. Tentando próximo vídeo.")
        else:
            print("✅ Download concluído.")

        ultima_url = url_video
        contador += 1

        # Clica no botão próximo, aguarda o próximo vídeo carregar
        btn_proximo = obter_botao_avancar()
        if not btn_proximo:
            print("✅ Fim do módulo detectado (botão próximo não encontrado).")
            break

        driver.execute_script("arguments[0].scrollIntoView(true);", btn_proximo)
        btn_proximo.click()

        # Espera a URL do iframe mudar para o próximo vídeo
        for _ in range(20):
            time.sleep(1)
            nova_url = pegar_url_iframe()
            if nova_url != ultima_url and nova_url:
                break
        else:
            print("❗ Tempo esgotado esperando o próximo vídeo carregar.")
            break

    print("🏁 Finalizado.")
    driver.quit()

if __name__ == "__main__":
    main()