import pandas as pd
import random
import numpy as np

# Caminho do arquivo Excel
excel_path = "Data\\paniniscout.xlsx"

# Carregar os dados do Excel
xls = pd.ExcelFile(excel_path)
df_titulos = pd.read_excel(xls, sheet_name=0)  # Ajuste a sheet_name caso necessário

# Criar coluna "Preço" (5% mais caro para 5% dos títulos)
df_titulos["Preço"] = df_titulos["PreçoOriginal"]
indices_ajustados = random.sample(range(len(df_titulos)), k=int(0.05 * len(df_titulos)))
df_titulos.loc[indices_ajustados, "Preço"] *= 1.05

df_titulos["Preço"] = df_titulos["Preço"].round(2)

# Criar coluna "Estoque" aleatório entre 0 e 15
df_titulos["Estoque"] = np.random.randint(0, 16, size=len(df_titulos))

# Gerar as datas de reposição
start_date = pd.to_datetime("2022-01-02")
end_date = pd.to_datetime("2025-03-02")

reposicoes = []
for _ in range(len(df_titulos)):
    date = start_date
    entrada_info = []
    while date <= end_date:
        if date.weekday() != 6:  # Evita domingos
            qtd = random.randint(1, 5)
            entrada_info.append(f"{date.strftime('%d/%m/%Y')} ({qtd})")
        date += pd.Timedelta(days=random.choice([25, 30]))
    reposicoes.append(", ".join(entrada_info))

df_titulos["Entrada"] = reposicoes

# Criar coluna "Saída"
def calcular_saida(estoque, entrada):
    if not entrada:  # Caso não haja entrada registrada
        return 0

    # Extrai os valores de entrada dos parênteses
    total_entrada = sum(int(e.split('(')[-1][:-1]) for e in entrada.split(", ") if '(' in e and ')' in e)

    # Se o estoque for maior que zero, saída = entrada total - estoque
    return max(0, total_entrada - estoque) if estoque > 0 else total_entrada

df_titulos["Saída"] = df_titulos.apply(lambda row: calcular_saida(row["Estoque"], row["Entrada"]), axis=1)

# Salvar em um novo arquivo Excel
output_path = "Data\\paniniscout.xlsx"
df_titulos.to_excel(output_path, index=False)

print(f"Arquivo salvo em {output_path}")