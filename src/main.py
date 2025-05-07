import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração do estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")

# Carregamento dos dados
try:
    caminho_arquivo = ('assets/Remuneracao_docentes_Brasil_2020.xlsx')
    df = pd.read_excel(caminho_arquivo, engine='openpyxl', header=8)
except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
    exit()

# Pré-processamento e renomeação
df = df.rename(columns={
    'NU_ANO_CENSO': 'ano',
    'NO_CODIGO': 'regiao',
    'DEPENDENCIA': 'dependencia',
    'media': 'remuneracao_media',
    'rem_40_horas': 'remuneracao_40h'
})

# Conversão e filtragem
df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
df = df[['ano', 'regiao', 'dependencia',
         'remuneracao_media', 'remuneracao_40h']].dropna()

# Análise exploratória
print("\n=== Estatísticas Descritivas ===")
print(df.describe())

print("\n=== Contagem por Dependência Administrativa ===")
print(df['dependencia'].value_counts())

# Visualizações
plt.figure(figsize=(15, 10))

# Gráfico 1: Comparação de remuneração média por dependência administrativa
plt.subplot(2, 2, 1)
sns.barplot(
    data=df,
    x='dependencia',
    y='remuneracao_media',
    estimator='mean',
    errorbar=None)
plt.title('Média Salarial por Dependência Administrativa (2020)')
plt.xlabel('Tipo de Instituição')
plt.ylabel('Remuneração Média (R$)')
plt.xticks(rotation=45)

# Gráfico 2: Comparação entre remuneração média e de 40h
plt.subplot(2, 2, 2)
df_melt = df.melt(id_vars=['regiao', 'dependencia'],
                  value_vars=['remuneracao_media', 'remuneracao_40h'],
                  var_name='tipo',
                  value_name='valor')
sns.barplot(data=df_melt, x='dependencia', y='valor', hue='tipo')
plt.title('Comparação entre Remuneração Média e de 40h (2020)')
plt.xlabel('Tipo de Instituição')
plt.ylabel('Valor (R$)')
plt.xticks(rotation=45)
plt.legend(title='Tipo de Remuneração')

# Gráfico 3: Distribuição das remunerações
plt.subplot(2, 2, 3)
sns.boxplot(data=df, x='dependencia', y='remuneracao_media')
plt.title('Distribuição das Remunerações Médias (2020)')
plt.xlabel('Tipo de Instituição')
plt.ylabel('Remuneração (R$)')
plt.xticks(rotation=45)

# Gráfico 4: Dispersão entre remuneração média e de 40h
plt.subplot(2, 2, 4)
sns.scatterplot(
    data=df,
    x='remuneracao_media',
    y='remuneracao_40h',
    hue='dependencia')
plt.title('Relação entre Remuneração Média e de 40h (2020)')
plt.xlabel('Remuneração Média (R$)')
plt.ylabel('Remuneração 40h (R$)')
plt.legend(title='Tipo de Instituição')

plt.tight_layout()
plt.show()

print("\n=== Remuneração Média por Dependência ===")
print(df.groupby('dependencia')[
      'remuneracao_media'].mean().sort_values(ascending=False))


try:
    df.to_csv('remuneracao_tratada.csv', index=False)
    print("\nDados exportados com sucesso para 'remuneracao_tratada.csv'")
except Exception as e:
    print(f"\nErro ao exportar dados: {e}")
