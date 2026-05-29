import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

data = "../data/owid-covid-data.csv"
df = pd.read_csv(data, usecols=['location', 'date', 'new_cases_smoothed_per_million', 'people_vaccinated_per_hundred'])

df = df[df['location'].isin(['France', 'Poland'])].copy()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['location', 'date'])

# vaccination data were reported irregularly
df['people_vaccinated_per_hundred'] = df.groupby('location')['people_vaccinated_per_hundred'].ffill().fillna(0)
df['new_cases_smoothed_per_million'] = df.groupby('location')['new_cases_smoothed_per_million'].fillna(0)

# we indicate that the average should be calculated only for numerical values
df_fr = df[df['location'] == 'France'].set_index('date').resample('W').mean(numeric_only=True)
df_pl = df[df['location'] == 'Poland'].set_index('date').resample('W').mean(numeric_only=True)

# we only take common dates
common_dates = df_fr.index.intersection(df_pl.index)
df_fr = df_fr.loc[common_dates]
df_pl = df_pl.loc[common_dates]

fig, ax = plt.subplots(figsize=(12, 7))

max_x = max(df_fr['people_vaccinated_per_hundred'].max(), df_pl['people_vaccinated_per_hundred'].max()) * 1.05
max_y = max(df_fr['new_cases_smoothed_per_million'].max(), df_pl['new_cases_smoothed_per_million'].max()) * 1.05

def update(frame):
    ax.clear()
    

    fr_sub = df_fr.iloc[:frame+1]
    pl_sub = df_pl.iloc[:frame+1]
    
    # drawing the history line
    ax.plot(fr_sub['people_vaccinated_per_hundred'], fr_sub['new_cases_smoothed_per_million'], 
            color='blue', alpha=0.4, linestyle='-', linewidth=2, label='France (history)')
    ax.plot(pl_sub['people_vaccinated_per_hundred'], pl_sub['new_cases_smoothed_per_million'], 
            color='red', alpha=0.4, linestyle='-', linewidth=2, label='Poland (history)')
    
    # drawing the current point in time
    if len(fr_sub) > 0:
        ax.scatter(fr_sub['people_vaccinated_per_hundred'].iloc[-1], fr_sub['new_cases_smoothed_per_million'].iloc[-1], 
                   color='blue', s=120, edgecolor='black', zorder=5, label='France (currently)')
    if len(pl_sub) > 0:
        ax.scatter(pl_sub['people_vaccinated_per_hundred'].iloc[-1], pl_sub['new_cases_smoothed_per_million'].iloc[-1], 
                   color='red', s=120, edgecolor='black', zorder=5, label='Poland (currently)')
        
    # date in the corner
    current_date = common_dates[frame].strftime('%Y-%m-%d')
    ax.text(0.03, 0.95, f"Date: {current_date}", transform=ax.transAxes, fontsize=16, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))
    

    ax.set_title('COVID-19: Disease incidence and vaccination coverage', fontsize=25, fontweight='bold')
    ax.set_xlabel('Percentage of population vaccinated with at least one dose (%)', fontsize=18)
    ax.set_ylabel('New cases per million inhabitants (7-day average)', fontsize=18)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    ax.set_xlim(-2, max_x)
    ax.set_ylim(-50, max_y)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=14)
    
    plt.tight_layout()


ani = animation.FuncAnimation(fig, update, frames=len(common_dates), interval=120)


output_filename = '../plots/plot_new_cases_vaccinations.gif'
ani.save(output_filename, writer='pillow', dpi=100)

update(len(common_dates) - 1)
plt.savefig('../plots/plot_new_cases_vaccinations.png', dpi=300, bbox_inches='tight')


