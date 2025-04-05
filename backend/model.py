import pandas as pd
from prophet import Prophet
import pickle
import os
from backend.database import get_data  # MongoDB-Datenquelle

def train_model():
    try:
        # MongoDB-Daten laden
        df = get_data()  # alle Daten abrufen (ohne Filter)
        
        # Sicherstellen, dass Daten vorhanden sind
        if df.empty:
            print("⚠️ Keine Daten in der MongoDB vorhanden!")
            return
        
        # Sicherstellen, dass der 'model' Ordner existiert
        os.makedirs('model', exist_ok=True)

        regions = df['region'].unique()
        ages = df['alter'].unique()

        for region in regions:
            for age in ages:
                df_sub = df[(df['region'] == region) & (df['alter'] == age)]
                if df_sub.empty:
                    print(f"⚠️  Keine Daten für {region} - {age}, überspringe...")
                    continue

                df_grouped = df_sub.groupby('jahr')['anzahl'].sum().reset_index()
                df_grouped.rename(columns={'jahr': 'ds', 'anzahl': 'y'}, inplace=True)
                df_grouped['ds'] = pd.to_datetime(df_grouped['ds'], format='%Y')

                # Prophet-Modell erstellen und trainieren
                model = Prophet(yearly_seasonality=False)
                model.fit(df_grouped)

                # Safe Filename für Region und Altersgruppe erstellen
                region_safe = region.replace(" ", "_").replace("/", "_")
                model_path = f'model/forecast_{region_safe}_{age}.pkl'  # Speichern im model-Ordner
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)

                print(f"✅ Modell gespeichert für {region} - {age}")
        
        # Modell für alle Regionen und Altersgruppen speichern
        # Das Kombinierte Modell speichern
        model_path_combined = 'model/region_age_combined_model.pkl'
        with open(model_path_combined, 'wb') as f:
            pickle.dump(model, f)
        
        print("✅ Kombiniertes Modell gespeichert als 'region_age_combined_model.pkl'")

    except Exception as e:
        print(f"Fehler: {str(e)}")

if __name__ == "__main__":
    train_model()
#     # Beispielaufruf
#     region = "Zürich"
#     altersgruppe = "20-30"
#     horizon = 5
#     forecast_data = make_forecast(region, altersgruppe, horizon)
#     print(forecast_data)