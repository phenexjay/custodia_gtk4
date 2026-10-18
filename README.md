# Custodia GTK 4

Desktopverwaltung für Code-Snippets mit Python, GTK 4, Libadwaita und GtkSourceView 5.

## Start und Tests

Benötigt werden Python 3 mit PyGObject sowie die GTK-Typbibliotheken:
`python3-gi`, `gir1.2-gtk-4.0`, `gir1.2-adw-1`, `gir1.2-gtksource-5`.
Für Tests ohne Desktop zusätzlich `xvfb`, `xauth` und eine D-Bus-Sitzung.

Aus dem Repository-Verzeichnis starten, da CSS relativ geladen wird:

```sh
/usr/bin/python3 main.py
```

In der eingerichteten Cloud-Umgebung zuerst die lokalen Bibliotheken aktivieren:

```sh
. /workspace/.custodia-env/activate.sh
cd /workspace/custodia_gtk4
dbus-run-session -- xvfb-run -a /usr/bin/python3 main.py
```

Die Tests verwenden temporäre Dateien; die mitgelieferte Kollektion wird nicht verändert:

```sh
# Nur Dateiformat und Datenmodell, ohne Display:
/usr/bin/python3 -m unittest discover -s tests -p test_files.py -v
# Einschließlich echter GTK-Fenster und Ereignisbehandlung:
dbus-run-session -- xvfb-run -a /usr/bin/python3 -m unittest discover -s tests -v
```

## Kollektionen

Über „Öffnen“ eine `.col`-Datei auswählen oder über das Symbol für eine neue
Kollektion einen Namen eingeben und „Erstellen“ wählen. Kategorien und Snippets
lassen sich über ihre Eingabefelder und Plus-Schaltflächen hinzufügen. Ein
Snippet auswählen und den Bearbeiten-Schalter aktivieren. Erneutes Betätigen,
Wechseln der Auswahl und Schließen des Fensters speichern die Bearbeitung.

Gespeichert wird am ausgewählten Dateipfad, unabhängig vom Kollektionsnamen.
Schreibvorgänge verwenden eine temporäre Datei im gleichen Verzeichnis und
ersetzen das Ziel erst nach erfolgreichem Schreiben. Fehler werden angezeigt.

Neue Speicherungen verwenden UTF-8-JSON mit `version: 1`, `title` und
`categories`. Kategorien enthalten `title`, `created` und `snippets`; Snippets
enthalten ihre Texte, Zeitstempel und Tags. Das Format wird beim Laden und
Speichern geprüft.

Bestehende binäre Pickle-Kollektionen werden über einen eingeschränkten Import
für `category.Category` und `snippet.Snippet` gelesen. Andere globale Objekte
werden abgewiesen. Beim nächsten Speichern wird dieselbe Datei in JSON
umgewandelt; ältere Programmversionen können diese anschließend nicht mehr
lesen. Vor einer Migration wichtiger Altbestände eine Sicherung erstellen.

`new_data.py` ist ein altes Hilfsskript, das `saves/default.col` überschreibt;
es gehört nicht zum normalen Start- oder Testablauf.

Einstellungen, Drucken sowie einige Symbolaktionen sind weiterhin unvollständig.
