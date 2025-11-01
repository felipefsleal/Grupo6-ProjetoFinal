import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import os

# --- Configurações Globais do Módulo ---

# Define o caminho para a pasta de gráficos (../graphics)
PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')
# Garante que a pasta de gráficos exista
os.makedirs(PATH_GRAFICOS, exist_ok=True)

# Define o estilo padrão do Seaborn
sns.set_style("whitegrid")

# Mapeamento de meses (constante global)
MES_MAP = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
    5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
    9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}
# Lista ordenada de meses (constante global)
MESES_ORDENADOS = list(MES_MAP.values())


# --- Função de Plotagem de Sazonalidade ---

def plot_faturamento_sazonal_filial(df_vendas_produtos, categorias, nome_arquivo, titulo_grafico):
    df = df_vendas_produtos.copy()
    
    # Garante que a coluna de mês exista (caso o DF seja 'vendas_produtos' puro)
    if 'MES_NOME' not in df.columns:
        if 'MES_NUM' not in df.columns:
             # Converte DATA_ATEND (que já deve ser datetime do notebook)
             df['DATA_ATEND'] = pd.to_datetime(df['DATA_ATEND'])
             df['MES_NUM'] = df['DATA_ATEND'].dt.month
        df['MES_NOME'] = df['MES_NUM'].map(MES_MAP)

    # 2. Filtragem e Agrupamento
    
    # Adicionamos .str.strip() para limpar espaços antes de filtrar
    # Isso garante que 'Natal ' (com espaço) seja tratado como 'Natal'
    df_filtrado = df[df['CATEGORIA'].str.strip().isin(categorias)]
    
    # Agrupa o faturamento por mês e filial
    df_sazonal = df_filtrado.groupby(['MES_NOME', 'FILIAL'])['FATUR_VENDA'].sum().reset_index()

    if df_sazonal.empty:
        print(f"Aviso: Nenhuma venda encontrada para as categorias: {categorias}. Gráfico não gerado.")
        return

    # 3. Geração do Gráfico
    plt.figure(figsize=(14, 7))
    ax = sns.barplot(
        data=df_sazonal,
        x='MES_NOME',
        y='FATUR_VENDA',
        hue='FILIAL',
        order=MESES_ORDENADOS,
        palette='Set2'
    )

    # 4. Formatação e Rótulos
    ax.set_title(titulo_grafico, fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Faturamento (R$)', fontsize=12)

    # Formata o eixo Y para R$ K (Milhares) ou R$ (normal)
    max_faturamento = df_sazonal['FATUR_VENDA'].max()
    if max_faturamento >= 10000: # Se o pico for > 10K, usa 'K'
        formatter = ticker.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K')
    else:
        formatter = ticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    ax.legend(title='Filial', loc='upper left')

    # 5. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, nome_arquivo)
    plt.tight_layout()