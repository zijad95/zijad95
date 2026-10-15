# Fahrradanhänger-Rad 20" in SolidWorks: Felge, Schlauch und Mantel

Diese Anleitung führt Schritt für Schritt durch das Modellieren der drei Teile, den Aufbau der Baugruppe und das Erstellen der normgerechten Zeichnungen (DIN/ISO, Projektionsmethode 1).
Die Menünamen beziehen sich auf die **deutsche SolidWorks-Oberfläche (ab Version 2018)**.

> **Abkürzungen:**
>
> - **STEP-Dateien** aus `cad_step/` direkt in SolidWorks öffnen (Datei › Öffnen › Dateityp „STEP“).
> - **VBA-Makro** `solidworks_makros/Anhaengerrad20.bas`: erzeugt Teile, Baugruppe und Zeichnungsgerüste als echte SolidWorks-Dateien (Kapitel 7).
> - **Zeichnungen** liegen in `zeichnungen/` als **PDF** (ansehen/drucken) und **DXF** (bearbeiten, Kapitel 8).

---

## 0. Was wird gebaut?

Ein typisches, kostengünstiges Rad für **Kinder- und Lastenanhänger**. 20 × 1.75 ist dort die häufigste Größe.

| Pos. | Sachnummer | Teil | Ausführung (bewusst günstig) | Masse |
|---|---|---|---|---|
| 1 | AR20-001 | **Felge** 406×19 (ETRTO 19-406) | einwandiges Alu-Profil EN AW-6063 T6 (ohne Hohlkammer), Haken, 36 Loch, ohne Ösen, Ventilloch Ø8,5 für AV | ≈ 301 g |
| 2 | AR20-002 | **Schlauch** 20 × 1.75–2.125 (47/57-406) | Butyl, Autoventil (AV/Schrader) 35 mm | ≈ 150 g |
| 3 | AR20-003 | **Mantel** 47-406 (20 × 1.75) | Drahtreifen, 30 TPI, einfache Gummimischung | ≈ 661 g |
| – | AR20-000 | **Baugruppe** Anhängerrad (ohne Nabe/Speichen) | Außen-Ø 500 mm, Breite 47 mm | ≈ 1,11 kg |

**Warum diese Ausführung beim Anhänger Sinn ergibt:**

- **20"** ist robust, rollt leicht und passt in die üblichen Anhängerrahmen. Ersatzteile gibt es überall (BMX- und Kinderrad-Größe).
- **36 Speichenlöcher**: viele Speichen tragen die Seitenlasten in Kurven gut. Ein Anhänger hat kein Lenkkopflager, die Räder werden quer belastet.
- **47 mm breiter Reifen** mit **niedrigem Druck (2,5–3,5 bar)** federt die Ladung bzw. das Kind ab.
- **AV-Ventil**: an jeder Tankstelle aufpumpbar, Schläuche am billigsten.
- **Drahtreifen** und **einwandige Felge** sind die preiswertesten Bauarten.

### Koordinatensystem (gilt für alle Teile!)

- **Radachse = Z-Achse**: Die Profile werden auf der **Ebene rechts** skizziert und um eine **horizontale Mittellinie durch den Ursprung** rotiert.
- Das **Ventil liegt bei +Y (12 Uhr)**.
- Alle Teile haben denselben Ursprung. In der Baugruppe genügt deshalb „Ebene auf Ebene“.

Wenn du auf der Ebene rechts skizzierst, ist **horizontal = axial (Breite, z)** und **vertikal = radial (r)**.
Tipp: Maße zur horizontalen Mittellinie als **Durchmessermaß** setzen. Dazu bei der Intelligenten Bemaßung Linie und Mittellinie anklicken und das Maß **jenseits der Mittellinie** absetzen; SolidWorks zeigt dann automatisch Ø an.

### Vorbereitung (einmalig)

