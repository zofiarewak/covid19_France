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


#period 1 for comparison- 2020-2022, how did the decline of pandemic impact the regression model?
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
    mode='lines', name='Actual COVID-19 cases (2020-2024)',
    line=dict(color='lightgray', width=1.5), opacity=0.7
))

fig.add_trace(go.Scatter(
    x=df_france['date'], y=y_pred_full,
    mode='lines', name='Regression model (Full period: 2020-2024)',
    line=dict(color='forestgreen', width=3)
))

fig.add_trace(go.Scatter(
    x=df_france['date'], y=y_pred_extrapolated_clipped,
    mode='lines', name='Forecast from 2020-2022 model (Extrapolation)',
    line=dict(color='firebrick', width=2.5, dash='dash')
))

fig.update_layout(
    title='Inferential Statistics: Impact of Pandemic Decline on Trend Predictions in France',
    xaxis_title='Date',
    yaxis_title='New cases per million (7-day smoothed)',
    hovermode="x unified",
    legend=dict(x=0.01, y=0.99),
    xaxis=dict(range=['2020-01-01', '2024-12-31']), # Strictly enforces timeline up to end of 2024
    yaxis=dict(range=[0, max(y) + 500]) 
)

fig.write_html("../html/05_inference_period.html")
fig.write_image("../data/05_inference_period.png", scale=3) 

print("Regression model for 2020-2024 is done")