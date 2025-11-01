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


#Funções de Plotagem

def plot_faturamento_total_filial(df_vendas):
    # 1. Agrupamento dos Dados
    df_faturamento_filial = df_vendas.groupby('FILIAL')['FATUR_VENDA'].sum().reset_index()

    # 2. Geração do Gráfico
    plt.figure(figsize=(9, 6))
    ax = sns.barplot(
        data=df_faturamento_filial,
        x='FILIAL',
        y='FATUR_VENDA',
        palette='Blues'
    )

    # 3. Formatação e Rótulos
    ax.set_title('Faturamento Total por Filial (Ano 2024)', fontsize=16)
    ax.set_xlabel('Tipo de Filial', fontsize=12)
    ax.set_ylabel('Faturamento Total (R$)', fontsize=12)

    formatter_currency = ticker.FuncFormatter(lambda x, p: f'R$ {x:,.0f}')
    ax.yaxis.set_major_formatter(formatter_currency)

    for p in ax.patches:
        ax.annotate(f'R$ {p.get_height():,.0f}',
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   xytext=(0, 9),
                   textcoords='offset points',
                   fontsize=10)

    # 4. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, 'faturamento_anual_por_filial.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()

def plot_faturamento_mensal_filial(df_vendas):
    df = df_vendas.copy()
    df['DATA_ATEND'] = pd.to_datetime(df['DATA_ATEND'])
    df['MES_NUM'] = df['DATA_ATEND'].dt.month
    df['MES_NOME'] = df['MES_NUM'].map(MES_MAP)

    # 2. Agrupamento dos Dados
    df_mes_filial = df.groupby(['MES_NOME', 'FILIAL'])['FATUR_VENDA'].sum().reset_index()

    # 3. Geração do Gráfico
    plt.figure(figsize=(14, 7))
    ax = sns.barplot(
        data=df_mes_filial,
        x='MES_NOME',
        y='FATUR_VENDA',
        hue='FILIAL',
        order=MESES_ORDENADOS, # Usa a constante global
        palette='Blues'
    )

    # 4. Formatação e Rótulos
    ax.set_title('Faturamento Mensal por Filial (2024)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Faturamento (R$)', fontsize=12)
    formatter = ticker.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K')
    ax.yaxis.set_major_formatter(formatter)
    ax.legend(title='Filial', loc='upper left')

    # 5. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, 'faturamento_mensal_agrupado.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()