1. **Extras › Optionen › Dokumenteigenschaften › Zeichnungsnorm:** `DIN`.
2. **Einheiten:** `MMGS (Millimeter, Gramm, Sekunde)`, Dezimalstellen Länge 2.
3. Ordner anlegen, z. B. `Anhaengerrad20\`. Dateinamen wie in der Tabelle oben verwenden.

---

## 1. Teil AR20-001 Felge

Soll-Zeichnung: `zeichnungen/AR20-001_Felge.pdf`

### 1.1 Profilskizze

1. **Datei › Neu › Teil.**
2. **Ebene rechts** wählen › **Skizze**.
3. **Mittellinie** horizontal durch den Ursprung zeichnen, etwa 40 mm lang. Das ist die Radachse.
4. **Mittellinie** vertikal durch den Ursprung bis ca. 215 mm nach oben (Symmetrielinie).
5. Mit **Linie** die **rechte Profilhälfte** als zusammenhängenden Linienzug zeichnen (P1 → P12). Start- und Endpunkt liegen auf der vertikalen Mittellinie.

   | Punkt | z (axial) | r (radial) | Ø (=2·r) | Bedeutung |
   |---|---|---|---|---|
   | P1 | 0 | 197,0 | 394 | Tiefbettboden oben (Mitte) |
   | P2 | 4,0 | 197,0 | 394 | Ende Bettboden |
   | P3 | 5,5 | 203,0 | 406 | Schräge hoch zum Wulstsitz |
   | P4 | 9,5 | 203,0 | **406** | Wulstsitz = **BSD 406** |
   | P5 | 9,5 | 207,5 | 415 | Hornflanke innen |
   | P6 | 9,0 | 208,0 | 416 | Hakenlippe |
   | P7 | 9,0 | 209,0 | 418 | Hornoberkante innen |
   | P8 | 11,5 | 209,0 | **418** | Hornoberkante außen |
   | P9 | 11,5 | 201,0 | 402 | Hornflanke außen |
   | P10 | 7,0 | 201,0 | 402 | Unterseite Wulstsitz |
   | P11 | 5,5 | 195,0 | 390 | Unterseite Schräge |
   | P12 | 0 | 195,0 | **390** | Felgenboden unten (Mitte) |

6. **Bemaßen** mit der Intelligenten Bemaßung:
   - **Radial (als Ø zur horizontalen Mittellinie):** Ø394 (P1–P2), Ø406 (P3–P4), Ø415 (P5), Ø416 (P6), Ø418 (P7–P8), Ø402 (P9–P10), Ø390 (P11–P12).
   - **Axial (Abstand zur vertikalen Mittellinie):** 4 (P2), 5,5 (P3), 9,5 (P4/P5), 9 (P6/P7), 11,5 (P8/P9), 7 (P10), 5,5 (P11).
   - Horizontale bzw. vertikale Linien mit den Beziehungen **Horizontal/Vertikal** fixieren.
7. **Elemente spiegeln:** alle Profillinien auswählen, „Spiegeln um“ = vertikale Mittellinie. Damit ist das Profil geschlossen (22 Linien).
8. Die Skizze muss **vollständig definiert** sein (schwarz). Skizze verlassen, umbenennen in `Felgenprofil`.

### 1.2 Grundkörper

9. **Features › Aufsatz/Basis rotieren**: Drehachse = horizontale Mittellinie, Richtung 1 = **Blind, 360°** › OK. Umbenennen in `Felgenkörper`.

### 1.3 Ventilloch Ø8,5 (bei 12 Uhr)

10. **Ebene oben** › Skizze › **Kreis** im Ursprung, **Ø8,5**.
11. **Features › Linear ausgetragener Schnitt**: Richtung 1 = **Durch alles**. Die Pfeilrichtung muss nach **+Y (oben)** zeigen. In der Vorschau darf nur der obere Felgenboden geschnitten werden.
12. Umbenennen in `Ventilloch`.

### 1.4 Erstes Speichenloch Ø4,5 (5° neben dem Ventilloch)

Die Speichenlöcher sind radial. Am einfachsten entstehen sie als **rotierter Schnitt**:

13. **Ebene vorne** › Skizze.
14. **Mittellinie** vom Ursprung schräg nach oben, Länge 210, Winkel **5° zur vertikalen Achse**. Das ist die Bohrungsachse.
15. **Rechteck** direkt neben der Mittellinie: eine Längsseite liegt **auf** der Mittellinie (Beziehung „Kollinear“).
    - Breite (quer zur Achse) = **2,25** (halber Lochdurchmesser)
    - innere Kante im Abstand **187** vom Ursprung, äußere Kante **204** (überdeckt den Felgenboden r = 195…197 komplett)
16. **Features › Rotierter Schnitt**: Achse = schräge Mittellinie, 360°. Umbenennen in `Speichenloch`.

> **Alternative:** Referenzgeometrie › Ebene durch die Z-Achse mit 5° zur Ebene oben. Darauf einen Kreis Ø4,5 im Ursprung skizzieren und einen linear ausgetragenen Schnitt „Durch alles“ in eine Richtung ausführen.

### 1.5 Speichenlöcher vervielfältigen

17. **Referenzgeometrie › Achse** › „Zwei Ebenen“: **Ebene oben** + **Ebene rechts** › OK. Das ergibt die Radachse (Z). Umbenennen in `Radachse`.
18. **Features › Kreismuster**: Achse = `Radachse`, **Gleicher Abstand**, **360°**, **36 Instanzen**, Feature = `Speichenloch`. Umbenennen in `Speichenlöcher 36x`.
19. **Kontrolle:** Das Ventilloch liegt genau **zwischen zwei Speichenlöchern** (je 5° Abstand).

### 1.6 Material, Eigenschaften, Kontrolle

20. **Material** › *SOLIDWORKS Materials › Aluminiumlegierungen › 6063-T6*.
21. **Datei › Eigenschaften › Benutzerdefiniert:** `Benennung = Felge 406x19, 36 Loch, AV`, `Zeichnungsnummer = AR20-001`, `Werkstoff = EN AW-6063 T6`.
22. **Extras › Auswerten › Masseneigenschaften:** Masse **≈ 301 g**.
23. Speichern als **`AR20-001_Felge.SLDPRT`**.

---

## 2. Teil AR20-002 Schlauch

Soll-Zeichnung: `zeichnungen/AR20-002_Schlauch.pdf`

Der Schlauch wird im **Einbauzustand** vereinfacht als Torus mit 1 mm Wand dargestellt. Er liegt kollisionsfrei im Mantel.

### 2.1 Schlauchkörper

1. **Datei › Neu › Teil** › **Ebene rechts** › Skizze.
2. **Mittellinie** horizontal durch den Ursprung (Radachse).
3. **Kreis** mit dem Mittelpunkt senkrecht über dem Ursprung, Abstand **228,5** (als Durchmessermaß zur Mittellinie: **Ø457**).
4. Kreis **Ø36,6** (außen) und einen zweiten, konzentrischen Kreis **Ø34,6** (innen, Wand 1,0).
5. **Aufsatz/Basis rotieren** um die horizontale Mittellinie, 360°. Die beiden Kreise ergeben einen hohlen Torus. Umbenennen in `Schlauchkörper`.

### 2.2 AV-Ventil (bei 12 Uhr)

6. **Ebene vorne** › Skizze.
7. **Mittellinie** senkrecht durch den Ursprung (Y-Achse) von y = 165 bis y = 220.
8. Geschlossener Linienzug (Koordinaten x | y):
   `(0 | 174) → (5 | 174) → (5 | 186) → (4 | 186) → (4 | 210,7) → (0 | 210,7) → zurück`
   - Ø10 = Ventilkappe (y 174…186)
   - Ø8 = Ventilschaft mit Gewinde 8V1 (y 186…210,7); das obere Ende steckt in der Schlauchwand (r = 210,2…211,2)
9. **Aufsatz/Basis rotieren** um die senkrechte Mittellinie, 360°, **„Ergebnis verschmelzen“** aktiv. Umbenennen in `Ventil AV`.

### 2.3 Material und Eigenschaften

10. Eigenes Material „Butyl IIR“ (Kopie von *Gummi*), **Dichte 920 kg/m³**.
11. Eigenschaften: `Benennung = Schlauch 20" AV 35 mm`, `Zeichnungsnummer = AR20-002`, `Werkstoff = Butylkautschuk IIR`.
12. Kontrolle: Masse **≈ 150 g**, Außen-Ø 493,6, Innen-Ø 420,4. Speichern als **`AR20-002_Schlauch.SLDPRT`**.

