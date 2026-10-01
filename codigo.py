# Limpar os dados do arquivo .csv
# Cabeçalho do arqwuivo esta separado por "\"
# plotar o gráfico

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

linhas_processadas = []

# 1. Lê o arquivo e normaliza os delimitadores
with open("efluente_agua_consumida.csv", "r", encoding="cp1252") as f:
    for linha in f:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
            
        linha_limpa = linha_limpa.strip('"')
        linha_normalizada = linha_limpa.replace('","', '|').replace('""', '').replace('"', '')
        campos = [campo.strip() for campo in linha_normalizada.split('|')]
        linhas_processadas.append(campos)

max_colunas = max(len(l) for l in linhas_processadas)
linhas_alinhadas = [l + [''] * (max_colunas - len(l)) for l in linhas_processadas]

# 2. Cria o DataFrame e padroniza colunas
cabecalho = linhas_alinhadas[0]
dados = linhas_alinhadas[1:]

tabela = pd.DataFrame(dados, columns=cabecalho)
tabela.columns = tabela.columns.str.replace('"', '').str.strip()

# 3. Extrai apenas o nome do município e descarta o IBGE
tabela['Município'] = tabela['Município,ibge'].str.split(',').str[0]
tabela = tabela.drop(columns=['Município,ibge'], errors='ignore')

# 4. Simplifica os nomes das colunas de anos (ex: "1998")
novos_nomes = {}
for col in tabela.columns:
    if "consumida" in col:
        ano = col.split("consumida")[-1].split("(%)")[0].strip()
        novos_nomes[col] = ano
tabela = tabela.rename(columns=novos_nomes)

anos = [col for col in tabela.columns if col.isdigit()]

# 5. Converte valores de texto para números (trata '-' como NaN)
for ano in anos:
    tabela[ano] = tabela[ano].replace('-', np.nan)
    tabela[ano] = tabela[ano].astype(str).str.replace(',', '.')
    tabela[ano] = pd.to_numeric(tabela[ano], errors='coerce')

import matplotlib.pyplot as plt
import seaborn as sns

# 6. Prepara os dados para o Heatmap
df_heatmap = tabela.set_index('Município')[anos]

# Ordena os municípios pelo desempenho mais recente (2022)
if '2022' in df_heatmap.columns:
    df_heatmap = df_heatmap.sort_values(by='2022', ascending=False)
else:
    df_heatmap = df_heatmap.sort_index()

# 7. Configura e plota o Heatmap
fig, ax = plt.subplots(figsize=(16, 32))

sns.heatmap(
    df_heatmap,
    cmap='YlGnBu',
    vmin=0,
    vmax=100,
    linewidths=0.05,
    linecolor='#e0e0e0',
    cbar_kws={'label': 'Índice de Esgoto Tratado (%)', 'shrink': 0.5},
    yticklabels=True,
    ax=ax
)

plt.title('Evolução do Esgoto Tratado por Município do RS (1998–2022)', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Ano', fontsize=13, labelpad=10)
plt.ylabel('Município', fontsize=13, labelpad=10)
plt.yticks(fontsize=7)
plt.xticks(rotation=45, fontsize=10)

# 8. Adiciona Fonte Oficial (Dados RS / SPGG-DEE) e Autor
plt.figtext(
    0.08, 0.01, 
    "Fonte: Portal Dados RS — SPGG/DEE (Saneamento - Esgoto - Tratamento)", 
    fontsize=10, 
    fontstyle='italic', 
    color='#333333', 
    ha='left'
)

plt.figtext(
    0.88, 0.01, 
    "Autor: Gabriel Siqueira dos Santos", 
    fontsize=10, 
    fontweight='bold', 
    color='#222222', 
    ha='right'
)

# Ajuste da margem inferior para preservar os créditos
plt.subplots_adjust(bottom=0.03)

# Salva em 300 DPI e exibe
plt.savefig('heatmap_esgoto_RS.png', dpi=300, bbox_inches='tight')
print("Heatmap atualizado e salvo como 'heatmap_esgoto_RS.png'!")
plt.show()


# FIM DO SCRIPT
