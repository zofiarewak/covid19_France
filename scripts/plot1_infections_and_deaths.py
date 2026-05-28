import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

file_name = "../data/epidemic_data_cleaned.csv"
df = pd.read_csv(file_name)
df['date'] = pd.to_datetime(df['date'])

df_france = df[df['country'] == 'France'].sort_values('date')
df_europe = df[df['country'] == 'Europe'].sort_values('date')

fig = make_subplots(
    rows=2, cols=1, 
    shared_xaxes=True, 
    vertical_spacing=0.12,
    subplot_titles=(
        "<b>Daily infections per million inhabitants (7-day average)</b>", 
        "<b>Daily deaths per million inhabitants (7-day average)</b>"
    )
)

fig.add_trace(go.Scatter(
    x=df_france['date'], y=df_france['new_cases_smoothed_per_million'],
    name='France (Cases)', mode='lines', line=dict(color='#1f77b4', width=2),
    hovertemplate='<b>France</b><br>Date: %{x}<br>Cases: %{y:.1f}<extra></extra>'
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df_europe['date'], y=df_europe['new_cases_smoothed_per_million'],
    name='Europe (Cases)', mode='lines', line=dict(color='#ff7f0e', width=2, dash='dash'),
    hovertemplate='<b>Europe</b><br>Date: %{x}<br>Cases: %{y:.1f}<extra></extra>'
), row=1, col=1)


fig.add_trace(go.Scatter(
    x=df_france['date'], y=df_france['new_deaths_smoothed_per_million'],
    name='France (Deaths)', mode='lines', line=dict(color='#d62728', width=2),
    hovertemplate='<b>France</b><br>Date: %{x}<br>Deaths: %{y:.1f}<extra></extra>'
), row=2, col=1)


fig.add_trace(go.Scatter(
    x=df_europe['date'], y=df_europe['new_deaths_smoothed_per_million'],
    name='Europe (Deaths)', mode='lines', line=dict(color='#2ca02c', width=2, dash='dash'),
    hovertemplate='<b>Europe</b><br>Date: %{x}<br>Deaths: %{y:.1f}<extra></extra>'
), row=2, col=1)


fig.update_layout(
    title={
        'text': "Infection Waves & Mortality Dynamics",
        'y': 0.97,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=30, family="Arial", color="black", weight="bold")
    },
    template="plotly_white",
    hovermode="x unified",
    
    height=680, 
    margin=dict(t=120, b=140, l=110, r=40),
    
    hoverlabel=dict(
        font_size=15,
        font_family="Arial"
    ),
    
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.22, 
        xanchor="center",
        x=0.5,
        font=dict(size=16) 
    )
)

fig.add_annotation(
    text="<b>Cases (per million)</b>",
    textangle=-90,
    x=-0.09,
    y=0.5,
    xref="paper",
    yref="y domain",
    showarrow=False,
    font=dict(size=20, family="Arial", color="black")
)


fig.add_annotation(
    text="<b>Deaths (per million)</b>",
    textangle=-90,
    x=-0.09,
    y=0.5,
    xref="paper",
    yref="y2 domain",
    showarrow=False,
    font=dict(size=20, family="Arial", color="black")
)

fig.update_annotations(font_size=22, font_family="Arial")


fig.update_yaxes(row=1, col=1, tickfont=dict(size=16), gridcolor='rgba(200, 200, 200, 0.3)')
fig.update_yaxes(row=2, col=1, tickfont=dict(size=16), gridcolor='rgba(200, 200, 200, 0.3)')

fig.update_xaxes(title_text="<b>Date</b>", row=2, col=1, title_font=dict(size=22), tickfont=dict(size=16), tickangle=-45, gridcolor='rgba(200, 200, 200, 0.3)')
fig.update_xaxes(row=1, col=1, gridcolor='rgba(200, 200, 200, 0.3)') 

output_html = "../plots/plot1_infections_and_deaths.html"
fig.write_html(output_html, include_plotlyjs='cdn')