---

## 3. Teil AR20-003 Mantel (Drahtreifen 47-406)

Soll-Zeichnung: `zeichnungen/AR20-003_Mantel.pdf`

### 3.1 Querschnittsskizze

1. **Datei › Neu › Teil** › **Ebene rechts** › Skizze.
2. Horizontale **Mittellinie** durch den Ursprung (Radachse) und vertikale **Mittellinie** (Symmetrie).
3. **Konstruktionspunkt M** auf der vertikalen Mittellinie im Abstand **226,5** (Ø453). M ist der Mittelpunkt beider Querschnittsbögen.
4. **Rechte Hälfte** als Linienzug + 2 Bögen zeichnen:

   | Punkt | z | r | Bedeutung |
   |---|---|---|---|
   | T1 | 5,5 | 203,0 | Wulst innen unten |
   | T2 | 9,5 | 203,0 | Wulst außen unten (sitzt auf Wulstsitz Ø406) |
   | T3 | 9,5 | 207,5 | Wulst an Hornflanke |
   | T4 | 9,0 | 208,0 | unter der Hakenlippe |
   | T5 | 9,0 | 209,0 | |
   | T6 | 11,5 | 209,0 | liegt auf dem Felgenhorn |
   | T7 | 17,212 | 210,5 | Übergang in den Außenbogen |
   | Scheitel außen | 0 | 250,0 | Außendurchmesser **500** |
   | Scheitel innen | 0 | 247,0 | Laufflächendicke **3** |
   | T8 | 15,427 | 213,0 | Übergang in den Innenbogen |
   | T9 | 5,5 | 210,0 | Wulst innen oben |

   - Linien T1→T2→T3→T4→T5→T6→T7
   - **Mittelpunktbogen** um M, **R23,5**, von T7 bis zur vertikalen Mittellinie (Scheitel außen)
   - **Mittelpunktbogen** um M, **R20,5**, von der vertikalen Mittellinie (Scheitel innen) bis T8
   - Linien T8→T9→T1
