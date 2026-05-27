import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

df = pd.read_csv('../data/epidemic_data_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])

df_france = df[(df['country'] == 'France') & (df['date'] <= '2024-12-31')].dropna(subset=['new_cases_smoothed_per_million']).copy()
df_france['days'] = (df_france['date'] - df_france['date'].min()).dt.days

X = df_france[['days']].values
y = df_france['new_cases_smoothed_per_million'].values

poly_features_full = PolynomialFeatures(degree=3)
X_poly_full = poly_features_full.fit_transform(X)
model_full = LinearRegression()
model_full.fit(X_poly_full, y)
y_pred_full = model_full.predict(X_poly_full)

df_period1 = df_france[df_france['date'] <= '2022-12-31']
X_p1 = df_period1[['days']].values
y_p1 = df_period1['new_cases_smoothed_per_million'].values

poly_features_p1 = PolynomialFeatures(degree=2)
X_poly_p1 = poly_features_p1.fit_transform(X_p1)
model_p1 = LinearRegression()
model_p1.fit(X_poly_p1, y_p1)

X_poly_extrapolated = poly_features_p1.transform(X)
y_pred_extrapolated = model_p1.predict(X_poly_extrapolated)
y_pred_extrapolated_clipped = np.clip(y_pred_extrapolated, 0, None)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_france['date'], y=y,
    mode='lines', name='Actual COVID-19 cases',
    line=dict(color='lightgray', width=1.5), opacity=0.7,
    hovertemplate='<b>Actual</b><br>Date: %{x}<br>Cases: %{y:.1f}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=df_france['date'], y=y_pred_full,
    mode='lines', name='Regression (Full 2020-2024)',
    line=dict(color='forestgreen', width=3),
    hovertemplate='<b>Full Model</b><br>Date: %{x}<br>Trend: %{y:.1f}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=df_france['date'], y=y_pred_extrapolated_clipped,
    mode='lines', name='Forecast (Based on 2020-2022)',
    line=dict(color='firebrick', width=2.5, dash='dash'),
    hovertemplate='<b>Forecast Model</b><br>Date: %{x}<br>Predicted: %{y:.1f}<extra></extra>'
))

fig.update_layout(
    title={
        'text': 'Trend Predictions & Pandemic Decline (France)',
        'y': 0.95, 
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=20, family="Arial", color="black")
    },
    xaxis_title='Date',
    yaxis_title='New cases per million',
    hovermode="x unified",
    template="plotly_white",
    
    legend=dict(
        orientation="h", 
        yanchor="top", 
        y=-0.25,
        xanchor="center", 
        x=0.5,
        font=dict(size=11)
    ),
    height=500,
    
    margin=dict(t=60, b=120, l=60, r=20), 
    
    xaxis=dict(
        range=['2020-01-01', '2024-12-31'],
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, max(y) + 500],
        tickfont=dict(size=12),
        gridcolor='rgba(200, 200, 200, 0.3)'
    )
)

output_html = "../plots/05_inference_period.html"
fig.write_html(output_html, include_plotlyjs='cdn')



