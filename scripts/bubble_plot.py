import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/epidemic_data_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])

countries_to_compare = ['France', 'Europe']
df_filtered = df[(df['country'].isin(countries_to_compare)) & (df['date'] <= '2024-12-31')].copy()

df_filtered = df_filtered.set_index('date')
df_weekly = df_filtered.groupby('country').resample('W').mean(numeric_only=True).reset_index()

df_weekly = df_weekly.sort_values('date')
df_weekly['date_str'] = df_weekly['date'].dt.strftime('%Y-%m-%d')

df_weekly['total_cases'] = df_weekly['total_cases'].fillna(0).clip(lower=100)
df_weekly['new_cases_smoothed_per_million'] = df_weekly['new_cases_smoothed_per_million'].fillna(0).clip(lower=1)
df_weekly['new_deaths_smoothed_per_million'] = df_weekly['new_deaths_smoothed_per_million'].fillna(0)

df_weekly['bubble_size'] = (df_weekly['new_deaths_smoothed_per_million'] * 15) + 35

fig = px.scatter(
    df_weekly,
    x="total_cases",
    y="new_cases_smoothed_per_million",
    animation_frame="date_str", 
    animation_group="country",
    size="bubble_size",        
    color="country", 
    hover_name="country",
    hover_data={
        'total_cases': ':',
        'new_cases_smoothed_per_million': ':.2f',
        'new_deaths_smoothed_per_million': ':.2f',
        'bubble_size': False     
    },
    size_max=120,     
    log_x=True,     
    log_y=True,    
    range_x=[1000, df_weekly['total_cases'].max() * 1.3],
    range_y=[1, df_weekly['new_cases_smoothed_per_million'].max() * 1.5],
    title="Comparative Presentation Timeline: COVID-19 Trajectory & Mortality Analysis",
    category_orders={"country": ["France", "Poland", "Europe"]}
)

fig.update_layout(
    xaxis_title="Total Cumulative Cases (Log Scale)",
    yaxis_title="New Cases per Million (7-day smoothed - Log Scale)",
    hovermode="closest",
    width=1920,   
    height=1080,  
    legend=dict(
        x=0.02, y=0.98, 
        font=dict(size=20),
        bgcolor="rgba(255, 255, 255, 0.7)"
    )
)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 80  
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 40  

fig.write_html("../html/06_animated_bubbles.html")
fig.write_image("../data/06_animated_bubbles.png", scale=3) 

print("bubble plot is done")