5. **Bemaßen:** R23,5 · R20,5 · M bei Ø453 · T7 bei Ø421 · T8 bei Ø426 · Wulst 4 breit (z 5,5…9,5) · Ø406 / Ø415 / Ø416 / Ø418 / Ø420 (T9) · Abstände 5,5 / 9 / 9,5 / 11,5 zur vertikalen Mittellinie. Die z-Werte von T7/T8 ergeben sich dann automatisch.
6. **Elemente spiegeln** um die vertikale Mittellinie. Die Skizze ist geschlossen und vollständig definiert.

### 3.2 Körper und Abschluss

7. **Aufsatz/Basis rotieren** um die horizontale Mittellinie, 360°. Umbenennen in `Mantelkörper`.
8. *Optional:* Laufflächenprofil als **rotierter Schnitt**, z. B. 3 Rillen 1,5 × 1 mm.
9. Material: *Gummi*, Dichte **1150 kg/m³** (benutzerdefiniertes Material „NR/SBR“).
10. Eigenschaften: `Benennung = Mantel 47-406 (20x1.75)`, `Zeichnungsnummer = AR20-003`, `Werkstoff = NR/SBR, Nylonkarkasse`.
11. Kontrolle: Masse **≈ 661 g**, Ø500, Breite 47. Speichern als **`AR20-003_Mantel.SLDPRT`**.

