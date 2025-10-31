import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import os

#Configurações Globais do Módulo

# Define o caminho para a pasta de gráficos (../graphics)
PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')
# Garante que a pasta de gráficos exista
os.makedirs(PATH_GRAFICOS, exist_ok=True)

# Define o estilo padrão do Seaborn para todas as funções deste módulo
sns.set_style("whitegrid")


#Funções de Plotagem

def plot_top_10_categorias(df_produtos):
    """
    Limpa, calcula e plota um gráfico de barras com as 10 principais
    categorias de produtos.
    
    Argumentos:
        df_produtos (pd.DataFrame): O DataFrame de produtos.
    """
    print("Iniciando plot: Top 10 Categorias...")
    
    # 1. Criar uma lista de categorias a serem excluídas
    categorias_para_excluir = ['Sem categoria', '']

    # 2. Filtrar o DataFrame
    produtos_clean_categoria = df_produtos[
        ~df_produtos['CATEGORIA'].str.strip().isin(categorias_para_excluir)
    ]

    print(f"Total de produtos no catálogo: {len(df_produtos)}")
    print(f"Total de produtos com categoria definida: {len(produtos_clean_categoria)}")

    # 3. Selecionar o Top 10
    top_10_cat = produtos_clean_categoria['CATEGORIA'].value_counts(normalize=True).head(10)

    # 4. Converter a Series para um DataFrame
    top_10_df = top_10_cat.reset_index()

    # 5. Renomear as colunas
    top_10_df.columns = ['CATEGORIA', 'PERCENTUAL']

    # 6. Converter o percentual de (0.0 a 1.0) para (0 a 100) para exibição
    top_10_df['PERCENTUAL'] = top_10_df['PERCENTUAL'] * 100

    print("\nTop 10 Categorias (%):")
    print(top_10_df)

    # --- Geração do Gráfico ---
    plt.figure(figsize=(12, 8))

    ax = sns.barplot(
        data=top_10_df,
        x='CATEGORIA',
        y='PERCENTUAL',
        palette='Spectral'
    )

    ax.set_title('Top 10 Categorias de Produtos (Percentual do Total Definido)', fontsize=16)
    ax.set_xlabel('Categoria', fontsize=12)
    ax.set_ylabel('Percentual do Total (%)', fontsize=12)

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.1f}%'))

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center', va = 'center',
                   xytext = (0, 9),
                   textcoords = 'offset points',
                   fontsize=10)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Salvar e exibir
    save_path = os.path.join(PATH_GRAFICOS, 'top_10_categorias.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

    print(f"\nGráfico salvo com sucesso em: {save_path}")


def plot_top_10_subcategorias(df_produtos):
    """
    Limpa, calcula e plota um gráfico de barras com as 10 principais
    subcategorias de produtos.
    
    Argumentos:
        df_produtos (pd.DataFrame): O DataFrame de produtos.
    """
    print("Iniciando plot: Top 10 Subcategorias...")
    
    # 1. Criar uma lista de subcategorias a serem excluídas
    subcategorias_para_excluir = ['Sem subcategoria', '']

    # 2. Filtrar o DataFrame
    produtos_clean_subcategoria = df_produtos[
        ~df_produtos['SUBCATEGORIA'].str.strip().isin(subcategorias_para_excluir)
    ]

    print(f"Total de produtos no catálogo: {len(df_produtos)}")
    print(f"Total de produtos com subcategoria definida: {len(produtos_clean_subcategoria)}")

    # 3. Selecionar o Top 10
    top_10_cat = produtos_clean_subcategoria['SUBCATEGORIA'].value_counts(normalize=True).head(10)

    # 4. Converter a Series para um DataFrame
    top_10_df = top_10_cat.reset_index()

    # 5. Renomear as colunas
    top_10_df.columns = ['SUBCATEGORIA', 'PERCENTUAL']

    # 6. Converter o percentual de (0.0 a 1.0) para (0 a 100) para exibição
    top_10_df['PERCENTUAL'] = top_10_df['PERCENTUAL'] * 100

    print("\nTop 10 Subcategorias (%):")
    print(top_10_df)

    # --- Geração do Gráfico ---
    plt.figure(figsize=(12, 8))

    ax = sns.barplot(
        data=top_10_df,
        x='SUBCATEGORIA',
        y='PERCENTUAL',
        palette='Spectral'
    )

    ax.set_title('Top 10 Subcategorias de Produtos (Percentual do Total Definido)', fontsize=16)
    ax.set_xlabel('Subcategoria', fontsize=12)
    ax.set_ylabel('Percentual do Total (%)', fontsize=12)

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.1f}%'))

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center', va = 'center',
                   xytext = (0, 9),
                   textcoords = 'offset points',
                   fontsize=10)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Salvar e exibir
    save_path = os.path.join(PATH_GRAFICOS, 'top_10_subcategorias.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

    print(f"\nGráfico salvo com sucesso em: {save_path}")