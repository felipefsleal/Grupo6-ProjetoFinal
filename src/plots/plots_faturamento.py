import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import os

PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')

def plot_faturamento_mensal_linha(df_vendas):
    df = df_vendas.copy()
    
    df['MES_NUM'] = df['DATA_ATEND'].dt.month

    # Mapeamento dos meses
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }

    df['MES_NOME'] = df['MES_NUM'].map(mes_map)

    # Lista ordenada dos nomes dos meses para usar no gráfico
    meses_ordenados = list(mes_map.values())

    df_agregado = df.groupby('MES_NOME')['FATUR_VENDA'].sum().reset_index()
    
    # Garante a ordem correta para plotagem
    df_agregado['MES_NOME'] = pd.Categorical(
        df_agregado['MES_NOME'], 
        categories=meses_ordenados, 
        ordered=True
    )
    df_agregado = df_agregado.sort_values('MES_NOME')

    plt.figure(figsize=(14, 7))
    sns.set_style("whitegrid")

    # Cria o gráfico de linha
    ax = sns.lineplot(
        data=df_agregado,
        x='MES_NOME',
        y='FATUR_VENDA',
        color='#0072B2',
        marker='o',
        markersize=8,
        linewidth=2.5
    )

    ax.set_title('Faturamento Mensal (2024)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Faturamento (em milhares de R$)', fontsize=12)

    # Formata o Eixo Y para "K"
    formatter = ticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K')
    ax.yaxis.set_major_formatter(formatter)

    # Loop para anotações
    for index, row in df_agregado.iterrows():
        
        # --- CORREÇÃO: Adiciona o "K" ao texto da caixa ---
        valor_milhar_str = f"{row['FATUR_VENDA']/1000:.0f}K"
        
        ax.annotate(
            text=valor_milhar_str, # Usa a string formatada com "K"
            xy=(row['MES_NOME'], row['FATUR_VENDA']), 
            xytext=(0, -20), 
            textcoords='offset points', 
            ha='center',
            va='top', 
            fontsize=9,
            fontweight='bold',
            color='#004C75',
            bbox=dict(facecolor='#E0F2FF',
                      alpha=0.7, 
                      boxstyle='square,pad=0.3')
        )

    plt.tight_layout()
    plt.show()
    plt.close()

def faturamento_mensal(df_vendas):
    df = df_vendas.copy()
    
    df['MES_NUM'] = df['DATA_ATEND'].dt.month

    # Mapeamento dos meses
    mes_map = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }

    df['MES_NOME'] = df['MES_NUM'].map(mes_map)

    # Lista ordenada dos nomes dos meses para usar no gráfico
    meses_ordenados = list(mes_map.values())

    df_agregado = df.groupby('MES_NOME')['FATUR_VENDA'].sum().reset_index()
    
    # Garante a ordem correta para plotagem
    df_agregado['MES_NOME'] = pd.Categorical(
        df_agregado['MES_NOME'], 
        categories=meses_ordenados, 
        ordered=True
    )
    df_agregado = df_agregado.sort_values('MES_NOME')

    plt.figure(figsize=(14, 7))

    # Cria o gráfico de barras
    ax = sns.barplot(
        data=df_agregado,
        x='MES_NOME',      
        y='FATUR_VENDA',  
        hue='MES_NOME',
        order=meses_ordenados, 
        palette='Blues_r',
        legend=False
    )

    ax.set_title('Faturamento Mensal (2024)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Faturamento (R$)', fontsize=12)

    formatter = ticker.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K')
    ax.yaxis.set_major_formatter(formatter)

    plt.tight_layout()
    plt.show()
    plt.close()