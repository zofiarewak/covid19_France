import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates

data = "../data/owid-covid-data.csv"
df = pd.read_csv(data, usecols=['location', 'date', 'reproduction_rate'])

df = df[df['location'].isin(['France', 'Poland'])].copy()
df['date'] = pd.to_datetime(df['date'])

df_pivot = df.pivot(index='date', columns='location', values='reproduction_rate')

# weekly aggregation (average R rate for a given week)
df_pivot = df_pivot.resample('W').mean(numeric_only=True).dropna()

fig, ax = plt.subplots(figsize=(12, 7))

min_date, max_date = df_pivot.index.min(), df_pivot.index.max()
# we set fixed Y-axis limits around 1.0 for better readability of jumps
max_y = max(df_pivot.max().max() * 1.05, 2.0) 

def update(frame):
    ax.clear()
    
    data_up_to_frame = df_pivot.iloc[:frame+1]
    dates = data_up_to_frame.index
    
    # static line for R=1
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.5, label='Critical threshold (R = 1.0)')
    
    # drawing the R-index lines for France and Poland
    ax.plot(dates, data_up_to_frame['France'], color='hotpink', linewidth=2.5, label='France')
    ax.plot(dates, data_up_to_frame['Poland'], color='teal', linewidth=2.5, label='Poland')
    
    ax.set_title('Epidemic dynamics: Virus reproduction rate (R-value)', fontsize=22, fontweight='bold')
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Reproduction rate (R)', fontsize=18)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    

    ax.set_xlim(min_date, max_date)
    ax.set_ylim(0.2, max_y)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    ax.legend(loc='upper right', fontsize=16)
    
    # date display formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.tight_layout()


ani = animation.FuncAnimation(fig, update, frames=len(df_pivot), interval=90)

ani.save('../plots/covid_r_value_fr_pl.gif', writer='pillow', dpi=100)

update(len(df_pivot) - 1)
plt.savefig('../plots/covid_r_value_fr_pl.png', dpi=300, bbox_inches='tight')







