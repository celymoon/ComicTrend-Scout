import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configuração do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Criar o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# URL da página inicial da Panini
url = "https://panini.com.br/planet-manga?product_list_order=ratings_summary"
driver.get(url)

# Esperar a página carregar completamente
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
)

time.sleep(5)

# Capturar o HTML
html_source = driver.page_source
soup = BeautifulSoup(html_source, "html.parser")

# ENCONTRAR O NÚMERO DA ÚLTIMA PÁGINA
try:
    ultima_pagina_element = soup.find("a", class_="page last")
    if ultima_pagina_element:
        # Pegamos todos os <span> dentro do link
        spans = ultima_pagina_element.find_all("span")
        total_paginas = int(spans[-1].text.strip())  # Pegamos o último <span>, que tem o número correto
    else:
        total_paginas = 1
except Exception as e:
    print(f"⚠️ Erro ao encontrar a última página: {e}")
    total_paginas = 1

print(f"🔍 Encontradas {total_paginas} páginas para scraping.")

# 🔹 Criar o arquivo CSV e escrever os cabeçalhos
with open("mangas_panini.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Título", "Preço Original", "Desconto", "Disponibilidade", "Pré-venda"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 🔄 LOOP PARA NAVEGAR POR TODAS AS PÁGINAS AUTOMATICAMENTE
    for pagina in range(1, total_paginas + 1):
        url = f"https://panini.com.br/planet-manga?p={pagina}&product_list_order=ratings_summary"
        print(f"\n📄 Scraping da Página {pagina}...")
        driver.get(url)

        # Esperar os produtos carregarem completamente
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
            )
        except:
            print(f" Produtos não carregaram na página {pagina}. Pulando...")
            continue

        # Capturar o HTML da página carregada
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")

        # Encontrar os produtos na página
        mangas = soup.find_all("li", class_="item product product-item")

        for manga in mangas:
            title = manga.find("a", class_="product-item-link")
            title_text = title.text.strip() if title else "Título não encontrado"

            
        # Encontrar preço com desconto (special-price → span.price)
            special_price = manga.find("span", class_="special-price")
            special_price_text = special_price.find("span", class_="price").text.strip() if special_price and special_price.find("span", class_="price") else None

        # Encontrar preço original (old-price → span.price)
            original_price = manga.find("span", class_="price-wrapper")
            original_price_text = original_price.find("span", class_="price").text.strip() if original_price and original_price.find("span", class_="price") else None
            old_price = manga.find("span", class_="old-price")
            old_price_text = old_price.find("span", class_="price").text.strip() if old_price and old_price.find("span", class_="price") else original_price_text
       
        #encontrar prevenda
            prevenda = manga.find("div", class_="amlabel-text")
            prevenda_text = prevenda.text.strip() if prevenda else None
        #encontrar disponibilidade
            status = manga.find("a", class_="bt-stock-unavailable")
            status_text = status.text.strip() if status else "Disponível"

            print(f"{title_text}, {old_price_text}, {special_price_text}, {status_text}, {prevenda_text}")

            # **Salvar os dados no CSV**
            writer.writerow({
                "Título": title_text,
                "Preço Original": old_price_text if old_price_text else "Não disponível",
                "Desconto": special_price_text if special_price_text else "Sem desconto",
                "Disponibilidade": status_text if status_text else "Disponível",
                "Pré-venda": prevenda_text if prevenda_text else "Não"
            })

# Fechar o navegador depois que tudo terminou
driver.quit()

print("\n✅ Dados salvos em 'mangas_panini.csv' com sucesso!")
