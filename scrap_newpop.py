import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


#Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


#Criando o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

#URL da página inicial da NewPOP
url = "https://www.lojanewpop.com.br/mangas?sort=mais_vendidos&pagina=1"
driver.get(url)

# Esperar a Página carregar completamente
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "info-produto"))
)

time.sleep(5)

# Capturar o HTML
html_source = driver.page_source
soup = BeautifulSoup(html_source, "html.parser")

# Encontrar o número da última página disponivel
try:
    pagination_element = soup.find("div", class_="pagination")
    if pagination_element:
            #Pegar todas as li dentro da paginação
            pages = pagination_element.find_all("a")
            #filtrar a última li que contenha um número
            page_numbers = [a.text.strip() for a in pages if a.text.strip().isdigit()]
            if page_numbers:
                total_pages = int(page_numbers[-1]) #últma página ativa
            else:
                total_pages = 1
except Exception as e:
    print(f"Erro ao encontrar a última página: {e}")
    total_pages = 1

print(f"Encontradas {total_pages} páginas para scraping.")

#Criar o arquivo CSV e escrever os cabeçalhos
with open("mangas_newpop.csv", "w", newline="", encoding="utf-8") as csvfile:
     fieldnames = ["Título", "Preço Original", "Desconto", "Disponibilidade"]
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writeheader()

     #Loop para navegar por todas as páginas automaticamente
     for page in range(1, total_pages + 1):
          url = f"https://www.lojanewpop.com.br/mangas?sort=mais_vendidos&pagina={page}"
          print(f"Scraping da página {page}...")
          driver.get(url)

          #Esperar os produtos carregarem completamente
          try:
               WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "info-produto"))
               )
          except:
               print(f" Produtos nao carregaram na página {page}. Pulando...")
               continue
          
          #Capturar o html da pagina carregada
          html_source = driver.page_source
          soup = BeautifulSoup(html_source, "html.parser")

          #Encontrar os produtos na página
          mangas = soup.find_all("div", class_="info-produto")

          for manga in mangas:
               #encontrar o título do manga
               title = manga.find("a", class_="nome-produto cor-secundaria")
               title_text = title.text.strip() if title else "Título não encontrado"

               # Disponibilidade do Produto
               indisponivel = manga.find("a", class_="botao avise-me-list-btn btn-block avise-me-pop-cadastro")
               indisponivel_text = indisponivel.text.strip() if indisponivel else "Disponível"

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
               
               print(f"{title_text} - preco original: {old_price_text} - desconto: {special_price_text} - Disponibilidade: {indisponivel_text}")

               writer.writerow({
                         "Título": title_text,
                         "Preço Original": old_price_text if old_price_text else "Não disponível",
                         "Desconto": special_price_text if special_price_text != old_price_text else "Sem desconto",
                         "Disponibilidade": indisponivel_text if indisponivel_text else None
                })
driver.quit()

print("Dados salvos em mangas_newpopo.csv com sucesso!")
