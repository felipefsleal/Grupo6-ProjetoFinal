import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import os

PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')

def top_categorias_vendidas(df):
    df_volume_categoria = df.groupby('CATEGORIA')['QTD_VENDA'].sum().reset_index()

    total_volume = df_volume_categoria['QTD_VENDA'].sum()
    df_volume_categoria['PERCENTUAL'] = (df_volume_categoria['QTD_VENDA'] / total_volume) * 100

    df_top_10_volume = df_volume_categoria.sort_values(
        'PERCENTUAL', ascending=False
    ).head(10)

    plt.figure(figsize=(14, 7))
    sns.set_style("whitegrid")

    ax = sns.barplot(
        data=df_top_10_volume,
        x='CATEGORIA',
        y='PERCENTUAL',
        hue='CATEGORIA',
        palette='Spectral',
        legend=False
    )

    ax.set_title('Top 10 Categorias Mais Vendidas (Volume) - 2024', fontsize=16)
    ax.set_xlabel('Categoria', fontsize=12)
    ax.set_ylabel('Percentual do Volume Total (%)', fontsize=12)

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

    PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')
    save_path = os.path.join(PATH_GRAFICOS, 'top_10_categorias_volume_vendas.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_subcategorias_vendidas(df):
    df_volume_categoria = df.groupby('SUBCATEGORIA')['QTD_VENDA'].sum().reset_index()

    total_volume = df_volume_categoria['QTD_VENDA'].sum()
    df_volume_categoria['PERCENTUAL'] = (df_volume_categoria['QTD_VENDA'] / total_volume) * 100

    df_top_10_volume = df_volume_categoria.sort_values(
        'PERCENTUAL', ascending=False
    ).head(10)

    plt.figure(figsize=(14, 7))
    sns.set_style("whitegrid")

    ax = sns.barplot(
        data=df_top_10_volume,
        x='SUBCATEGORIA',
        y='PERCENTUAL',
        hue='SUBCATEGORIA',
        palette='Spectral',
        legend=False
    )

    ax.set_title('Top 10 Subcategorias Mais Vendidas (Volume) - 2024', fontsize=16)
    ax.set_xlabel('Subcategoria', fontsize=12)
    ax.set_ylabel('Percentual do Volume Total (%)', fontsize=12)

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

    PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')
    save_path = os.path.join(PATH_GRAFICOS, 'top_subcategorias_vendidas.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()