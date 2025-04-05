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

# URL da página da Panini
url = "https://www.lojanewpop.com.br/mangas?sort=mais_vendidos&pagina=10"
driver.get(url)

# Esperar até os produtos carregarem completamente (máx. 10 segundos)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "info-produto"))
    )
except:
    print("Os produtos não foram carregados completamente.")

# Capturar o HTML da página depois do carregamento dinâmico
html_source = driver.page_source

# Fechar o navegador
driver.quit()

# Usar BeautifulSoup para extrair informações
soup = BeautifulSoup(html_source, "html.parser")

# Encontrar os produtos na página
mangas = soup.find_all("div", class_="info-produto")

for manga in mangas:
 #encontrar o título do manga
    title = manga.find("a", class_="nome-produto cor-secundaria")
    title_text = title.text.strip() if title else "Título não encontrado"

    # Encontrar o preço promocional (se houver)
    special_price = manga.find("strong", class_="preco-promocional cor-principal titulo")
    special_price_text = special_price.text.strip() if special_price else None

    # Encontrar o preço original
    old_price_element = manga.find("s", class_="preco-venda titulo")
    old_price_text = old_price_element.text.strip() if old_price_element else None

    # Se o produto NÃO tem promoção, o preço original é o único preço mostrado
    if not old_price_text:
        old_price_text = special_price_text  # Definir como o único preço disponível
        special_price_text = None  # Definir como None, pois não há desconto

    # Disponibilidade do Produto
    indisponivel = manga.find("a", class_="botao avise-me-list-btn btn-block avise-me-pop-cadastro")
    indisponivel_text = indisponivel.text.strip() if indisponivel else "Disponível"

    

    print(f"{title_text} - preco original: {old_price_text} - desconto: {special_price_text} - Disponibilidade: {indisponivel_text}")