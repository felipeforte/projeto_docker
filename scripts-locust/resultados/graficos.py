import pandas as pd
import matplotlib.pyplot as plt

# Configuração do estilo dos gráficos
plt.style.use('default')

# Lista de arquivos a serem lidos
files = [
    'wp_1inst_20usuarios_stats.csv',
    'wp_1inst_100usuarios_stats.csv',
    'wp_1inst_750usuarios_stats.csv',
    'wp_2inst_20usuarios_stats.csv',
    'wp_2inst_100usuarios_stats.csv',
    'wp_2inst_750usuarios_stats.csv',
    'wp_3inst_20usuarios_stats.csv',
    'wp_3inst_100usuarios_stats.csv',
    'wp_3inst_750usuarios_stats.csv'
]

# Listas para armazenar os dados
instances = []
users = []
avg_response_times = []
requests_per_second = []

# Processamento dos arquivos
for file in files:
    parts = file.split('_')
    inst = int(parts[1].replace('inst', ''))
    user = int(parts[2].replace('usuarios', ''))

    df = pd.read_csv(file)
    aggregated = df[df['Name'].astype(str).str.strip() == 'Aggregated']

    if not aggregated.empty:
        instances.append(inst)
        users.append(user)
        avg_response_times.append(aggregated['Average Response Time'].values[0])
        requests_per_second.append(aggregated['Requests/s'].values[0])

# Cria DataFrame consolidado
data = pd.DataFrame({
    'Instances': instances,
    'Users': users,
    'AvgResponseTime': avg_response_times,
    'RequestsPerSecond': requests_per_second
}).sort_values(['Instances', 'Users'])

# === GRÁFICO 1 === #
# Tempo de resposta (y) vs Usuários (x), agrupado por instâncias
fig1, ax1 = plt.subplots(figsize=(7,5))

# Pivot: index = Users, columns = Instances
pivot1 = data.pivot(index='Users', columns='Instances', values='AvgResponseTime')
width = 0.8 / len(pivot1.columns)
x = range(len(pivot1.index))

# Cores suaves no estilo do exemplo
colors = ['#94bde5', '#f3c7a7', '#e5a0a0']

for i, col in enumerate(pivot1.columns):
    ax1.bar(
        [pos + i*width - (len(pivot1.columns)-1)*width/2 for pos in x],
        pivot1[col],
        width=width,
        color=colors[i % len(colors)],
        label=f'{col} instância(s)'
    )

ax1.set_xticks(list(x))
ax1.set_xticklabels(pivot1.index)
ax1.set_xlabel('Número de usuários')
ax1.set_ylabel('Tempo de resposta (s)')
ax1.set_title('Tempo de resposta vs usuários')
ax1.legend()
plt.tight_layout()
plt.savefig('tempo_resposta_barras.png', dpi=300, bbox_inches='tight')

# === GRÁFICO 2 === #
# Throughput (y) vs Instâncias (x), agrupado por usuários
fig2, ax2 = plt.subplots(figsize=(7,5))

pivot2 = data.pivot(index='Instances', columns='Users', values='RequestsPerSecond')
width = 0.8 / len(pivot2.columns)
x = range(len(pivot2.index))
colors = ['#c6d8b6', '#b5c9e6', '#f5d19b']

for i, col in enumerate(pivot2.columns):
    ax2.bar(
        [pos + i*width - (len(pivot2.columns)-1)*width/2 for pos in x],
        pivot2[col],
        width=width,
        color=colors[i % len(colors)],
        label=f'{col} usuário(s)'
    )

ax2.set_xticks(list(x))
ax2.set_xticklabels(pivot2.index)
ax2.set_xlabel('Número de instâncias')
ax2.set_ylabel('Requisições por segundo')
ax2.set_title('Requisições por segundo vs instâncias')
ax2.legend()
plt.tight_layout()
plt.savefig('throughput_barras.png', dpi=300, bbox_inches='tight')

plt.show()