---

## 4. Baugruppe AR20-000 Anhängerrad

Soll-Zeichnung: `zeichnungen/AR20-000_Baugruppe.pdf`

1. **Datei › Neu › Baugruppe** › „Komponente einfügen“ › `AR20-001_Felge` › mit **grünem Haken** bestätigen. Die Felge sitzt dann im Ursprung und ist automatisch **fixiert**.
2. **Komponenten einfügen** › `AR20-002_Schlauch`.
3. **Verknüpfen**, jeweils **Deckungsgleich**:
   - Ebene vorne (Schlauch) ↔ Ebene vorne (Felge)
   - Ebene oben (Schlauch) ↔ Ebene oben (Felge)
   - Ebene rechts (Schlauch) ↔ Ebene rechts (Felge)

   > Realitätsnähere Variante: **Konzentrisch** Ventilschaft ↔ Ventilloch + **Konzentrisch** Schlauch ↔ Felge (Achsen) + **Deckungsgleich** Ebene rechts ↔ Ebene rechts.
4. Genauso den **Mantel** `AR20-003_Mantel` einfügen und verknüpfen.
5. **Extras › Auswerten › Kollisionserkennung** › Berechnen. Erwartet: **„Keine Kollisionen“**.
6. *Optional:* **Explosionsansicht** (Mantel +40 mm in Z, Schlauch +20 mm in Z).
7. Eigenschaften: `Benennung = Anhaengerrad 20" (ohne Nabe/Speichen)`, `Zeichnungsnummer = AR20-000`.
8. Speichern als **`AR20-000_Anhaengerrad.SLDASM`**. Gesamtmasse ≈ **1,11 kg**.

> Die **Nabe** (beim Anhänger meist mit Steckachse bzw. Schnellspanner) und die **Speichen** sind nicht enthalten. Sie können später in dieselbe Baugruppe konzentrisch zur Radachse eingefügt werden.

---

## 5. Zeichnungen: Grundeinstellungen (für alle 4 Blätter)

1. **Datei › Neu › Zeichnung** › Blattformat **„A3 (DIN)“** (A3 quer, mit Schriftfeld).
2. Rechtsklick auf das Blatt › **Eigenschaften**:
   - Maßstab **1:5**
   - Projektionsart **Erster Winkel** (= DIN ISO 128 Projektionsmethode 1)
   - „Eigenschaftswerte von Modell verwenden …“ aktivieren. Dann füllen *Benennung*, *Zeichnungsnummer*, *Werkstoff* und *Masse* das Schriftfeld automatisch.
3. **Extras › Optionen › Dokumenteigenschaften:** Zeichnungsnorm **DIN**, Schrifthöhe 3,5 mm, Dezimaltrennzeichen Komma.
4. Notiz in jedes Blatt: „Allgemeintoleranzen ISO 2768-m“.
5. Am Ende als `.SLDDRW` speichern und zusätzlich als **PDF** (Datei › Speichern unter › PDF).

| Werkzeug (Ansichtlayout / Beschriftung) | Wozu |
|---|---|
| Modellansicht | erste Ansicht (Vorderansicht) einfügen |
| Projizierte Ansicht | Draufsicht/Seitenansicht ableiten |
| Schnittansicht | Schnitt A–A durch die Radachse |
| Detailansicht | vergrößerter Ausschnitt (Profil) |
| Intelligente Bemaßung | Maße setzen |
| Modellelemente | Skizzenmaße aus dem Teil übernehmen |
| Mittellinie / Mittelpunktmarkierung | Achsen und Lochmitten |
| Automatische Positionsnummer / Stückliste | nur in der Baugruppenzeichnung |

