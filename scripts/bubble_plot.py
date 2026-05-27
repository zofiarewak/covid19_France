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

df_weekly['bubble_size'] = (df_weekly['new_deaths_smoothed_per_million'] * 8) + 20

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
    size_max=45,
    log_x=True,     
    log_y=True,    
    range_x=[1000, df_weekly['total_cases'].max() * 1.3],
    range_y=[1, df_weekly['new_cases_smoothed_per_million'].max() * 1.5],
    title="COVID-19 Trajectory & Mortality Analysis",
    category_orders={"country": ["France", "Europe"]},
    template="plotly_white"
)

fig.update_layout(
    title={
        'text': "COVID-19 Trajectory & Mortality Analysis",
        'y': 0.96,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=18, family="Arial", color="black")
    },
    xaxis_title="Total Cumulative Cases (Log Scale)",
    yaxis_title="New Cases per Million (Log Scale)",
    hovermode="closest",
    
    height=500,
    
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.65,
        xanchor="center",
        x=0.5,
        font=dict(size=11)
    ),
    margin=dict(t=50, b=170, l=50, r=30) 
)

fig.update_xaxes(tickfont=dict(size=10), gridcolor='rgba(200, 200, 200, 0.3)', title_font=dict(size=11))
fig.update_yaxes(tickfont=dict(size=10), gridcolor='rgba(200, 200, 200, 0.3)', title_font=dict(size=11))

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 80  
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 40  

fig.layout.updatemenus[0].pad = dict(t=40, b=10)
fig.layout.updatemenus[0].y = -0.12 

fig.layout.sliders[0].pad = dict(t=40, b=10)
fig.layout.sliders[0].y = -0.12 

output_html = "../plots/06_animated_bubbles.html"
fig.write_html(output_html, include_plotlyjs='cdn')

