#   Projeto Comic Trend Scout   (Projeto em andamento)

## Sobre o Projeto
Este projeto tem como objetivo otimizar a gestão de estoque da Livraria Saber voltado para mangás e Histórias em Quadrinhos. Para isso será utilizado análise de dados para prever tendências de vendas e auxiliar na tomada de decisões estratégicas de reposição de estoque, além da prevenção de tendências utilizando Machine Learning NLP para análise de comportamento e popularidade. Para isso, combino dados internos da livraria com métricas externas de popularidade e tendências, como rankings, avaliações online e popularidade em redes sociais.

##  Funcionalidades
-   Coleta de Dados: Extração de informações de vendas e estoque da livraria.

-   Web Scraping: Coleta de métricas externas de editoras (NewPOP,Planet Mangá, JBC, Pipoca&Nanquim, Darkside), blogs e Streamings (myanimelist e Crunchyroll) para análise de popularidade.

-   Análise de Tendências: Identificação de padrões de vendas e demanda futura ao análisar trend's na cidade local (arredores) e internet.

-   Modelo Preditivo: Algoritmo para prever quais títulos têm maior probabilidade de venda.

-   Dashboard Interativo: Visualização dos insights gerados no Power BI.

##  Dados Utilizados

-   **Dados Internos:**

    -   Histórico de compras e vendas do ano de 2022 a 2025

    -   Estoque atual de cada título disponível na Livraria

    -   Títulos em estoque na livraria que se encontram esgotados nas editoras e plataformas de e-commerce (Amazon e Shopee)

-   **Dados Externos:**

    -   Posição de mais vendidos das 5 editoras fornecedoras
    -   avaliações dos títulos coletados via web scraping (myanimelist, Crunchyroll e Biblioteca Brasileira de Mangás)

##  Tecnologias Utilizadas

-   **Linguagens:** Python, SQL

-   **Bibliotecas e Frameworks:** Pandas, NumPy, Selenium, BeautifulSoup, Matplotlib, Seaborn

-   **Banco de Dados:** PostgreSQL

-   **Data Visualization Tool:** Excel, Jupyter Notebook, Power BI

##  Estrutura do Projeto

    📂 ComicTrend Scout
        │── 📁 data               # Arquivos CSV e Excel com dados processados
        │── 📁 scripts            # Código-fonte para coleta e análise de dados
        │── 📁 notebooks          # Jupyter Notebooks com análises exploratórias
        │── 📁 models             # Modelos preditivos treinados
        │── 📁 dashboard          # Interface para visualização de insights
        │── README.md             # Documentação do projeto

#   Status do Andamento do Projeto
    Início do projeto: 24/03/2025 
    previsão para finalização: 24/04/2025
✅ Coleta e limpeza de dados internos </br>
✅ Web scraping de dados externos </br>
🔄 Desenvolvimento do modelo preditivo (em progresso) </br>
🔄 Criação do dashboard (em progresso)

##  Próximos Passos

-   Refinamento do modelo preditivo

-   Integração dos dados no dashboard interativo

-   Testes e validação da previsão de demanda

##  Contribuições

Este projeto ainda está em desenvolvimento e colaborações são bem-vindas! Caso tenha sugestões ou queira contribuir, sinta-se à vontade para abrir uma issue ou pull request.

## 📧 Contato

Caso tenha dúvidas ou sugestões, entre em contato:
</br> LinkedIn: https://www.linkedin.com/in/celinemlyra/ </br>
</br> GitHub: https://github.com/celymoon


.</br>
.</br>
.


_OBS: Este README será atualizado conforme o projeto avança._

