# Basis-Image mit Python
FROM python:3.9-slim

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Kopiere die 'requirements.txt' in das Arbeitsverzeichnis
COPY requirements.txt /app/

# Installiere die benötigten Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Projektinhalt in das Arbeitsverzeichnis
COPY . /app/

# Setze das Flask-App-Entrypoint (falls Flask verwendet wird)
# Hier gehst du davon aus, dass dein Hauptscript im Backend-Ordner liegt.
CMD ["python", "app.py"]

# Falls du eine andere Startdatei hast, ersetze den Befehl oben entsprechend.