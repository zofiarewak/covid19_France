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
    vertical_spacing=0.15,
    subplot_titles=(
        "Daily infections per million inhabitants (7-day average)", 
        "Daily deaths per million inhabitants (7-day average)"))

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
    template="plotly_white",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.12,
        xanchor="right",
        x=1,
        font=dict(size=11)
    ),
    height=500,
    margin=dict(t=100, b=40, l=60, r=20) 
)

fig.update_yaxes(title_text="Cases (per million)", row=1, col=1, title_font=dict(size=12), tickfont=dict(size=11))
fig.update_yaxes(title_text="Deaths (per million)", row=2, col=1, title_font=dict(size=12), tickfont=dict(size=11))
fig.update_xaxes(title_text="Date", row=2, col=1, title_font=dict(size=12), tickfont=dict(size=11), tickangle=-45)


output_html = "../plots/plot1_infections_and_deaths.html"
fig.write_html(output_html, include_plotlyjs='cdn')

