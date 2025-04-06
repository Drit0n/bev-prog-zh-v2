import pandas as pd
from prophet import Prophet
from .database import get_data  # MongoDB-Datenquelle

def make_forecast(region, altersgruppe, horizon):
    # 🔵 Hole die Daten aus MongoDB
    df_filtered = get_data(region, altersgruppe)

    if df_filtered.empty:
        return []  # Keine Prognose möglich

    # Daten vorbereiten für Prophet
    df_grouped = df_filtered.groupby('jahr')['anzahl'].sum().reset_index()
    df_grouped.rename(columns={'jahr': 'ds', 'anzahl': 'y'}, inplace=True)
    df_grouped['ds'] = pd.to_datetime(df_grouped['ds'], format='%Y')

    # Prophet Modell trainieren
    model = Prophet(yearly_seasonality=False)
    model.fit(df_grouped)

    # Zukunftsdaten für den Forecast erstellen
    future = model.make_future_dataframe(periods=horizon, freq='YE')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
