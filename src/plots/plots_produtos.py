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

def top_categorias_sazonais(df, n_top, outliers):
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    meses_ordenados = [mes_map[m] for m in outliers]

    df['MES_NUM'] = df['DATA_ATEND'].dt.month

    df_outliers = df.loc[
        df['MES_NUM'].isin(outliers)
    ].copy()

    df_agregado = df_outliers.groupby(['MES_NUM', 'CATEGORIA'])['QTD_VENDA'].sum().reset_index()
    df_agregado['TOTAL_MES'] = df_agregado.groupby('MES_NUM')['QTD_VENDA'].transform('sum')
    df_agregado['PERCENTUAL'] = (df_agregado['QTD_VENDA'] / df_agregado['TOTAL_MES']) * 100

    def get_top_n(group):
        return group.nlargest(n_top, 'PERCENTUAL')

    df_top_n_mensal = df_agregado.groupby('MES_NUM', group_keys=False).apply(get_top_n)
    
    df_top_n_mensal['MES_NOME'] = df_top_n_mensal['MES_NUM'].map(mes_map)

    plt.figure(figsize=(14, 7))
    
    ax = sns.barplot(
        data=df_top_n_mensal,
        x='MES_NOME',
        y='PERCENTUAL',
        hue='CATEGORIA', 
        order=meses_ordenados,
        palette='tab10' 
    )

    formatter_k = ticker.FuncFormatter(lambda x, p: f'{x/1000:.1f}K')
    ax.yaxis.set_major_formatter(formatter_k)
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center',
                       xytext = (0, 9),
                       textcoords = 'offset points',
                       fontsize=8,
                       fontweight='bold')

    ax.set_title(f'Top {n_top} Categorias Mais Vendidas por Mês Sazonal (Volume)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Percentual', fontsize=12)
    ax.legend(title='Categoria', loc='upper left', bbox_to_anchor=(1.0, 1))

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # 6. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, 'top_3_categorias_sazonais.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_subcategorias_sazonais(df, n_top, outliers):
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    meses_ordenados = [mes_map[m] for m in outliers]

    df['MES_NUM'] = df['DATA_ATEND'].dt.month

    df_outliers = df.loc[
        df['MES_NUM'].isin(outliers)
    ].copy()

    df_agregado = df_outliers.groupby(['MES_NUM', 'SUBCATEGORIA'])['QTD_VENDA'].sum().reset_index()
    df_agregado['TOTAL_MES'] = df_agregado.groupby('MES_NUM')['QTD_VENDA'].transform('sum')
    df_agregado['PERCENTUAL'] = (df_agregado['QTD_VENDA'] / df_agregado['TOTAL_MES']) * 100

    def get_top_n(group):
        return group.nlargest(n_top, 'PERCENTUAL')

    df_top_n_mensal = df_agregado.groupby('MES_NUM', group_keys=False).apply(get_top_n)
    
    df_top_n_mensal['MES_NOME'] = df_top_n_mensal['MES_NUM'].map(mes_map)

    plt.figure(figsize=(14, 7))
    
    ax = sns.barplot(
        data=df_top_n_mensal,
        x='MES_NOME',
        y='PERCENTUAL',
        hue='SUBCATEGORIA', 
        order=meses_ordenados,
        palette='tab10' 
    )

    formatter_k = ticker.FuncFormatter(lambda x, p: f'{x/1000:.1f}K')
    ax.yaxis.set_major_formatter(formatter_k)
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center',
                       xytext = (0, 9),
                       textcoords = 'offset points',
                       fontsize=8,
                       fontweight='bold')

    ax.set_title(f'Top {n_top} Subcategorias Mais Vendidas por Mês Sazonal (Volume)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Percentual', fontsize=12)
    ax.legend(title='Categoria', loc='upper left', bbox_to_anchor=(1.0, 1))

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # 6. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, 'top_3_subcategorias_sazonais.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_categoria_outlier_share(df, categoria, outliers):
    non_outlier_months = [m for m in range(1, 13) if m not in outliers]
    
    mes_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
               7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    meses_ordenados = [mes_map[m] for m in non_outlier_months]

    df['MES_NUM'] = df['DATA_ATEND'].dt.month

    df_non_outliers = df.loc[
        df['MES_NUM'].isin(non_outlier_months)
    ].copy()

    df_agregado = df_non_outliers.groupby(['MES_NUM', 'CATEGORIA'])['QTD_VENDA'].sum().reset_index()

    df_agregado['TOTAL_MES'] = df_agregado.groupby('MES_NUM')['QTD_VENDA'].transform('sum')
    df_agregado['PERCENTUAL'] = (df_agregado['QTD_VENDA'] / df_agregado['TOTAL_MES']) * 100

    df_target = df_agregado.loc[df_agregado['CATEGORIA'] == categoria].copy()
    
    df_target['MES_NOME'] = df_target['MES_NUM'].map(mes_map)

    # 5. --- Plotagem ---
    plt.figure(figsize=(14, 7))
    
    ax = sns.barplot(
        data=df_target,
        x='MES_NOME',
        y='PERCENTUAL', 
        order=meses_ordenados,
        # Usando 'color' para cor única (melhor prática)
        color=sns.color_palette('Reds', n_colors=1)[0]
    )

    # Formatação Eixo Y é agora %
    formatter_pct = ticker.FuncFormatter(lambda x, p: f'{x:.1f}%')
    ax.yaxis.set_major_formatter(formatter_pct)
    
    # Adiciona rótulos de dados (em Percentual)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center',
                       xytext = (0, 9),
                       textcoords = 'offset points',
                       fontsize=9,
                       fontweight='bold')

    ax.set_title(f"Participação (%) da Categoria '{categoria}' no Volume Mensal (Meses NÃO-SAZONAIS)", fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Percentual do Volume Total do Mês (%)', fontsize=12)

    plt.tight_layout()
    
    # 6. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, f'participacao_mensal_{categoria.lower().replace(" ", "_")}_non_outlier.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()