def plot_faturamento_e_ticket_medio_mensal(df_vendas):
    df = df_vendas.copy()
    df['DATA_ATEND'] = pd.to_datetime(df['DATA_ATEND'])
    df['MES_NUM'] = df['DATA_ATEND'].dt.month
    df['MES_NOME'] = df['MES_NUM'].map(MES_MAP)

    # 2. Cálculo - Faturamento (Barras)
    df_mes_filial = df.groupby(['MES_NOME', 'FILIAL'])['FATUR_VENDA'].sum().reset_index()

    # 3. Cálculo - Ticket Médio (Linhas)
    df_agregado_tm = df.groupby(['MES_NUM', 'MES_NOME', 'FILIAL']).agg(
        FATUR_TOTAL=('FATUR_VENDA', 'sum'),
        CLIENTES_UNICOS=('CLI_CPF', 'nunique')
    ).reset_index()
    df_agregado_tm['TICKET_MEDIO'] = df_agregado_tm['FATUR_TOTAL'] / df_agregado_tm['CLIENTES_UNICOS']
    
    df_agregado_tm = df_agregado_tm.sort_values(by='MES_NUM')
    df_tm_rua = df_agregado_tm[df_agregado_tm['FILIAL'] == 'RUA']
    df_tm_shopping = df_agregado_tm[df_agregado_tm['FILIAL'] == 'SHOPPING']

    # 4. Geração do Gráfico Combinado
    palette_colors = sns.color_palette("Spectral")
    color_rua = palette_colors[0]
    color_shopping = palette_colors[1]
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plotagem Gráfico de Barras (Eixo Esquerdo)
    sns.barplot(
        data=df_mes_filial,
        x='MES_NOME',
        y='FATUR_VENDA',
        hue='FILIAL',
        order=MESES_ORDENADOS,
        palette='Blues',
        ax=ax
    )
    ax.set_title('Faturamento Mensal e Ticket Médio por Filial (2024)', fontsize=18)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Faturamento (R$)', fontsize=12, color='gray')
    formatter_k = ticker.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K')
    ax.yaxis.set_major_formatter(formatter_k)
    ax.tick_params(axis='y', labelcolor='gray')

    # Plotagem Gráfico de Linhas (Eixo Direito)
    ax2 = ax.twinx()
    ax2.plot(df_tm_rua['MES_NOME'], df_tm_rua['TICKET_MEDIO'],
             color=color_rua, marker='o', linestyle='--', linewidth=2, label='Ticket Médio RUA')
    ax2.plot(df_tm_shopping['MES_NOME'], df_tm_shopping['TICKET_MEDIO'],
             color=color_shopping, marker='s', linestyle='--', linewidth=2, label='Ticket Médio SHOPPING')

    ax2.set_ylabel('Ticket Médio (R$)', fontsize=12, color=palette_colors[2])
    formatter_tm = ticker.FuncFormatter(lambda x, p: f'R$ {x:.2f}')
    ax2.yaxis.set_major_formatter(formatter_tm)
    ax2.tick_params(axis='y', labelcolor=palette_colors[2])
    ax2.grid(False)

    # 5. Adicionar Rótulos (Caixas)
    vertical_offset = 1
    for _, row in df_tm_rua.iterrows():
        ax2.text(row['MES_NOME'], row['TICKET_MEDIO'] + vertical_offset,
                 f"R$ {row['TICKET_MEDIO']:.2f}", color='white', fontsize=8, fontweight='bold',
                 ha='center', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.3', fc=color_rua, ec='none', alpha=0.8))
    for _, row in df_tm_shopping.iterrows():
        ax2.text(row['MES_NOME'], row['TICKET_MEDIO'] - vertical_offset,
                 f"R$ {row['TICKET_MEDIO']:.2f}", color='white', fontsize=8, fontweight='bold',
                 ha='center', va='top',
                 bbox=dict(boxstyle='round,pad=0.3', fc=color_shopping, ec='none', alpha=0.8))

    # 6. Salvamento e Legenda Combinada
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    l1 = ['Faturamento RUA', 'Faturamento SHOPPING']
    ax.legend(h1 + h2, l1 + l2,
              title='Legenda', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

    fig.tight_layout(rect=[0, 0, 0.85, 1])
    save_path = os.path.join(PATH_GRAFICOS, 'faturamento_e_ticket_medio_mensal.png')
    plt.savefig(save_path)
    plt.show()
    plt.close(fig)


def plot_clientes_unicos_mensal_filial(df_vendas):
    df = df_vendas.copy()
    df['DATA_ATEND'] = pd.to_datetime(df['DATA_ATEND'])
    df['MES_NUM'] = df['DATA_ATEND'].dt.month
    df['MES_NOME'] = df['MES_NUM'].map(MES_MAP)

    # 2. Agrupamento dos Dados
    df_clientes_unicos = df.groupby(['MES_NOME', 'FILIAL'])['CLI_CPF'].nunique().reset_index()

    # 3. Geração do Gráfico
    plt.figure(figsize=(14, 7))
    ax = sns.barplot(
        data=df_clientes_unicos,
        x='MES_NOME',
        y='CLI_CPF',
        hue='FILIAL',
        order=MESES_ORDENADOS,
        palette='Blues'
    )

    # 4. Formatação e Rótulos
    ax.set_title('Número de Clientes Únicos por Mês e Filial (2024)', fontsize=16)
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Número de Clientes Únicos', fontsize=12)

    formatter_k_int = ticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K')
    ax.yaxis.set_major_formatter(formatter_k_int)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}',
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   xytext=(0, 9),
                   textcoords='offset points',
                   fontsize=9)

    ax.legend(title='Filial', loc='upper left')

    # 5. Salvamento
    save_path = os.path.join(PATH_GRAFICOS, 'clientes_unicos_mensal_agrupado.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()