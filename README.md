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

## 💻 Installation

### 1. **Repository klonen:**
Zuerst das Repository auf deinen lokalen Rechner klonen:
```bash
git clone https://github.com/dein-github/bev-prog-zh-v2.git
```
2. Virtuelle Umgebung einrichten:
Erstelle eine virtuelle Umgebung und aktiviere sie:

```bash
cd bev-prog-zh-v2
python -m venv venv
source venv/bin/activate  # Für Mac/Linux
venv\Scripts\activate  # Für Windows
```
3. Abhängigkeiten installieren:
Installiere die notwendigen Python-Pakete:

```bash
pip install -r requirements.txt
```
4. MongoDB Atlas konfigurieren:
Stelle sicher, dass du eine MongoDB Atlas-Datenbank eingerichtet hast. Passe die Verbindungseinstellungen in deinem Code an, um die MongoDB URI und deine Datenbankdetails zu konfigurieren.

5. Flask App starten:
Starte die Flask-Anwendung:

```bash
flask --app backend run
```
🔄 Automatisierung
GitHub Actions:
Auto Scrape & Upload:
Automatisiertes Scraping und Hochladen der CSV-Daten von opendata.swiss in die MongoDB-Datenbank.

Model Training:
Das Prophet-Modell wird automatisch mit den neuesten Daten trainiert, um die Bevölkerungsprognose regelmäßig zu aktualisieren.

Workflow:
Der Auto Scrape & Upload-Job wird regelmäßig über GitHub Actions ausgeführt, um sicherzustellen, dass die Daten immer auf dem neuesten Stand sind.

Der Model Training-Job sorgt dafür, dass das Modell bei jedem neuen Datensatz neu trainiert wird.

📈 Prognose
Die Anwendung bietet Nutzern die Möglichkeit, die Bevölkerungsentwicklung für verschiedene Regionen und Altersgruppen zu prognostizieren. Die Ergebnisse werden sowohl in grafischer als auch in tabellarischer Form angezeigt. Insights wie langfristiger Trend, Spitzenjahr und Altersstruktur werden ebenfalls berechnet und präsentiert.

📚 Weitere Informationen
MongoDB Atlas: Zur Speicherung und schnellen Abfrage von Bevölkerungsdaten.

Scrapy: Für das Scrapen der Daten von opendata.swiss.

Prophet: Für das Modelltraining und die Zeitreihenanalyse.

Flask: Als Backend-Framework zur Bereitstellung der API und Darstellung der Ergebnisse.

Plotly: Für die interaktive Visualisierung der prognostizierten Bevölkerungszahlen.

🤖 Beitrag leisten
Fühle dich frei, zum Projekt beizutragen, indem du Issues erstellst oder Pull Requests vorschlägst. Dein Beitrag ist willkommen!

Vielen Dank für dein Interesse an diesem Projekt! 🌟
