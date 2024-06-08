# cdk1
Herzlich willkommen zu unserer Klimadaten-Challenge cdk1 zum Thema Überschwemmungen! In diesem README finden Sie alle wichtigen Informationen zu unserer Herausforderung, den Zielen und der Struktur unseres Projekts.

## projektübersicht
Im Rahmen unserer Klimadaten-Challenge haben wir uns einer wichtigen Aufgabe gestellt: Die Europäische Union möchte die Bevölkerung besser über die Risiken des Klimawandels informieren. Geplant ist eine neue Webseite, auf der Daten zur Entwicklung bestimmter Extremereignisse in Europa übersichtlich dargestellt werden.

Wir haben uns entschieden, den Fokus auf Überschwemmungen zu legen. Sowohl Fachpersonen als auch interessierte Bürger sollen mit wenigen Klicks einen Überblick über die Klimaveränderungen in für sie relevanten Regionen erhalten, abgestimmt auf ihre individuellen Bedürfnisse.

Unser Auftrag als Data Scientists war es, einen funktionsfähigen Entwurf dieser Webseite zu entwickeln und zu programmieren.

## Projektstruktur

- **dashboard/**: Enthält beide Dashboards – für die Schweiz und die Alpenräume.
  - **dashboard.py**: Dashboard für die Schweiz.
  - **dashboard_alps.py**: Dashboard für die Alpenräume.
- **data/**: Beinhaltet unsere Rohdaten sowie die verarbeiteten Daten nach dem Data Wrangling.
  - **generated/**: Verarbeitete Daten.
  - **source/**: Rohdaten.
- **data_story/**: Beinhaltet unsere Data Story sowie wichtige Ressourcen dafür.
- **data_wrangling/**: Beinhaltet Dateien für das Data Wrangling.
- **exploration/**: Beinhaltet Dateien für die Explorative Datenanalyse (EDA).

## Installation
Zur Installation und Nutzung unserer Daten finden Sie alle relevanten Dateien im Verzeichnis data, insbesondere im Unterverzeichnis generated. Dort befinden sich alle von uns generierten Daten.

Wichtige Dateien
Für das dashboard_alps.py, das die Alpenregionen abdeckt, benötigen Sie folgende Dateien:

- [flood_data_fixed.csv](https://github.com/bn4t/cdk1/blob/master/data/generated/flood_data_fixed.csv)
- [rain_data_alps.csv](https://github.com/bn4t/cdk1/blob/master/data/generated/rain_data_alps.csv)
- [regionswithcords.csv](https://github.com/bn4t/cdk1/blob/master/data/generated/regionswithcords.csv)

Für das dashboard.py, das ausschliesslich die Schweiz anzeigt, sind folgende Dateien erforderlich:

- [flood_data.csv](https://github.com/bn4t/cdk1/blob/master/data/generated/flood_data.csv)
- [rain_data.csv](https://github.com/bn4t/cdk1/blob/master/data/generated/rain_data.csv)
- [regions_ch.csv](https://github.com/bn4t/cdk1/blob/master/data/generated/regions_ch.csv)

Voraussetzungen
Um das Dashboard sowie die Datenstory starten zu können, benötigen Sie Visual Studio Code [(VS Code)](https://code.visualstudio.com/).

## Schritte zur Installation
Sie können entweder unser gesamtes GitHub-Repository klonen oder nur die relevanten Dateien herunterladen. Wichtig ist, dass sich die Daten sowie die Code-Dateien im VS Code-Workspace befinden, damit alles reibungslos funktioniert.
![Workspace](https://github.com/bn4t/cdk1/assets/145562358/a282049a-17d0-4735-8b62-d58afc74614c)


## Nutzung
1. Öffnen Sie das Terminal in VS Code, indem Sie auf `Terminal` > `New Terminal` im Menü klicken.
2. Geben Sie im Terminal den folgenden Befehl ein (abhängig davon, wie Ihre Hauptdatei heißt):
   - Für `app.py`:
     ```bash
     python app.py
     ```
   - Für `dashboard.py`:
     ```bash
     python dashboard.py
     ```
   - Für `dashboard_alps.py`:
     ```bash
     python dashboard_alps.py
     ```
   - Für `data_story.html`, öffnen Sie die Datei direkt im Browser:
     ```bash
     open data_story.html
     ```

3. Nachdem der Code vollständig ausgeführt wurde, wird ein Link in der Form `http://127.0.0.1:5000` im Terminal angezeigt.
4. Klicken Sie auf diesen Link, indem Sie `Ctrl + Linksklick` (Windows/Linux) oder `Command + Linksklick` (Mac) verwenden, um das Dashboard in Ihrem Browser zu öffnen.

## Dokumentation
Die Informationen zu unserem Arbeitsablauf finden Sie in unserem [Wiki](https://github.com/bn4t/cdk1/wiki).

## Mitwirkende
Benjamin Nater
Boran Eker
Murat Kayhan

