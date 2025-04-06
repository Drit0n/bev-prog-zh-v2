# -----------------------------------------------------------------------------
# model.py – Training von Prophet-Modellen für Bevölkerungsprognose
#
# Dieses Skript lädt die Bevölkerungsdaten aus MongoDB, trainiert für jede
# Kombination aus Region und Altersgruppe ein eigenes Prophet-Modell und speichert
# diese als .pkl-Dateien. Zusätzlich wird ein kombiniertes Gesamtmodell über alle
# Daten hinweg trainiert und gespeichert.
#
# Einsatz im Rahmen der Web-App „bev-prog-zh“ (Flask + Prophet + MongoDB + Azure)
# -----------------------------------------------------------------------------


import pandas as pd
from prophet import Prophet
import pickle
import os
import sys

# Füge das übergeordnete Verzeichnis dem Suchpfad hinzu,
# sodass das 'backend'-Modul gefunden wird.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import get_data  # Holt Daten direkt aus MongoDB

def train_model():
    try:
        # MongoDB-Daten laden
        df = get_data()  # alle Daten abrufen (ohne Filter)
        
        # Sicherstellen, dass Daten vorhanden sind
        if df.empty:
            print("⚠️ Keine Daten in der MongoDB vorhanden!")
            return
        
        # Output-Verzeichnis erstellen
        os.makedirs('backend/static', exist_ok=True)
        os.makedirs('model', exist_ok=True)  # <--- neu für combined model

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

                # Safe Filename erstellen
                region_safe = region.replace(" ", "_").replace("/", "_")
                model_path = f'backend/static/forecast_{region_safe}_{age}.pkl'
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)

                print(f"✅ Modell gespeichert für {region} - {age}")
        
        # 📦 Kombiniertes Modell über alle Daten
        print("🔄 Trainiere kombiniertes Gesamtmodell über alle Daten...")
        df_all = df.groupby('jahr')['anzahl'].sum().reset_index()
        df_all.rename(columns={'jahr': 'ds', 'anzahl': 'y'}, inplace=True)
        df_all['ds'] = pd.to_datetime(df_all['ds'], format='%Y')

        combined_model = Prophet(yearly_seasonality=False)
        combined_model.fit(df_all)

        combined_model_path = 'model/region_age_combined_model.pkl'
        with open(combined_model_path, 'wb') as f:
            pickle.dump(combined_model, f)

        print(f"✅ Kombiniertes Modell gespeichert unter {combined_model_path}")
                
    except Exception as e:
        print(f"Fehler: {str(e)}")

if __name__ == "__main__":
    train_model()
    print("✅ Modelltraining abgeschlossen!")
    print("✅ Alle Modelle erfolgreich trainiert und gespeichert.")