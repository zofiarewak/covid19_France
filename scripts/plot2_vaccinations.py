import pandas as pd
import plotly.graph_objects as go

file_name = "../data/epidemic_data_cleaned.csv"
df = pd.read_csv(file_name)
df['date'] = pd.to_datetime(df['date'])

df_france = df[df['country'] == 'France'].sort_values('date')
df_europe = df[df['country'] == 'Europe'].sort_values('date')

france_yearly = df_france.groupby(df_france['date'].dt.year.rename('Year')).last().reset_index()
europe_yearly = df_europe.groupby(df_europe['date'].dt.year.rename('Year')).last().reset_index()

france_yearly = france_yearly[france_yearly['Year'] >= 2020]
europe_yearly = europe_yearly[europe_yearly['Year'] >= 2020]

years = france_yearly['Year'].tolist()

fig = go.Figure()

# bar for France
fig.add_trace(go.Bar(
    x=years,
    y=france_yearly['total_vaccinations_per_hundred'],
    name='France',
    marker_color='#1f77b4',
    offsetgroup=1,
    hovertemplate='<b>France</b><br>Year: %{x}<br>Vaccinations: %{y:.1f} per 100<extra></extra>'
))

# bar for Europe (mean)
fig.add_trace(go.Bar(
    x=years,
    y=europe_yearly['total_vaccinations_per_hundred'],
    name='Europe (mean)',
    marker_color='#ff7f0e',
    offsetgroup=2,
    hovertemplate='<b>Europe</b><br>Year: %{x}<br>Vaccinations: %{y:.1f} per 100<extra></extra>'
))

fig.update_layout(
    title={
        'text': "Total vaccinations per 100 people (Year-end status)",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=20, family="Arial", color="black")
    },
    xaxis=dict(
        title=dict(
            text="Year",
            font=dict(size=14, family="Arial", color="black")
        ),
        tickfont=dict(size=12),
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
    barmode='group',
    bargap=0.3,
    legend=dict(
        font=dict(size=12),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    template="plotly_white",
    height=500,
    margin=dict(t=90, b=40, l=50, r=20)
)

fig.update_traces(
    texttemplate='%{y:.1f}', 
    textposition='outside', 
    textfont=dict(size=11, color='black')
)

output_html = "../plots/plot2_vaccinations.html"
fig.write_html(output_html, include_plotlyjs='cdn')



