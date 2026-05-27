import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('../data/owid-covid-data.csv')

# filtering data for France, years 2020-2024
df['date'] = pd.to_datetime(df['date'])
df_france = df[(df['location'] == 'France') & (df['date'] <= '2024-12-31')].copy()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=df_france['date'], 
        y=df_france['new_cases_smoothed_per_million'],
        name="New covid19 cases",
        line=dict(color='royalblue', width=2),
        fill='tozeroy', 
        opacity=0.4
    ),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(
        x=df_france['date'], 
        y=df_france['stringency_index'],
        name="Stringency Index",
        line=dict(color='firebrick', width=3, shape='hv'),
    ),
    secondary_y=True,
)

fig.update_layout(
    title='France: Covid-19 cases vs. stringency index',
    xaxis_title='Data',
    hovermode="x unified", 
    legend=dict(x=0.01, y=0.99)
)

fig.update_yaxes(title_text="<b>Covid-19 cases</b> (7 days mean / million)", secondary_y=False)
fig.update_yaxes(title_text="<b>Stringency Index</b> (scale 0 - 100)", secondary_y=True)

fig.write_html("../html/04_stringency_vs_cases.html")

fig.write_image("../data/04_stringency_vs_cases.png", scale=3) 

print("Plot 4 generated")