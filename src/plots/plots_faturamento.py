import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import os

PATH_GRAFICOS = os.path.join(os.pardir, 'graphics')

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