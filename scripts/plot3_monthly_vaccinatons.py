import pandas as pd
import plotly.graph_objects as go

file_name = "../data/epidemic_data_cleaned.csv"
df = pd.read_csv(file_name)
df['date'] = pd.to_datetime(df['date'])

df_france = df[df['country'] == 'France'].sort_values('date')
df_europe = df[df['country'] == 'Europe'].sort_values('date')

france_monthly = df_france.groupby(df_france['date'].dt.to_period('M').rename('Period')).last().reset_index()
europe_monthly = df_europe.groupby(df_europe['date'].dt.to_period('M').rename('Period')).last().reset_index()

france_monthly['Year-Month'] = france_monthly['date'].dt.strftime('%Y-%m')
europe_monthly['Year-Month'] = europe_monthly['date'].dt.strftime('%Y-%m')

france_filtered = france_monthly[france_monthly['date'].dt.year.between(2020, 2022)]
europe_filtered = europe_monthly[europe_monthly['date'].dt.year.between(2020, 2022)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=france_filtered['Year-Month'],
    y=france_filtered['total_vaccinations_per_hundred'],
    name='France',
    mode='lines',
    line=dict(width=3, color='#1f77b4'),
    fill='tozeroy', 
    fillcolor='rgba(31, 119, 180, 0.15)', 
    hovertemplate='<b>France</b><br>Month: %{x}<br>Vaccinations: %{y:.1f} per 100<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=europe_filtered['Year-Month'],
    y=europe_filtered['total_vaccinations_per_hundred'],
    name='Europe (mean)',
    mode='lines',
    line=dict(width=3, color='#ff7f0e', dash='dash'),
    fill='tozeroy',
    fillcolor='rgba(255, 127, 14, 0.1)', 
    hovertemplate='<b>Europe</b><br>Month: %{x}<br>Vaccinations: %{y:.1f} per 100<extra></extra>'
))

fig.update_layout(
    title={
        'text': "Monthly vaccination progress per 100 people (2020-2022)",
        'y': 0.95,  # Tytuł wraca na górę, bo ma już pełną swobodę
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=20, family="Arial", color="black")
    },
    xaxis=dict(
        title=dict(
            text="Year-Month",
            font=dict(size=14, family="Arial", color="black")
        ),
        tickfont=dict(size=11),
        tickangle=-45, 
        type='category'
    ),
    yaxis=dict(
        title=dict(
            text="Vaccinations per 100 inhabitants",
            font=dict(size=14, family="Arial", color="black")
        ),
        tickfont=dict(size=12),
        gridcolor='rgba(200, 200, 200, 0.3)'
    ),
    legend=dict(
        orientation="h",
        yanchor="top", 
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    template="plotly_white",
    hovermode="x unified", 
    height=500, 
    margin=dict(t=60, b=80, l=50, r=20) 
)

output_html = "../plots/plot3_monthly_vaccinations.html"
fig.write_html(output_html, include_plotlyjs='cdn')


