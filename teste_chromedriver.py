from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# Não rode em headless
# options.add_argument("--headless")
options.add_argument("--start-maximized")

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    input("Se o navegador abriu, pressione Enter para fechar...")
    driver.quit()
except Exception as e:
    print("Erro ao iniciar o ChromeDriver:", e)
