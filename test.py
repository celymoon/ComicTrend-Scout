import os
import csv
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

# Criar o driver do Chrome automaticamente
driver = webdriver.Chrome(options=chrome_options)

# URL da página da Panini
url = "https://panini.com.br/planet-manga?gad_source=1&p=4"
driver.get(url)

# Esperar até os produtos carregarem completamente (máx. 10 segundos)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
    )
except:
    print("Os produtos não foram carregados completamente.")

# Capturar o HTML da página depois do carregamento dinâmico
html_source = driver.page_source

# Usar BeautifulSoup para extrair informações
soup = BeautifulSoup(html_source, "html.parser")

# Encontrar os produtos na página
mangas = soup.find_all("li", class_="item product product-item")

# Criar o arquivo CSV e escrever os cabeçalhos
csv_path = os.path.join("Data", "mangas_panini.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Título", "Preço Original", "Desconto"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for manga in mangas:
        # Encontrar título
        title = manga.find("a", class_="product-item-link")
        title_text = title.text.strip() if title else "Título não encontrado"
        manga_url = title['href'] if title else None


        # Encontrar preço com desconto (special-price → span.price)
        special_price = manga.find("span", class_="special-price")
        special_price_text = special_price.find("span", class_="price").text.strip() if special_price else None

        # Encontrar preço original (old-price → span.price)
        original_price = manga.find("span", class_="price-wrapper")
        original_price_text = original_price.find("span", class_="price").text.strip() if original_price else None
        old_price = manga.find("span", class_="old-price")
        old_price_text = old_price.find("span", class_="price").text.strip() if old_price else original_price_text

        print(f"📚 {title_text} - | Preço Original: {old_price_text} | Com Desconto: {special_price_text} | Link:{manga_url}")

        # Salvar os dados no CSV
        writer.writerow({
            "Título": title_text,
            "Preço Original": old_price_text if old_price_text else "Não disponível",
            "Desconto": special_price_text if special_price_text else "Sem desconto",
        })

# Fechar o navegador
driver.quit()

# print(f"✅ Dados salvos com sucesso em: {csv_path}")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configuração do Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar em modo headless
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Inicializar o driver do Selenium
driver = webdriver.Chrome(options=chrome_options)

# URL do produto
url = "https://panini.com.br/solo-leveling-03"
driver.get(url)

# Aguardar o carregamento completo da página
time.sleep(5)  # Ajuste o tempo conforme necessário

# Obter o HTML da página
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Fechar o driver do Selenium
driver.quit()

# Dicionário para armazenar os dados extraídos
dados = {
    "Autor": None,
    "Mês de Lançamento": None,
    "Ano de Lançamento": None
}

# Encontrar todas as células <td> com a classe 'col data'
td_elements = soup.find_all("td", class_="col data")

# Iterar sobre os elementos encontrados para buscar os dados específicos
for td in td_elements:
    data_th = td.get("data-th", "").strip()
    valor = td.get_text(strip=True)
    
    # Identificar o autor
    if data_th == "Autores":
        dados["Autor"] = valor
    
    if data_th == "Mês":
        dados["Mês de Lançamento"] = valor
    
    if data_th  == "Ano de publicação":
        dados["Ano de Lançamento"] = valor

for chave, valor in dados.items():
    print(f"{chave}: {valor}")

# import os
# import csv
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# # Configuração do Chrome
# chrome_options = Options()
# chrome_options.add_argument("--headless")  
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")

# # Criar o driver do Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # URL da página inicial da Panini
# url = "https://panini.com.br/planet-manga?product_list_order=ratings_summary"
# driver.get(url)

# # Esperar a página carregar completamente
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
# )

# time.sleep(5)  # Ajuste o tempo conforme necessário

# # Capturar o HTML
# html_source = driver.page_source
# soup = BeautifulSoup(html_source, "html.parser")

# # ENCONTRAR O NÚMERO DA ÚLTIMA PÁGINA
# try:
#     ultima_pagina_element = soup.find("a", class_="page last")
#     if ultima_pagina_element:
#         spans = ultima_pagina_element.find_all("span")
#         total_paginas = int(spans[-1].text.strip())
#     else:
#         total_paginas = 1
# except Exception as e:
#     print(f"⚠️ Erro ao encontrar a última página: {e}")
#     total_paginas = 1

# print(f"🔍 Encontradas {total_paginas} páginas para scraping.")

# # Criar o arquivo CSV e escrever os cabeçalhos
# csv_path = os.path.join("Data", "mangas_panini.csv")
# with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
#     fieldnames = ["Título", "Preço Original", "Desconto", "Disponibilidade", "Pré-venda", "Autor", "Ano de Lançamento", "Mês de Lançamento"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     # LOOP PARA NAVEGAR POR TODAS AS PÁGINAS AUTOMATICAMENTE
#     for pagina in range(1, total_paginas + 1):
#         url = f"https://panini.com.br/planet-manga?p={pagina}&product_list_order=ratings_summary"
#         print(f"\n📄 Scraping da Página {pagina}...")
#         driver.get(url)

#         # Esperar os produtos carregarem completamente
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
#             )
#         except:
#             print(f"Produtos não carregaram na página {pagina} . Pulando...")
#             continue

#         # Capturar o HTML da página carregada
#         html_source = driver.page_source
#         soup = BeautifulSoup(html_source, "html.parser")

#         # Encontrar os produtos na página
#         mangas = soup.find_all("li", class_="item product product-item")

#         for manga in mangas:
#             # Extrair as informações principais
#             title = manga.find("a", class_="product-item-link")
#             title_text = title.text.strip() if title else "Título não encontrado"
#             manga_url = title['href'] if title else None

#             # Preço com desconto
#             special_price = manga.find("span", class_="special-price")
#             special_price_text = special_price.find("span", class_="price").text.strip() if special_price else None

#             # Preço original
#             original_price = manga.find("span", class_="price-wrapper")
#             original_price_text = original_price.find("span", class_="price").text.strip() if original_price else None

#             # Status de disponibilidade
#             status = manga.find("a", class_="bt-stock-unavailable")
#             status_text = status.text.strip() if status else "Disponível"

#             # Informações de pré-venda
#             prevenda = manga.find("div", class_="amlabel-text")
#             prevenda_text = prevenda.text.strip() if prevenda else None

            
#              # Acessar a página do manga para coletar informações adicionais
#             try:
#                 if manga_url:
#                     driver.get(manga_url)  # Corrigido para usar o href diretamente
#                     WebDriverWait(driver, 30).until(  # Aumentei o tempo para 30 segundos
#                         EC.presence_of_element_located((By.CLASS_NAME, "product-info"))
#                     )

#                     # Capturar a página do manga
#                     manga_html = driver.page_source
#                     manga_soup = BeautifulSoup(manga_html, "html.parser")

#                     # Coletar autor, ano e mês de lançamento
#                     author_text = "Autor não encontrado"
#                     year = "Ano não encontrado"
#                     month = "Mês não encontrado"

#                     # Encontrar o tbody com as informações
#                     tbody = manga_soup.find("tbody")
#                     if tbody:
#                         rows = tbody.find_all("tr")
#                         for row in rows:
#                             th = row.find("th")
#                             td = row.find("td")
#                             if th and td:
#                                 data_th = th.get("data-th")
#                                 if data_th == "Autores":
#                                     author_text = td.text.strip()
#                                 if data_th == "Ano de publicação":
#                                     year = td.text.strip()
#                                 if data_th == "Mês":
#                                     month = td.text.strip()

#                     # Retornar à página principal
#                     driver.back()
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
#                     )
#             except Exception as e:
#                 print(f"⚠️ Erro ao acessar a página do manga {title_text}: {e}")
#                 author_text, year, month = "Não disponível", "Não disponível", "Não disponível"

#             # Salvar os dados no CSV
#             writer.writerow({
#                 "Título": title_text,
#                 "Preço Original": original_price_text if original_price_text else "Não disponível",
#                 "Desconto": special_price_text if special_price_text else "Sem desconto",
#                 "Disponibilidade": status_text if status_text else "Disponível",
#                 "Pré-venda": prevenda_text if prevenda_text else "Não",
#                 "Autor": author_text,
#                 "Ano de Lançamento": year,
#                 "Mês de Lançamento": month
#             })

# # Fechar o navegador depois que tudo terminou
# driver.quit()

# print("\n✅ Dados salvos em 'mangas_panini.csv' com sucesso!")
