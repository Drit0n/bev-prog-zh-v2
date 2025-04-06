# Projekt 1: Bevölkerungsprognose Kanton Zürich 🌍📊

## Überblick

Willkommen zu meinem Projekt zur **Bevölkerungsprognose für den Kanton Zürich**. Ziel dieses Projekts ist es, zukünftige Bevölkerungszahlen des Kantons Zürich und seiner Regionen basierend auf historischen Daten und maschinellen Lernmodellen vorherzusagen. Die Anwendung nutzt den **Prophet-Algorithmus** für Zeitreihenprognosen und ermöglicht es, fundierte Aussagen zur Bevölkerungsentwicklung über verschiedene Zeiträume und demografische Gruppen hinweg zu treffen.

## 📅 Datenquelle

Die verwendeten Bevölkerungsdaten stammen von der **[opendata.swiss](https://opendata.swiss/de/dataset/zukunftige-bevolkerung-kanton-zurich-und-regionen-nach-geschlecht-und-alter/resource/ad753801-25e7-4bce-b8ab-a704962c95de)** Plattform. Die CSV-Datei, die jährlich aktualisierte Daten zur Bevölkerungsentwicklung nach Region, Altersgruppe und Geschlecht enthält, wird **automatisch** gescrapt und in eine **MongoDB Atlas-Datenbank** hochgeladen.

## 🧠 Machine Learning

Für die **Prognose der Bevölkerungsentwicklung** wird der **Prophet-Algorithmus** verwendet. Prophet ist ein Open-Source-Tool von Facebook, das speziell für die Analyse und Vorhersage von Zeitreihendaten entwickelt wurde. Es ermöglicht eine robuste Prognose, auch wenn die Daten saisonale Muster oder Feiertagseffekte aufweisen.

### Funktionen des Modells:
- **Zeitraum:** Die Prognosen können für verschiedene Zeiträume (z. B. 5, 10, 15 Jahre) durchgeführt werden.
- **Regionen und Altersgruppen:** Das Modell berechnet Prognosen basierend auf spezifischen Regionen und Altersgruppen, die von den Nutzern der Web-App ausgewählt werden können.

## 🚀 Funktionsweise

### **1. Scrapy Spider:**
Der **Scrapy Spider** extrahiert automatisch die CSV-Datei von der Webseite **opendata.swiss**. Der Spider sucht nach dem Link zur CSV-Datei und lädt sie auf den lokalen Server herunter.

### **2. Datenbank:**
Die heruntergeladene CSV-Datei wird in eine **MongoDB Atlas-Datenbank** importiert. Diese Datenbank bietet eine schnelle Möglichkeit zur Abfrage und Filterung von Bevölkerungsdaten basierend auf verschiedenen Parametern (z. B. Region, Altersgruppe, Jahr).

### **3. Modelltraining:**
Das **Prophet-Modell** wird regelmäßig neu trainiert, um die neuesten verfügbaren Daten in die Prognosen zu integrieren. Modelle werden für jede Region und Altersgruppe gespeichert und können dann in der Web-App abgerufen werden.

### **4. Frontend:**
Die Web-App zeigt die prognostizierten Bevölkerungszahlen interaktiv in einer **Plotly-Visualisierung**. Nutzer können auswählen, welche Region und Altersgruppe sie analysieren möchten, und die Web-App zeigt sowohl historische als auch prognostizierte Daten an.

## 📂 Projektstruktur

```
bev-prog-zh/
├── app.py                  # Einstiegspunkt der App
├── backend/                # Business-Logik und Datenverarbeitung
│   ├── routes.py
│   ├── model.py
│   ├── forecast.py
│   ├── database.py
│   └── static/             # Forecast-Modelle (.pkl)
├── templates/              # HTML-Templates für das Dashboard
│   ├── base.html
│   ├── index.html
│   └── insights.html
├── data/                   # Originaldaten (CSV)
├── static/                 # Styles, ggf. Icons
├── .github/workflows/      # GitHub Actions für CI/CD
├── Dockerfile              # Docker für Azure-Deployment
├── docker-compose.yml      # Lokales Multi-Container-Setup
└── requirements.txt        # Python-Abhängigkeiten
```

## 🧰 Verwendete Technologien

| Technologie     | Funktion                                    |
|----------------|---------------------------------------------|
| Python 3.10     | Programmiersprache                          |
| Flask           | Web-Framework (Backend/API)                |
| Prophet         | Zeitreihenprognose (ML)                     |
| Plotly          | Interaktive Visualisierung                  |
| Scrapy          | Datenextraktion von opendata.swiss         |
| MongoDB Atlas   | Cloud-Datenbank für Bevölkerungsdaten       |
| GitHub Actions  | CI/CD für Modelltraining und Datenupload    |
| Docker          | Containerisierung & Azure Deployment        |

## 💻 Installation

### 1. **Repository klonen:**
```bash
git clone https://github.com/dein-github/bev-prog-zh-v2.git
```

### 2. Virtuelle Umgebung einrichten:
```bash
cd bev-prog-zh-v2
python -m venv venv
source venv/bin/activate  # Für Mac/Linux
venv\Scripts\activate  # Für Windows
```

### 3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

### 4. MongoDB Atlas konfigurieren:
MongoDB URI in `.env` Datei oder direkt im Code definieren.

### 5. Flask App starten:
```bash
flask --app backend run
```

## 🔄 Automatisierung

### GitHub Actions:
- **Auto Scrape & Upload:** Automatisches Scraping und Upload in MongoDB
- **Model Training:** Automatisches Training neuer Forecast-Modelle

## 📈 Prognose & Einblicke

### Dynamische Insights:
- ✈️ **Langfristiger Trend**
- 🌟 **Spitzenjahr**
- 🧴 **Altersstruktur**
- 📈 **Prognosewachstum**

## 📊 KPI-Definitionen im Dashboard

- **Gesamtbevölkerung:** Summe aller Altersgruppen
- **Ø Wachstum:** Durchschnitt 2010–2024
- **Größte Altersgruppe:** Bevölkerungsstärkste Gruppe im aktuellen Jahr

## 🧪 Teststrategie

- Datenintegritätstests
- Visuelle Prüfung von Diagrammen
- Test der GitHub CI/CD Pipelines

## 🔐 Sicherheit & Datenschutz

- Keine personenbezogenen Daten
- Verwendung von Open Data
- Gesicherter Datenbankzugriff via .env Variablen

## ℹ️ Projektgrenzen

- ✅ Regionale Prognose nach Altersgruppe
- ❌ Keine sozioökonomische Analyse
- ❌ Kein Login-System

## 📚 Weitere Informationen

- Flask, Plotly, Prophet, Scrapy, MongoDB Atlas

## 🤖 Beitrag leisten

Feedback, Forks und PRs sind jederzeit willkommen! 🚀
