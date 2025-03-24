from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configuração do Chrome (sem necessidade de baixar o ChromeDriver)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Para rodar sem abrir o navegador
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Criar o driver do Chrome automaticamente (Selenium Manager faz tudo!)
driver = webdriver.Chrome(options=chrome_options)

# URL da página da Martins Fontes
url = "https://www.martinsfontespaulista.com.br/buscar?q=Mang%C3%A1s&page=1&filter=discrete%3A652%3A1594&filter=discrete%3A652%3A6174&filter=discrete%3A652%3A2636&filter=discrete%3A652%3A3180&filter=discrete%3A652%3A264416&viewType=list&perPage=48"
driver.get(url)

# Esperar a página carregar completamente
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "line"))
)

time.sleep(5)

#Capturar o HTML    
html_source = driver.page_source
soup = BeautifulSoup(html_source, "html.parser")

# Encontrar o número da última página disponivel
try:
    time.sleep(10)
    pagination_element = soup.find("div", class_="text-list")  # Verifique no DevTools se a classe está correta
    if pagination_element:
        pages = pagination_element.find_all("button")  # Altere para "a" se necessário
        page_numbers = [p.text.strip() for p in pages if p.text.strip().isdigit()]
        total_pages = int(page_numbers[-1]) if page_numbers else 1
    else:
        total_pages = 1
except Exception as e:
    print(f"Erro ao encontrar a última página: {e}")
    total_pages = 1

print(f"Encontradas {total_pages} páginas para scraping.")