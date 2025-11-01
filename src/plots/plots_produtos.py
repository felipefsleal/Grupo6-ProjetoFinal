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
        palette='Blues_r',
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
        palette='Blues_r',
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
        palette='Blues_r' 
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
        palette='Blues_r' 
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
        pallete='Blues_r'
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

def top_categorias_mensal(df, n_top):
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    meses_ordenados = list(mes_map.values())

    df['MES_NUM'] = df['DATA_ATEND'].dt.month

    df_agregado = df.groupby(['MES_NUM', 'CATEGORIA'])['QTD_VENDA'].sum().reset_index()
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
        palette='Blues_r' 
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

    ax.set_title(f'Top {n_top} Categorias Mais Vendidas por Mês (Volume)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Percentual', fontsize=12)
    ax.legend(title='Categoria', loc='upper left', bbox_to_anchor=(1.0, 1))

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # 6. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, 'top_3_categorias_sazonais.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_produtos_sazonais_percentual(df, n_top, outliers, categoria):
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    meses_ordenados = [mes_map[m] for m in outliers]

    # 1. Filtra os dados para os meses de pico E a categoria alvo
    df_alvo = df.loc[
        (df['MES_NUM'].isin(outliers)) & 
        (df['CATEGORIA'] == categoria)
    ].copy()
    
    if df_alvo.empty:
        print(f"Aviso: O DataFrame alvo para a categoria '{categoria}' está vazio. Verifique o nome da categoria ou os filtros.")
        return

    # 2. Agrupa por Mês e Nome do Produto, somando o volume
    df_agg = df_alvo.groupby(['MES_NUM', 'NOME_PRODUTO'])['QTD_VENDA'].sum().reset_index()

    # 3. Calcula o Percentual de participação do SKU no volume TOTAL DA CATEGORIA NAQUELE MÊS
    
    # Calcula o total de volume da CATEGORIA por mês (usando transform)
    df_agg['TOTAL_MES_CAT'] = df_agg.groupby('MES_NUM')['QTD_VENDA'].transform('sum')
    
    # Calcula o Percentual
    df_agg['PERCENTUAL'] = (df_agg['QTD_VENDA'] / df_agg['TOTAL_MES_CAT']) * 100

    # 4. Encontra os Top N SKUs para CADA MÊS, baseado em PERCENTUAL
    def get_top_n(group):
        # Agora o nlargest usa a coluna PERCENTUAL para ranquear
        return group.nlargest(n_top, 'PERCENTUAL')

    df_top_n_mensal = df_agg.groupby('MES_NUM', group_keys=False).apply(get_top_n)
    
    # 5. Mapeia o MES_NUM para MES_NOME para os rótulos do gráfico
    df_top_n_mensal['MES_NOME'] = df_top_n_mensal['MES_NUM'].map(mes_map)

    # 6. --- Plotagem ---
    plt.figure(figsize=(14, 7))
    sns.set_style("whitegrid")
    
    ax = sns.barplot(
        data=df_top_n_mensal,
        x='MES_NOME',
        y='PERCENTUAL', 
        hue='NOME_PRODUTO', 
        order=meses_ordenados,
        palette='Blues_r' # Paleta de cores para diferenciar os SKUs
    )

    # Formatação Eixo Y é %
    formatter_pct = ticker.FuncFormatter(lambda x, p: f'{x:.1f}%')
    ax.yaxis.set_major_formatter(formatter_pct)
    
    # Adiciona rótulos de dados (em Percentual)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center',
                       xytext = (0, 5),
                       textcoords = 'offset points',
                       fontsize=7)

    ax.set_title(f"Participação (%) dos Top {n_top} SKUs em '{categoria}' por Mês Sazonal", fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Participação no Volume da Categoria (%)', fontsize=12)
    ax.legend(title='Produto (SKU)', loc='upper left', bbox_to_anchor=(1.0, 1))

    plt.tight_layout(rect=[0, 0, 0.8, 1])
    
    # 7. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, f'top_{n_top}_skus_sazonais_percentual.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def plot_top_subcategorias_sazonais(df, n_top):
    """
    Plota a participação percentual (volume) das Top N subcategorias mais vendidas 
    nos meses sazonais de pico (Março, Novembro, Dezembro).
    """
    
    meses_pico = [3, 11, 12] 
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    meses_ordenados = [mes_map[m] for m in meses_pico]
    
    print(f"Iniciando plot: Top {n_top} Subcategorias por Percentual nos Meses Sazonais {meses_ordenados}...")

    # 1. Filtra os dados apenas para os meses de pico
    df_picos = df.loc[
        df['MES_NUM'].isin(meses_pico)
    ].copy()

    # 2. Agrupa por Mês e SUBCATEGORIA, somando a QTD_VENDA (Volume)
    df_agregado = df_picos.groupby(['MES_NUM', 'SUBCATEGORIA'])['QTD_VENDA'].sum().reset_index()

    # 3. CÁLCULO DE PERCENTUAL: Calcula o Percentual de participação da Subcategoria no volume TOTAL DAQUELE MÊS
    
    # Calcula o total de volume por mês (usando transform)
    df_agregado['TOTAL_MES'] = df_agregado.groupby('MES_NUM')['QTD_VENDA'].transform('sum')
    
    # Calcula o Percentual
    df_agregado['PERCENTUAL'] = (df_agregado['QTD_VENDA'] / df_agregado['TOTAL_MES']) * 100

    # 4. Encontra as Top N subcategorias para CADA MÊS, baseado em PERCENTUAL
    def get_top_n(group):
        # O nlargest agora usa a coluna PERCENTUAL para ranquear
        return group.nlargest(n_top, 'PERCENTUAL')

    df_top_n_mensal = df_agregado.groupby('MES_NUM', group_keys=False).apply(get_top_n)
    
    # 5. Mapeia o MES_NUM para MES_NOME para os rótulos do gráfico
    df_top_n_mensal['MES_NOME'] = df_top_n_mensal['MES_NUM'].map(mes_map)

    # 6. --- Plotagem ---
    plt.figure(figsize=(14, 7))
    
    ax = sns.barplot(
        data=df_top_n_mensal,
        x='MES_NOME',
        y='PERCENTUAL', # Eixo Y é agora o PERCENTUAL
        hue='SUBCATEGORIA', 
        order=meses_ordenados,
        palette='Blues_r' 
    )

    # Formatação Eixo Y é %
    formatter_pct = ticker.FuncFormatter(lambda x, p: f'{x:.1f}%')
    ax.yaxis.set_major_formatter(formatter_pct)
    
    # Adiciona rótulos de dados (em Percentual)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center',
                       xytext = (0, 5),
                       textcoords = 'offset points',
                       fontsize=7)

    # Título e Eixos atualizados para refletir o percentual
    ax.set_title(f"Participação (%) das Top {n_top} Subcategorias no Volume Mensal (Meses de Pico)", fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Participação no Volume Total do Mês (%)', fontsize=12)
    ax.legend(title='Subcategoria', loc='upper left', bbox_to_anchor=(1.0, 1))

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # 7. Salvamento
    save_path = os.path.join(os.pardir, 'graphics', 'top_3_subcategorias_sazonais_percentual.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def subcategoria_by_filial_sazonal(df_vendas_completo, target_subcategory):
    """
    Compara o percentual de participação no volume de vendas da subcategoria alvo 
    entre as filiais RUA e SHOPPING nos meses de pico.
    """
    
    meses_pico = [3, 11, 12] 
    mes_map = {3: 'Mar', 11: 'Nov', 12: 'Dez'}
    meses_ordenados = list(mes_map.values())

    # 1. Filtra os dados para os meses de pico E a subcategoria alvo
    df_alvo = df_vendas_completo.loc[
        (df_vendas_completo['MES_NUM'].isin(meses_pico)) & 
        (df_vendas_completo['SUBCATEGORIA'] == target_subcategory)
    ].copy()

    if df_alvo.empty:
        print(f"Aviso: Não há vendas da subcategoria '{target_subcategory}' nos meses de pico.")
        return

    # 2. Agrupa por Mês e Filial, somando o volume
    df_agregado = df_alvo.groupby(['MES_NUM', 'FILIAL'])['QTD_VENDA'].sum().reset_index()

    # 3. CÁLCULO DE PERCENTUAL: Participação da Filial no volume TOTAL DA SUBCATEGORIA NAQUELE MÊS
    
    # Calcula o total de volume da subcategoria por mês (usando transform)
    df_agregado['TOTAL_MES_SUBCAT'] = df_agregado.groupby('MES_NUM')['QTD_VENDA'].transform('sum')
    
    # Calcula o Percentual
    df_agregado['PERCENTUAL'] = (df_agregado['QTD_VENDA'] / df_agregado['TOTAL_MES_SUBCAT']) * 100
    
    # 4. Mapeia o MES_NUM para MES_NOME
    df_agregado['MES_NOME'] = df_agregado['MES_NUM'].map(mes_map)

    # 5. --- Plotagem (Percentual) ---
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    ax = sns.barplot(
        data=df_agregado,
        x='MES_NOME',
        y='PERCENTUAL', # Eixo Y agora é PERCENTUAL
        hue='FILIAL', 
        order=meses_ordenados,
        palette='Blues' 
    )

    # Formatação Eixo Y para %
    formatter_pct = ticker.FuncFormatter(lambda x, p: f'{x:.1f}%')
    ax.yaxis.set_major_formatter(formatter_pct)
    
    # Adiciona rótulos de dados (em Percentual)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center',
                       xytext = (0, 5),
                       textcoords = 'offset points',
                       fontsize=9)

    ax.set_title(f"Participação (%) no Volume de '{target_subcategory}' por Filial (Picos Sazonais)", fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Participação no Volume da Subcategoria (%)', fontsize=12)
    ax.legend(title='Filial', loc='upper right')

    plt.tight_layout()
    
    # 6. Salvamento (Atualizar o nome do arquivo)
    save_path = os.path.join(os.pardir, 'graphics', f'{target_subcategory.lower()}_percentual_por_filial_sazonal.png'.replace(' ', '_'))
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_produtos(df):
    df_faturamento_produto = df.groupby(['NOME_PRODUTO', 'CATEGORIA']).agg(
        Faturamento_Total=('FATUR_VENDA', 'sum')
    ).reset_index()

    # 2. Ordenar pelo Faturamento e selecionar os Top 20 produtos mais vendidos
    df_top_produtos = df_faturamento_produto.sort_values(by='Faturamento_Total', ascending=False).head(20)

    # 3. Preparar a visualização
    plt.figure(figsize=(14, 8))
    sns.set_style("whitegrid")

    # 4. Criar o gráfico de barras, diferenciando pela CATEGORIA
    # Usando a coluna 'CATEGORIA' para determinar a cor (hue)
    bar_plot = sns.barplot(
        data=df_top_produtos,
        x='NOME_PRODUTO',
        y='Faturamento_Total',
        hue='CATEGORIA',
        dodge=False
    )

    # 5. Adicionar Título e Rótulos
    plt.title(f'Top 20 Produtos por Faturamento Total',fontsize=16)
    plt.xlabel('Produto', fontsize=12)
    plt.ylabel('Faturamento Total (R$)', fontsize=12)

    # Rotacionar os rótulos do eixo X para melhor leitura
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)

    # 6. Melhorar a Legenda
    plt.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')

    # 7. Ajustar o layout e salvar o gráfico
    PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')
    save_path = os.path.join(PATH_GRAFICOS, 'top_produtos.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_produtos_volume(df):
    df_volume_produto = df.groupby(['NOME_PRODUTO', 'CATEGORIA']).agg(
        Volume_Total=('QTD_VENDA', 'sum')
    ).reset_index()

    # 2. Ordenar pelo Faturamento e selecionar os Top 20 produtos mais vendidos
    df_top_produtos = df_volume_produto.sort_values(by='Volume_Total', ascending=False).head(20)

    # 3. Preparar a visualização
    plt.figure(figsize=(14, 8))
    sns.set_style("whitegrid")

    # 4. Criar o gráfico de barras, diferenciando pela CATEGORIA
    # Usando a coluna 'CATEGORIA' para determinar a cor (hue)
    bar_plot = sns.barplot(
        data=df_top_produtos,
        x='NOME_PRODUTO',
        y='Volume_Total',
        hue='CATEGORIA',
        dodge=False,
        pallete='Blues_r'
    )

    # 5. Adicionar Título e Rótulos
    plt.title(f'Top 20 Produtos por Volume Total',fontsize=16)
    plt.xlabel('Produto', fontsize=12)
    plt.ylabel('Volume Total', fontsize=12)

    # Rotacionar os rótulos do eixo X para melhor leitura
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)

    # 6. Melhorar a Legenda
    plt.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')

    # 7. Ajustar o layout e salvar o gráfico
    PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')
    save_path = os.path.join(PATH_GRAFICOS, 'top_produtos_volume.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()

def top_categorias_valor(df):

    # 1. Agrupar os dados por CATEGORIA e somar o Faturamento
    df_faturamento_categoria = df.groupby('CATEGORIA').agg(
        Faturamento_Total=('FATUR_VENDA', 'sum')
    ).reset_index()

    # 2. Ordenar e selecionar as Top 10 categorias
    df_faturamento_categoria = df_faturamento_categoria.sort_values(by='Faturamento_Total', ascending=False)
    df_top_categorias = df_faturamento_categoria.head(10)

    # 3. Criar o gráfico de barras (sem rótulos de porcentagem)
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    bar_plot = sns.barplot(
        data=df_top_categorias,
        x='CATEGORIA',
        y='Faturamento_Total',
        palette='Blues_r'
    )

    # 4. Formatar o eixo Y para Reais (milhões)
    formatter = ticker.FuncFormatter(lambda x, pos: f'R$ {x/1e6:.1f}M')
    bar_plot.yaxis.set_major_formatter(formatter)

    # 5. Adicionar Título e Rótulos
    plt.title('Top 10 Categorias por Faturamento Total (R$)', fontsize=16)
    plt.xlabel('Categoria', fontsize=12)
    plt.ylabel('Faturamento Total (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()