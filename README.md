# Datenanalyse

## Benutzung

### Whatsapp
- Die manuell herunter geladenen `.txt` Dateien für jeden Chat werden in einen Ordner verschoben. 
- Das Script `convert.py` wird nun mit dem Ordnerpfad aufgerufen.
- Die `.json` Dateien für jeden Chat werden nun mit einem weiteren Script zu einer Datei zusammengeführt. Hierfür wird `chat_over_day.py` mit dem selben Ordner aufgerufen.
- Optional kann nun die finale Datei `output.txt` in den Ordner `Whatsapp/` kopiert werden. Alternativ kann der Pfad beim Aufruf der Module auch von hand gesetzt werden.
- Für eine grobe Analyse kann dann das Script `whatsapp.py` aufgerufen werden.
- Auch einzelne Module können aus `Whatsapp/` manuell gestartet oder in eigene Skripte eingebunden werden. 

### TODO