---

## 6. Zeichnungen Schritt für Schritt

### 6.1 AR20-001 Felge

1. **Modellansicht** › `AR20-001_Felge` › **Vorderansicht** › Maßstab **1:5** › links oben platzieren.
2. **Verdeckte Kanten sichtbar** und **Mittellinien** einschalten. Winkelmaße **5°** (Ventilloch ↔ erstes Speichenloch) und **10°** (Teilung) setzen.
3. **Schnittansicht** › Schnittlinie **vertikal** durch den Mittelpunkt › rechts daneben ablegen › Bezeichnung **A**.
4. **Detailansicht B** › Kreis um das obere Profil in Schnitt A–A › Maßstab **5:1**.
5. **Projizierte Ansicht** nach unten (Draufsicht) › darin **Detailansicht C** um Ventilloch + Nachbarlöcher, Maßstab **2:1**. Die Draufsicht danach ausblenden.
6. **Bemaßen:**
   - Vorderansicht: **Ø418**, **Ø390**, Hinweis „Wulstsitz Ø406 (BSD)“, Notiz „36× Ø4,5 radial, gleichmäßig verteilt, um 5° zum Ventilloch versetzt“
   - Detail B: **23**, **19** (Maulweite), **8**, **11**, **4**, **14**, **8**, **6**, **6** (Betttiefe), **2**, Hinweis „Hakenlippe 0,5×1“
   - Detail C: **Ø8,5**, **Ø4,5**, Abstand **2× 17,1** (≙ 5° auf r = 196)
7. Notiz: „Material EN AW-6063 T6, eloxiert. Nicht bemaßte Radien R0,5. Löcher entgratet.“

### 6.2 AR20-002 Schlauch

1. Vorderansicht 1:5 mit **Ø493,6** und **Ø420,4**, Hinweis „Ventil AV bei 12 Uhr“.
2. **Schnittansicht A–A** vertikal durch den Mittelpunkt, also durch das Ventil.
3. **Detailansicht B** (Querschnitt + Ventil), Maßstab **2:1**.
4. Bemaßen: **Ø36,6**, **Wand 1**, **Ø8 (8V1)**, **Ø10**, **12** (Kappe), **36,2** (Kappe bis Schlauch).
5. Notiz: „20 × 1.75–2.125 (ETRTO 47/57-406), Butyl. Ventil AV 35 mm, max. 3,5 bar.“

### 6.3 AR20-003 Mantel

1. Vorderansicht 1:5 mit **Ø500** und **Ø406 (Wulst)**.
2. **Schnittansicht A–A**, dann **Detailansicht B**, Maßstab **2:1**.
3. Bemaßen: Breite **47**, Höhe **47**, **R23,5**, **R20,5**, **23,5** (Wulst bis Bogenmitte), **19** / **11** (Wulstabstand außen/innen), **6** (Wulsthöhe), „Lauffläche 3“, „Wulst mit Drahtkern“.
4. Notiz: „47-406 (20 × 1.75), Drahtreifen, 30 TPI, max. 3,5 bar (50 psi).“

### 6.4 AR20-000 Zusammenbau

1. Vorderansicht 1:5 mit **Ø500**.
2. **Schnittansicht A–A**. Keine Komponente vom Schnitt ausschließen; jedes Teil bekommt automatisch eine eigene Schraffur.
3. **Detailansicht B**, Maßstab **2:1**, Maße **47** (Reifenbreite) und **55** (Felgenboden bis Lauffläche).
4. **Tabellen › Stückliste** über dem Schriftfeld (Pos. | Menge | Benennung | Sachnummer | Werkstoff | Masse).
5. **Automatische Positionsnummer**: **1** Felge, **2** Schlauch, **3** Mantel.
6. Notiz „Reifendruck 2,5–3,5 bar“.

