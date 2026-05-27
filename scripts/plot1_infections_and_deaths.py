import pandas as pd
import matplotlib.pyplot as plt

file_name = "../data/epidemic_data_cleaned.csv"
df = pd.read_csv(file_name)

df['date'] = pd.to_datetime(df['date'])

df_france = df[df['country'] == 'France'].sort_values('date')
df_europe = df[df['country'] == 'Europe'].sort_values('date')


fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax[0].plot(df_france['date'], df_france['new_cases_smoothed_per_million'], label='France', color='#1f77b4', linewidth=2)

ax[0].plot(df_europe['date'], df_europe['new_cases_smoothed_per_million'], label='Europe (mean)', color='#ff7f0e', linestyle='--', linewidth=2)

ax[0].set_title('Daily infections per million inhabitants (7-day average)', fontsize=18, pad=15, fontweight='bold')
ax[0].set_ylabel('Number of cases (per million)', fontsize=14, fontweight='bold')
ax[0].legend(fontsize=16, loc='upper right')
ax[0].grid(True, linestyle=':', alpha=0.6)
ax[0].tick_params(axis='y', labelsize=14)

# lower chart
ax[1].plot(df_france['date'], df_france['new_deaths_smoothed_per_million'], label='France', color='#d62728', linewidth=2)
ax[1].plot(df_europe['date'], df_europe['new_deaths_smoothed_per_million'], label='Europe (mean)', color='#2ca02c', linestyle='--', linewidth=2)

ax[1].set_title('Daily deaths per million inhabitants (7-day average)', fontsize=18, pad=15, fontweight='bold')
ax[1].set_xlabel('Data', fontsize=16, fontweight='bold')
ax[1].set_ylabel('Number of deaths (per million)', fontsize=14, fontweight='bold')
ax[1].legend(fontsize=16, loc='upper right')
ax[1].grid(True, linestyle=':', alpha=0.6)


plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
fig.align_ylabels()
plt.tight_layout()
plt.savefig('../plots/plot1_infections_and_deaths.png', dpi=300, bbox_inches='tight')


