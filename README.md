# Projekt 1: Bevölkerungsprognose Kanton Zürich 🌍📊

## Überblick

Willkommen zu meinem Projekt zur Bevölkerungsprognose für den Kanton Zürich. Die Anwendung nutzt historische Bevölkerungsdaten und Machine Learning (Prophet), um zukünftige Bevölkerungszahlen basierend auf verschiedenen Faktoren wie Region und Altersgruppe vorherzusagen.

## 📅 Datenquelle

Die Bevölkerungsdaten kommen von [opendata.swiss](https://opendata.swiss/de/dataset/zukunftige-bevolkerung-kanton-zurich-und-regionen-nach-geschlecht-und-alter/resource/ad753801-25e7-4bce-b8ab-a704962c95de), die CSV-Datei wird automatisch gescrapt und in eine MongoDB Atlas-Datenbank hochgeladen.

## 🧠 Machine Learning

Für die Prognose der Bevölkerungsentwicklung wird der **Prophet-Algorithmus** verwendet, der speziell für Zeitreihenanalysen entwickelt wurde.

## 🚀 Funktionsweise

- **Scrapy Spider:** Automatisches Scrapen der CSV von [opendata.swiss](https://opendata.swiss).
- **Datenbank:** MongoDB Atlas zur Speicherung und schnellen Abfrage von Bevölkerungsdaten.
- **Modelltraining:** Prophet-Modelle werden automatisch trainiert und gespeichert, um die Prognose für verschiedene Regionen und Altersgruppen zu berechnen.
- **Frontend:** Die Ergebnisse werden in einer interaktiven Web-App mit Flask und Plotly angezeigt.

## 💻 Installation

1. **Repository klonen:**
    ```bash
    git clone https://github.com/dein-github/bev-prog-zh.git
    ```

2. **Virtuelle Umgebung einrichten:**
    ```bash
    cd bev-prog-zh
    python -m venv venv
    source venv/bin/activate  # Für Mac/Linux
    venv\Scripts\activate  # Für Windows
    ```

3. **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

4. **MongoDB Atlas konfigurieren:**  
   Stelle sicher, dass du eine MongoDB Atlas-Datenbank eingerichtet hast und den Connection-String in den Einstellungen korrekt einfügst.

5. **Flask App starten:**
    ```bash
    flask --app backend run
    ```

## 🔄 Automatisierung

- **GitHub Actions:**  
    - **Auto Scrape & Upload:** Automatisiertes Scraping und Hochladen der CSV-Daten.
    - **Model Training:** Das Training der Prophet-Modelle wird regelmäßig durchgeführt, um die neuesten Daten zu berücksichtigen.

## 📈 Prognose

Die Anwendung ermöglicht es Nutzern, Prognosen über die Bevölkerungsentwicklung zu erhalten, und bietet detaillierte **Insights** zu verschiedenen Trends und Altersgruppen.

## 📚 Weitere Informationen

- **MongoDB Atlas** zur Speicherung der Daten
- **Scrapy** für das Scrapen der Daten
- **Prophet** für das Modelltraining der Zeitreihen

## 🤖 Beitrag leisten

Fühle dich frei, zum Projekt beizutragen, indem du **Issues** erstellst oder **Pull Requests** vorschlägst.

---

Danke für dein Interesse an diesem Projekt! 🌟