---

## 7. Automatisch per Makro (`solidworks_makros/Anhaengerrad20.bas`)

1. SolidWorks › **Extras › Makro › Neu…** › z. B. `Anhaengerrad20.swp` speichern. Der VBA-Editor öffnet sich.
2. Im VBA-Editor **Datei › Datei importieren…** › `Anhaengerrad20.bas`. Das leere `Module1` kann gelöscht werden.
3. **F5** › `main`.
4. Ergebnis im Unterordner `Anhaengerrad20\` neben der .swp-Datei: drei `.SLDPRT`, eine `.SLDASM` und vier `.SLDDRW` (Vorderansicht 1:5 + Isometrie).
5. Schnitt, Details, Maße und Stückliste danach wie in Kapitel 6 ergänzen.

Hinweise: Das Makro nutzt die Standardvorlagen (*Extras › Optionen › Standardvorlagen*) und ist sprachunabhängig. Klappt ein Schritt nicht, weicht es aus (einzelne Löcher statt Muster, Fixieren statt Verknüpfen) und zeigt am Ende eine Hinweisliste. Das Makro selbst konnte ohne SolidWorks-Lizenz nicht ausgeführt werden. Die Geometrie ist aber dieselbe wie in den geprüften STEP-Dateien.

## 8. Mitgelieferte Dateien öffnen und bearbeiten

**3D-Teile (STEP):**

- `AR20-001_Felge.step`, `AR20-002_Schlauch.step`, `AR20-003_Mantel.step`, `AR20-000_Anhaengerrad_Baugruppe.step`
- SolidWorks: **Datei › Öffnen** › Dateityp *STEP (\*.step)*. Die Baugruppe öffnet sich als `.SLDASM` mit drei Teilen. Danach **Speichern unter** als SolidWorks-Datei.
- Zum Bearbeiten: Rechtsklick auf „Importiert1“ › **FeatureWorks › Features erkennen**. Dann werden Rotation, Bohrungen und Muster wieder zu bearbeitbaren Features. Alternativ direkt mit **Fläche verschieben** / **Direktbearbeitung** arbeiten.

**Zeichnungen:**

- **PDF** (`AR20_Zeichnungssatz.pdf` bzw. einzeln): zum Ansehen und Drucken.
- **DXF** (`*.dxf`, Maßstab 1:1 in mm, A3-Blatt): bearbeitbar.
  - SolidWorks: **Datei › Öffnen › DXF** › „In neue Zeichnung importieren“ › Einheiten **Millimeter**, Blattformat „Keins“. Dann sind Linien, Texte und Maße als 2D-Skizze editierbar.
  - Ebenso in AutoCAD, DraftSight oder dem kostenlosen LibreCAD.
  - Ebenen: `KONTUR`, `DUENN`, `MITTELLINIE`, `VERDECKT`, `MASSE`, `TEXT`, `SCHRAFFUR`, `RAHMEN`.
  - Die Maße in der DXF sind einfache Linien + Text (nicht assoziativ). Für eine Zeichnung, die sich bei Modelländerungen mitändert, die SolidWorks-Zeichnung nach Kapitel 5–6 aus dem Modell ableiten.

## 9. Hauptmaße

| | Felge | Schlauch | Mantel | Rad |
|---|---|---|---|---|
| Außen-Ø | 418 | 493,6 | **500** | 500 |
| Innen-Ø | 390 | 420,4 | 406 (Wulst) | 390 |
| Breite | 23 (Maul 19) | 36,6 | **47** | 47 |
| Werkstoff | EN AW-6063 T6 | Butyl IIR | NR/SBR | – |
| Masse | 301 g | 150 g | 661 g | 1,11 kg |
| Norm | ETRTO 19-406 | 47/57-406 | ETRTO 47-406 | – |
