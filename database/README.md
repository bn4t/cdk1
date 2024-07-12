# Database

In dieser Directory ist ein dump einer Datenbank mit Regen- als auch Flut-Daten der Schweiz.
Die Datenbank wurde zwar nicht verwendet für unsere Data Story oder Dashboard, jedoch wäre es eine möglichkeit gewesen die Datenbank zu verwenden für weitere Analysen.

## Import
Die Datenbank kann mit folgendem Befehl importiert werden: `pg_restore -d cdk cdk.sql`.
Vorher muss die Datenbank `cdk` manuell erstellt werden.
