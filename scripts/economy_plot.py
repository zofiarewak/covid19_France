import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('../data/owid-covid-data.csv')

df['date'] = pd.to_datetime(df['date'])
df_france = df[(df['location'] == 'France') & (df['date'] <= '2024-12-31')].copy()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=df_france['date'], 
        y=df_france['new_cases_smoothed_per_million'],
        name="New COVID-19 Cases",
        line=dict(color='royalblue', width=2),
        fill='tozeroy', 
        opacity=0.4,
        hovertemplate='Cases: %{y:.1f} per M<extra></extra>'
    ),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(
        x=df_france['date'], 
        y=df_france['stringency_index'],
        name="Stringency Index (Lockdown Strictness)",
        line=dict(color='firebrick', width=3, shape='hv'),
        hovertemplate='Stringency: %{y:.1f}/100<extra></extra>'
    ),
    secondary_y=True,
)

fig.update_layout(
    title={
        'text': 'Government restrictions vs. infection waves (France)',
        'y': 0.96,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=30, family="Arial", color="black", weight="bold") 
    },
    xaxis_title='Date',
    hovermode="x unified", 
    template="plotly_white",

    height=680,
    margin=dict(t=70, b=140, l=70, r=70),
    

    hoverlabel=dict(
        font_size=15,
        font_family="Arial"
    ),

    legend=dict(
        orientation="h",
        yanchor="top", 
        y=-0.18, 
        xanchor="center",
        x=0.5,
        font=dict(size=16) 
    )
)

fig.update_xaxes(
    tickfont=dict(size=16),
    title_font=dict(size=22),
    gridcolor='rgba(200, 200, 200, 0.3)'
)

fig.update_yaxes(
    title_text="<b>COVID-19 cases</b> (7-day mean / million)", 
    secondary_y=False, 
    title_font=dict(size=22),
    tickfont=dict(size=16),
    gridcolor='rgba(200, 200, 200, 0.3)'
)

fig.update_yaxes(
    title_text="<b>Stringency index</b> (scale 0 - 100)", 
    secondary_y=True, 
    title_font=dict(size=22), 
    tickfont=dict(size=16)
)

output_html = "../plots/04_stringency_vs_cases.html"
fig.write_html(output_html, include_plotlyjs='cdn')