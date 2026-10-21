# Bregenz Kebap – Webseite

Einseitige Webseite für Bregenz Kebap in der Quellenstraße, 6900 Bregenz.
Alles steckt in einer einzigen Datei: `index.html`. Es braucht keinen Build-Schritt, die Datei einfach im Browser öffnen oder auf einen beliebigen Webspace hochladen (z. B. GitHub Pages, Netlify).

## Inhalte anpassen

Ganz unten in `index.html` stehen zwei Blöcke, die du bearbeiten kannst:

- **`CONFIG`**: Hausnummer, Telefonnummer, Link zum Impressum und Öffnungszeiten.
  - Eine leere Telefonnummer bzw. ein leerer Impressum-Link wird automatisch ausgeblendet.
  - Für einen Ruhetag `null` eintragen. Schließzeiten nach Mitternacht (z. B. `["11:00", "01:00"]`) funktionieren.
  - Die Anzeige „Jetzt geöffnet / Geschlossen“ rechnet automatisch in der Wiener Zeitzone.
- **`MENU`**: Kategorien und Gerichte mit Beschreibung und Preis. `tag` zeigt ein kleines Label an, `veg: true` markiert ein Gericht als vegetarisch.

> **Wichtig:** Öffnungszeiten, Speisekarte und Preise sind derzeit **Beispielwerte**. Bitte vor der Veröffentlichung durch die echten Daten ersetzen und ein Impressum ergänzen (in Österreich Pflicht).

## Features

- Animierter Dönerspieß und Glut-Funken im Hero-Bereich
- Speisekarte mit Kategorien-Tabs (auch per Pfeiltasten bedienbar)
- Live-Anzeige „Jetzt geöffnet“ inkl. Hervorhebung des heutigen Tages
- Eingebettete Karte und Button „Route planen“ (Google Maps)
- Für Handy optimiert, respektiert die Einstellung „Bewegung reduzieren“
