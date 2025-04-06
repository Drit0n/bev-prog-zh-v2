# -----------------------------------------------------------------------------
# routes.py – Zentrale Flask-Routen-Logik für bev-prog-zh
#
# Diese Datei verarbeitet HTTP-Anfragen, steuert die Benutzerlogik,
# ruft Prognosen auf Basis von Region, Altersgruppe und Zeitraum ab
# und berechnet zusätzlich dynamische Insight-Karten für die Weboberfläche.
# -----------------------------------------------------------------------------



from flask import Blueprint, render_template, request
import pandas as pd
from .forecast import make_forecast
from .database import get_data  # MongoDB Integration

bp = Blueprint('main', __name__, template_folder='../frontend')

@bp.route('/', methods=['GET'])
def index():
    region = request.args.get('region', 'all')
    age = request.args.get('age', 'all')
    horizon = int(request.args.get('horizon', 5))

    forecast_data = make_forecast(region, age, horizon)

    # Daten aus MongoDB laden 
    df_filtered = get_data(region, age)

    # Sicherstellen, dass Jahr als int verfügbar ist
    df_filtered['jahr'] = df_filtered['jahr'].astype(int)

    # ---- Langfristiger Trend (2010–2024) ----
    df_total = df_filtered.groupby('jahr')['anzahl'].sum()
    pop_2010 = df_total.get(2010, 0)
    pop_2024 = df_total.get(2024, 0)
    if pop_2010 > 0:
        langfristiger_wachstum = round(((pop_2024 - pop_2010) / pop_2010) * 100, 2)
    else:
        langfristiger_wachstum = "n/a"

    # ---- Spitzenjahr ----
    df_total_pct = df_total.pct_change() * 100
    if not df_total_pct.dropna().empty:
        spitzenjahr = df_total_pct.idxmax()
        max_wachstumsrate = round(df_total_pct.max(), 2)
    else:
        spitzenjahr = "n/a"
        max_wachstumsrate = "n/a"

    # ---- Altersstruktur 2024 ----
    df_2024 = df_filtered[df_filtered['jahr'] == 2024]
    if not df_2024.empty:
        gruppe = df_2024.groupby('alter')['anzahl'].sum()
        top_altersgruppe = gruppe.idxmax()
        anzahl_personen = int(gruppe.max())
    else:
        top_altersgruppe = "n/a"
        anzahl_personen = "n/a"

    # ---- Prognose Insight ----
    start_year = 2025
    end_year = start_year + horizon
    forecast_df = pd.DataFrame(forecast_data)
    forecast_df['jahr'] = pd.to_datetime(forecast_df['ds']).dt.year
    future_rows = forecast_df[(forecast_df['jahr'] >= start_year) & (forecast_df['jahr'] <= end_year)]

    if not future_rows.empty:
        erste = future_rows.iloc[0]['yhat']
        letzte = future_rows.iloc[-1]['yhat']
        absolute_growth = letzte - erste
        percent_growth = round((absolute_growth / erste) * 100, 2)
        avg_annual_growth = round(percent_growth / (horizon if horizon > 0 else 1), 2)
        if percent_growth > 1:
            prognose_text = f"Wachstum 🟢 +{percent_growth}% (+{int(absolute_growth)} Personen)"
        elif percent_growth < -1:
            prognose_text = f"Rückgang 🔻 {percent_growth}%"
        else:
            prognose_text = f"Stabil ➖ Veränderung: {percent_growth}%"
    else:
        prognose_text = "⚠️ Keine Prognosedaten"
        avg_annual_growth = "-"
        percent_growth = "n/a"

    # ---- Insight-Kommentare ----
    # Trend
    if langfristiger_wachstum == "n/a":
        trend_comment = ""
    elif langfristiger_wachstum >= 20:
        trend_comment = "➡️ Sehr stark wachsender Trend über viele Jahre."
    elif langfristiger_wachstum >= 10:
        trend_comment = "➡️ Kontinuierliches und stabiles Wachstum."
    elif langfristiger_wachstum >= 3:
        trend_comment = "➡️ Leicht ansteigende Bevölkerungszahl."
    else:
        trend_comment = "➡️ Kaum Wachstum über die Jahre."

    # Spitzenjahr
    if spitzenjahr != "n/a":
        if max_wachstumsrate >= 3:
            spitzenjahr_comment = "➡️ Aussergewöhnliches Boom-Jahr."
        elif max_wachstumsrate >= 1:
            spitzenjahr_comment = "➡️ Gesundes Wachstum im Spitzenjahr."
        elif max_wachstumsrate > 0:
            spitzenjahr_comment = "➡️ Geringes Wachstum im Spitzenjahr."
        else:
            spitzenjahr_comment = "➡️ Keine nennenswerte Veränderung."
    else:
        spitzenjahr_comment = ""

    # Altersstruktur
    if top_altersgruppe != "n/a":
        altersgruppe_num = int(top_altersgruppe.split("_")[0])
        if altersgruppe_num >= 65:
            altersstruktur_comment = "➡️ Region mit überdurchschnittlich vielen Senioren."
        elif altersgruppe_num <= 19:
            altersstruktur_comment = "➡️ Hoher Anteil an Kindern und Jugendlichen."
        elif 20 <= altersgruppe_num <= 44:
            altersstruktur_comment = "➡️ Überwiegend junge Erwerbstätige."
        else:
            altersstruktur_comment = "➡️ Gut durchmischte Altersstruktur."
    else:
        altersstruktur_comment = ""

    # Prognose
    if percent_growth != "n/a" and percent_growth != "-":
        if percent_growth > 10:
            prognose_comment = "➡️ Prognose zeigt starkes Bevölkerungswachstum."
        elif percent_growth > 3:
            prognose_comment = "➡️ Prognostiziertes moderates Wachstum."
        elif percent_growth > 0:
            prognose_comment = "➡️ Leicht wachsend laut Prognose."
        elif percent_growth < -2:
            prognose_comment = "➡️ Möglicher Rückgang der Bevölkerung."
        else:
            prognose_comment = "➡️ Prognose zeigt stagnierende Entwicklung."
    else:
        prognose_comment = ""

    # ---- Insights für Template ----
    insights = [
        {
            "title": "📈 Langfristiger Trend (2010–2024)",
            "color": "primary",
            "text1": f"Wachstum um +{langfristiger_wachstum:.2f}%." if langfristiger_wachstum != "n/a" else "⚠️ Keine Daten für diesen Zeitraum.",
            "text2": trend_comment
        },
        {
            "title": "🏆 Spitzenjahr",
            "color": "success",
            "text1": f"Jahr {spitzenjahr} mit +{max_wachstumsrate}% Wachstum." if spitzenjahr != "n/a" else "⚠️ Keine Daten verfügbar.",
            "text2": spitzenjahr_comment
        },
        {
            "title": "👥 Altersstruktur 2024",
            "color": "secondary",
            "text1": f"Grösste Gruppe: {top_altersgruppe.replace('_','-')} Jahre mit {anzahl_personen} Personen." if top_altersgruppe != "n/a" else "⚠️ Keine Daten für 2024.",
            "text2": altersstruktur_comment
        },
        {
            "title": "📊 Prognose ab 2025",
            "color": "info",
            "text1": prognose_text,
            "text2": prognose_comment
        }
    ]

    # 🔵 Regionen + Altersgruppen aus MongoDB laden
    df_all = get_data()
    regions = df_all['region'].unique()
    altersgruppen = df_all['alter'].unique()

    return render_template('index.html',
                           region=region,
                           age=age,
                           horizon=horizon,
                           forecast=forecast_data,
                           forecast_json=forecast_data,
                           regions=regions,
                           altersgruppen=altersgruppen,
                           insights=insights)
