# Laufrad 28" in SolidWorks: Felge, Schlauch und Mantel

Diese Anleitung führt Schritt für Schritt durch das Modellieren der drei Teile, den Aufbau der Baugruppe und das Erstellen der normgerechten Zeichnungen (DIN/ISO, Projektionsmethode 1).
Die Menünamen beziehen sich auf die **deutsche SolidWorks-Oberfläche (ab Version 2018)**.

> **Abkürzung:** Wer nicht alles von Hand modellieren will, nimmt
> - die fertigen **STEP-Dateien** aus `cad_step/` (Datei › Öffnen, Dateityp „STEP AP203/214/242“), oder
> - das **VBA-Makro** `solidworks_makros/Laufrad28.bas`. Es erzeugt alle Teile, die Baugruppe und die Grundgerüste der Zeichnungen (siehe Kapitel 7).
>
> Die bemaßten **Soll-Zeichnungen** liegen in `zeichnungen/` (`LR28_Zeichnungssatz.pdf`). Daran siehst du, wie das Ergebnis aussehen soll.

---

## 0. Was wird gebaut? (kostengünstige Standardausführung)

| Pos. | Sachnummer | Teil | Ausführung (bewusst günstig) | Masse |
|---|---|---|---|---|
| 1 | LR28-001 | **Felge** 622×19 (ETRTO 19-622) | einwandiges Alu-Profil EN AW-6063 T6 (ohne Hohlkammer), Haken (Crochet), 36 Loch, ohne Ösen, Stoß gepinnt, Ventilloch Ø8,5 für AV | ≈ 465 g |
| 2 | LR28-002 | **Schlauch** 28" × 1 3/8–1 5/8 (32/47-622) | Butyl, Autoventil (AV/Schrader) 40 mm, das billigste und überall aufpumpbare Ventil | ≈ 148 g |
| 3 | LR28-003 | **Mantel** 37-622 (28 × 1.40) | Drahtreifen (kein Faltreifen), 50 TPI Nylonkarkasse, einfache Gummimischung | ≈ 716 g |
| – | LR28-000 | **Baugruppe** Laufrad (ohne Nabe/Speichen) | Außendurchmesser ≈ 696 mm, Breite 37 mm | ≈ 1,33 kg |

**Warum das günstig ist:** einwandige Felge statt Hohlkammer (weniger Material, einfacheres Strangpressprofil), keine Ösen, AV-Ventil statt SV/Presta (passt an jede Tankstelle, Schlauch billiger), Drahtreifen statt Faltreifen (Stahlkern statt Kevlar), 50 TPI statt 60–120 TPI.

### Koordinatensystem (gilt für alle Teile!)

- **Radachse = Z-Achse**: Die Profile werden auf der **Ebene rechts** skizziert und um eine **horizontale Mittellinie durch den Ursprung** rotiert.
- Das **Ventil liegt bei +Y (12 Uhr)**.
- Alle Teile haben denselben Ursprung. In der Baugruppe genügt deshalb „Ebene auf Ebene“.

Wenn du auf der Ebene rechts skizzierst, ist **horizontal = axial (Breite, z)** und **vertikal = radial (r)**.
Tipp: Maße zur horizontalen Mittellinie als **Durchmessermaß** setzen. Dazu bei der Intelligenten Bemaßung Linie und Mittellinie anklicken und das Maß **jenseits der Mittellinie** absetzen; SolidWorks zeigt dann automatisch Ø an.

### Vorbereitung (einmalig)

1. **Extras › Optionen › Dokumenteigenschaften › Zeichnungsnorm:** `DIN`.
2. **Einheiten:** `MMGS (Millimeter, Gramm, Sekunde)`, Dezimalstellen Länge 2.
3. Ordner anlegen, z. B. `Laufrad28\`. Dateinamen wie in der Tabelle oben verwenden.

---

## 1. Teil LR28-001 Felge

Soll-Zeichnung: `zeichnungen/LR28-001_Felge.pdf`

### 1.1 Profilskizze (Skizze „Felgenprofil“)

1. **Datei › Neu › Teil.**
2. **Ebene rechts** wählen › **Skizze**.
3. **Mittellinie** horizontal durch den Ursprung zeichnen, etwa 40 mm lang. Das ist die Radachse.
4. **Mittellinie** vertikal durch den Ursprung bis ca. 320 mm nach oben (Symmetrielinie).
5. Mit **Linie** die **rechte Profilhälfte** als zusammenhängenden Linienzug zeichnen (P1 → P12). Start- und Endpunkt liegen auf der vertikalen Mittellinie.

   | Punkt | z (axial) | r (radial) | Ø (=2·r) | Bedeutung |
   |---|---|---|---|---|
   | P1 | 0 | 305,0 | 610 | Tiefbettboden oben (Mitte) |
   | P2 | 4,0 | 305,0 | 610 | Ende Bettboden |
   | P3 | 5,5 | 311,0 | 622 | Schräge hoch zum Wulstsitz |
   | P4 | 9,5 | 311,0 | **622** | Wulstsitz = **BSD 622** |
   | P5 | 9,5 | 315,5 | 631 | Hornflanke innen |
   | P6 | 9,0 | 316,0 | 632 | Hakenlippe |
   | P7 | 9,0 | 317,0 | 634 | Hornoberkante innen |
   | P8 | 11,5 | 317,0 | **634** | Hornoberkante außen |
   | P9 | 11,5 | 309,0 | 618 | Hornflanke außen |
   | P10 | 7,0 | 309,0 | 618 | Unterseite Wulstsitz |
   | P11 | 5,5 | 303,0 | 606 | Unterseite Schräge |
   | P12 | 0 | 303,0 | **606** | Felgenboden unten (Mitte) |

6. **Bemaßen** mit der Intelligenten Bemaßung:
   - **Radial (als Ø zur horizontalen Mittellinie):** Ø610 (P1–P2), Ø622 (P3–P4), Ø631 (P5), Ø632 (P6), Ø634 (P7–P8), Ø618 (P9–P10), Ø606 (P11–P12).
   - **Axial (Abstand zur vertikalen Mittellinie):** 4 (P2), 5,5 (P3), 9,5 (P4/P5), 9 (P6/P7), 11,5 (P8/P9), 7 (P10), 5,5 (P11).
   - Horizontale bzw. vertikale Linien mit den Beziehungen **Horizontal/Vertikal** fixieren.
7. **Elemente spiegeln:** alle Profillinien auswählen, „Spiegeln um“ = vertikale Mittellinie. Damit ist das Profil geschlossen (22 Linien).
8. Die Skizze muss jetzt **vollständig definiert** sein (schwarz). Skizze verlassen, umbenennen in `Felgenprofil`.

### 1.2 Grundkörper

9. **Features › Aufsatz/Basis rotieren**: Drehachse = horizontale Mittellinie, Richtung 1 = **Blind, 360°** › OK. Umbenennen in `Felgenkörper`.

### 1.3 Ventilloch Ø8,5 (bei 12 Uhr)

10. **Ebene oben** › Skizze › **Kreis** im Ursprung, **Ø8,5**.
11. **Features › Linear ausgetragener Schnitt**: Richtung 1 = **Durch alles**. Die Pfeilrichtung muss nach **+Y (oben)** zeigen. In der Vorschau darf nur der obere Felgenboden geschnitten werden, nicht der untere.
12. Umbenennen in `Ventilloch`.

### 1.4 Erstes Speichenloch Ø4,5 (5° neben dem Ventilloch)

Die Speichenlöcher sind radial. Am einfachsten entstehen sie als **rotierter Schnitt**:

13. **Ebene vorne** › Skizze.
14. **Mittellinie** vom Ursprung schräg nach oben, Länge 320, Winkel **5° zur vertikalen Achse** (Winkelmaß zwischen Mittellinie und einer vertikalen Hilfslinie bzw. der Y-Achse). Das ist die Bohrungsachse.
15. **Rechteck** direkt neben der Mittellinie: eine Längsseite liegt **auf** der Mittellinie (Beziehung „Kollinear“).
    - Breite (quer zur Achse) = **2,25** (halber Lochdurchmesser)
    - innere Kante im Abstand **295** vom Ursprung, äußere Kante **312** vom Ursprung (das Rechteck muss den Felgenboden r = 303…305 komplett überdecken)
16. **Features › Rotierter Schnitt**: Achse = schräge Mittellinie, 360°. Umbenennen in `Speichenloch`.

> **Alternative:** Referenzgeometrie › Ebene mit Referenz 1 = Z-Achse (Achse aus Schritt 17), Referenz 2 = Ebene oben, Winkel 5°. Darauf einen Kreis Ø4,5 im Ursprung skizzieren und einen linear ausgetragenen Schnitt „Durch alles“ in eine Richtung ausführen.

### 1.5 Speichenlöcher vervielfältigen

17. **Referenzgeometrie › Achse** › „Zwei Ebenen“: **Ebene oben** + **Ebene rechts** › OK. Das ergibt die Radachse (Z). Umbenennen in `Radachse`.
    (Alternativ: Ansicht › Ausblenden/Einblenden › Temporäre Achsen.)
18. **Features › Kreismuster**:
    - Musterachse = `Radachse`
    - **Gleicher Abstand**, Winkel **360°**, **36 Instanzen**
    - Zu musternde Features = `Speichenloch`
    - OK. Umbenennen in `Speichenlöcher 36x`.
19. **Kontrolle:** Das Ventilloch liegt jetzt genau **zwischen zwei Speichenlöchern** (je 5° Abstand).

### 1.6 Material, Eigenschaften, Kontrolle

20. Rechtsklick **Material** › Material bearbeiten › *SOLIDWORKS Materials › Aluminiumlegierungen › 6063-T6*.
21. **Datei › Eigenschaften › Benutzerdefiniert:**
    `Benennung = Felge 622x19, 36 Loch, AV`, `Zeichnungsnummer = LR28-001`, `Werkstoff = EN AW-6063 T6`.
22. **Extras › Auswerten › Masseneigenschaften:** Masse **≈ 465 g**, Volumen ≈ 172 cm³.
23. Speichern als **`LR28-001_Felge.SLDPRT`**.

Der FeatureManager sieht dann so aus: `Felgenprofil` → `Felgenkörper` → `Ventilloch` → `Speichenloch` → `Radachse` → `Speichenlöcher 36x`.

---

## 2. Teil LR28-002 Schlauch

Soll-Zeichnung: `zeichnungen/LR28-002_Schlauch.pdf`

Der Schlauch wird im **Einbauzustand** vereinfacht als Torus mit 0,9 mm Wand dargestellt. Er liegt kollisionsfrei im Mantel.

### 2.1 Schlauchkörper

1. **Datei › Neu › Teil** › **Ebene rechts** › Skizze.
2. **Mittellinie** horizontal durch den Ursprung (Radachse).
3. **Kreis** mit dem Mittelpunkt auf der vertikalen Achse, **Abstand 330** über dem Ursprung (als Durchmessermaß zur Mittellinie: **Ø660**). Beziehung „Vertikal“ zwischen Ursprung und Kreismittelpunkt setzen.
4. Kreis **Ø28** (außen) und einen zweiten, konzentrischen Kreis **Ø26,2** (innen, Wand 0,9).
5. **Aufsatz/Basis rotieren** um die horizontale Mittellinie, 360°. Die beiden Kreise ergeben einen hohlen Torus. Umbenennen in `Schlauchkörper`.

### 2.2 AV-Ventil (bei 12 Uhr)

6. **Ebene vorne** › Skizze.
7. **Mittellinie** senkrecht durch den Ursprung (Y-Achse) von y = 270 bis y = 325.
8. Geschlossener Linienzug (Koordinaten x | y):
   `(0 | 280) → (5 | 280) → (5 | 292) → (4 | 292) → (4 | 316,5) → (0 | 316,5) → zurück`
   - Ø10 = Ventilkappe (y 280…292)
   - Ø8 = Ventilschaft mit Gewinde 8V1 (y 292…316,5); das obere Ende steckt in der Schlauchwand (r = 316…316,9)
9. **Aufsatz/Basis rotieren** um die senkrechte Mittellinie, 360°, **„Ergebnis verschmelzen“** aktiv. Umbenennen in `Ventil AV`.

### 2.3 Material und Eigenschaften

10. Material: eigenes Material anlegen (Materialdatenbank › Benutzerdefinierte Materialien › Kopie von *Gummi*) mit dem Namen **„Butyl IIR“** und der **Dichte 920 kg/m³**.
11. Eigenschaften: `Benennung = Schlauch 28" AV 40 mm`, `Zeichnungsnummer = LR28-002`, `Werkstoff = Butylkautschuk IIR`.
12. Kontrolle: Masse **≈ 148 g**, Außen-Ø 688, Innen-Ø 632. Speichern als **`LR28-002_Schlauch.SLDPRT`**.

---

## 3. Teil LR28-003 Mantel (Drahtreifen 37-622)

Soll-Zeichnung: `zeichnungen/LR28-003_Mantel.pdf`

### 3.1 Querschnittsskizze

1. **Datei › Neu › Teil** › **Ebene rechts** › Skizze.
2. Horizontale **Mittellinie** durch den Ursprung (Radachse) und vertikale **Mittellinie** (Symmetrie).
3. Einen **Konstruktionspunkt M** auf der vertikalen Mittellinie im Abstand **329,5** (Ø659) setzen. Er ist der Mittelpunkt beider Querschnittsbögen.
4. **Rechte Hälfte** als Linienzug + 2 Bögen zeichnen:

   | Punkt | z | r | Bedeutung |
   |---|---|---|---|
   | T1 | 5,5 | 311,0 | Wulst innen unten |
   | T2 | 9,5 | 311,0 | Wulst außen unten (sitzt auf Wulstsitz Ø622) |
   | T3 | 9,5 | 315,5 | Wulst an Hornflanke |
   | T4 | 9,0 | 316,0 | unter der Hakenlippe |
   | T5 | 9,0 | 317,0 | |
   | T6 | 11,5 | 317,0 | liegt auf dem Felgenhorn |
   | T7 | 14,874 | 318,5 | Übergang in den Außenbogen |
   | Scheitel außen | 0 | 348,0 | Außendurchmesser **696** |
   | Scheitel innen | 0 | 345,0 | Laufflächendicke **3** |
   | T8 | 12,247 | 320,0 | Übergang in den Innenbogen |
   | T9 | 5,5 | 317,0 | Wulst innen oben |

   - Linien T1→T2→T3→T4→T5→T6→T7
   - **Mittelpunktbogen** um M, **R18,5**, von T7 bis zur vertikalen Mittellinie (Scheitel außen)
   - **Mittelpunktbogen** um M, **R15,5**, von der vertikalen Mittellinie (Scheitel innen) bis T8
   - Linien T8→T9→T1
5. **Bemaßen:** R18,5 · R15,5 · M bei Ø659 · T7 bei Ø637 · T8 bei Ø640 · Wulst 4 breit (z 5,5…9,5) · Ø622 / Ø631 / Ø632 / Ø634 · Abstände 5,5 / 9 / 9,5 / 11,5 zur vertikalen Mittellinie. Die z-Werte von T7/T8 ergeben sich dann automatisch.
6. **Elemente spiegeln** um die vertikale Mittellinie. Die Skizze ist geschlossen und vollständig definiert.

### 3.2 Körper und Abschluss

7. **Aufsatz/Basis rotieren** um die horizontale Mittellinie, 360°. Umbenennen in `Mantelkörper`.
8. *Optional, für die Optik:* Laufflächenprofil als **rotierter Schnitt** anlegen, z. B. 3 Rillen 1,5 × 1 mm. Das ist nicht Teil der Soll-Zeichnung.
9. Material: *Gummi*, Dichte auf **1150 kg/m³** anpassen (benutzerdefiniertes Material „NR/SBR“).
10. Eigenschaften: `Benennung = Mantel 37-622 (28x1.40)`, `Zeichnungsnummer = LR28-003`, `Werkstoff = NR/SBR, Nylonkarkasse`.
11. Kontrolle: Masse **≈ 716 g**, Ø696, Breite 37. Speichern als **`LR28-003_Mantel.SLDPRT`**.

---

## 4. Baugruppe LR28-000 Laufrad

Soll-Zeichnung: `zeichnungen/LR28-000_Baugruppe.pdf`

1. **Datei › Neu › Baugruppe** › „Komponente einfügen“ › `LR28-001_Felge` › mit **grünem Haken** bestätigen. Die Felge wird dann im Ursprung platziert und automatisch **fixiert**.
2. **Komponenten einfügen** › `LR28-002_Schlauch` irgendwo ablegen.
3. **Verknüpfen** (Mates), jeweils **Deckungsgleich**:
   - Ebene vorne (Schlauch) ↔ Ebene vorne (Felge)
   - Ebene oben (Schlauch) ↔ Ebene oben (Felge)
   - Ebene rechts (Schlauch) ↔ Ebene rechts (Felge)

   > Realitätsnähere Variante: **Konzentrisch** Ventilschaft ↔ Ventilloch + **Konzentrisch** Schlauch-Torus ↔ Felge (Achsen) + **Deckungsgleich** Ebene rechts ↔ Ebene rechts.
4. Genauso den **Mantel** `LR28-003_Mantel` einfügen und mit den drei Ebenen verknüpfen.
5. **Prüfen:** **Extras › Auswerten › Kollisionserkennung** › Berechnen. Erwartet: **„Keine Kollisionen“**. Das Ventil steht durch das Ventilloch (Spiel 0,25 mm radial), der Mantelwulst sitzt auf dem Wulstsitz Ø622 unter dem Felgenhaken.
6. *Optional:* **Explosionsansicht** (Mantel +40 mm in Z, Schlauch +20 mm in Z) für die Präsentation.
7. Eigenschaften der Baugruppe: `Benennung = Laufrad 28" (ohne Nabe/Speichen)`, `Zeichnungsnummer = LR28-000`.
8. Speichern als **`LR28-000_Laufrad.SLDASM`**. Gesamtmasse ≈ **1,33 kg**.

---

## 5. Zeichnungen: Grundeinstellungen (für alle 4 Blätter)

1. **Datei › Neu › Zeichnung** › Blattformat **„A3 (DIN)“** / *a3 - din* (A3 quer, mit Schriftfeld).
2. Rechtsklick auf das Blatt › **Eigenschaften**:
   - Maßstab **1:5**
   - Projektionsart **Erster Winkel** (= DIN ISO 128 Projektionsmethode 1)
   - „Eigenschaftswerte von Modell verwenden, das in Ansicht angezeigt wird“ aktivieren. Dann füllen *Benennung*, *Zeichnungsnummer*, *Werkstoff* und *Masse* das Schriftfeld automatisch.
3. **Extras › Optionen › Dokumenteigenschaften:** Zeichnungsnorm **DIN**, Schrifthöhe 3,5 mm, Pfeile gefüllt, Dezimaltrennzeichen Komma.
4. In jedes Blatt einen Hinweis setzen (**Beschriftung › Notiz**): „Allgemeintoleranzen ISO 2768-m“.
5. Am Ende: **Datei › Speichern unter** › `.SLDDRW`, zusätzlich als **PDF** (und für die Fertigung optional als DXF).

Wichtige Werkzeuge (Registerkarte **Ansichtlayout** bzw. **Beschriftung**):

| Werkzeug | Wozu |
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

### 6.1 Zeichnung LR28-001 Felge (`LR28-001_Felge.SLDDRW`)

1. **Modellansicht** › `LR28-001_Felge` › Ausrichtung **Vorderansicht** › Maßstab **1:5** › links oben platzieren.
2. In der Vorderansicht **Mittellinien** einblenden. **Verdeckte Kanten sichtbar** schalten, damit die radialen Bohrungen als verdeckte Linien erscheinen. Danach Winkelmaße **5°** (Ventilloch ↔ erstes Speichenloch) und **10°** (Lochteilung) setzen.
3. **Schnittansicht** › Schnittlinie **vertikal** durch den Mittelpunkt (Ursprung) › rechts neben der Vorderansicht ablegen › Bezeichnung **A**, Maßstab 1:5.
4. **Detailansicht** › Kreis um das **obere Profil** in Schnitt A–A › Bezeichnung **B** › Maßstab **benutzerdefiniert 5:1** › rechts oben ablegen.
5. **Projizierte Ansicht** aus der Vorderansicht nach unten ziehen. Bei Methode 1 entsteht so die **Draufsicht** (Blick von oben auf das Ventilloch). Darin eine **Detailansicht C** um Ventilloch und die beiden Nachbarlöcher, Maßstab **2:1**. Die Draufsicht selbst kann danach ausgeblendet werden.
6. **Bemaßen** (Soll siehe PDF):
   - Vorderansicht: **Ø634**, **Ø606**, Hinweis „Wulstsitz Ø622 (BSD)“, Notiz „36× Ø4,5 radial, gleichmäßig verteilt, um 5° zum Ventilloch versetzt“
   - Detail B: **23** (Außenbreite), **19** (Maulweite), **8** (Bettboden), **11** (Unterseite), **4** (Wulstsitzbreite), **14** (Profilhöhe), **8** (Hornflanke außen), **6** (Hornhöhe über Wulstsitz), **6** (Betttiefe), **2** (Wandstärke), Hinweis „Hakenlippe 0,5×1“
   - Detail C: **Ø8,5** (Ventilloch), **Ø4,5** (Speichenloch), Abstand **2× 26,5** (≙ 5° auf r = 304)
   - Tipp: **Beschriftung › Modellelemente** › „Für Zeichnung markierte Maße“ übernimmt die Skizzenmaße aus Kapitel 1. Danach nur noch sauber anordnen.
7. Notiz: „Material EN AW-6063 T6, eloxiert. Nicht bemaßte Radien R0,5. Löcher entgratet.“
8. Speichern + PDF.

### 6.2 Zeichnung LR28-002 Schlauch (`LR28-002_Schlauch.SLDDRW`)

1. **Modellansicht** › Vorderansicht 1:5 › Maße **Ø688** (außen) und **Ø632** (innen). Hinweis „Ventil AV bei 12 Uhr“.
2. **Schnittansicht A–A** vertikal durch den Mittelpunkt. Die Schnittlinie läuft dabei **durch das Ventil**.
3. **Detailansicht B** um Schlauchquerschnitt + Ventil, Maßstab **2:1**.
4. Bemaßen: **Ø28**, Wand **0,9**, Ventilschaft **Ø8 (8V1)**, Kappe **Ø10**, Kappenlänge **12**, Ventillänge **36** (von der Kappe bis zur Schlauchwand).
5. Notiz: „Größe 28" × 1 3/8–1 5/8 (ETRTO 32/47-622), Butyl. Ventil AV 40 mm, max. 4,5 bar. Einbauzustand vereinfacht als Torus.“

### 6.3 Zeichnung LR28-003 Mantel (`LR28-003_Mantel.SLDDRW`)

1. Vorderansicht 1:5 mit **Ø696** (außen) und **Ø622 (Wulst)**.
2. **Schnittansicht A–A**, dann **Detailansicht B** (Querschnitt oben), Maßstab **2,5:1**.
3. Bemaßen: Breite **37**, Höhe **37**, **R18,5**, **R15,5**, **18,5** (Wulst bis Bogenmitte), Wulstabstand **19** außen / **11** innen, Wulsthöhe **6**, Hinweis „Lauffläche 3“, „Wulst mit Drahtkern“.
4. Notiz: „Größe 37-622 (28 × 1.40), Drahtreifen, 50 TPI, max. 4,5 bar. Reflexstreifen und Profil nicht dargestellt.“

### 6.4 Zusammenbauzeichnung LR28-000 (`LR28-000_Laufrad.SLDDRW`)

1. Vorderansicht 1:5 mit **Ø696**.
2. **Schnittansicht A–A**. Im Dialog „Schnittansicht“ **keine** Komponente vom Schnitt ausschließen; SolidWorks schraffiert jedes Teil automatisch unterschiedlich.
3. **Detailansicht B** über dem Profil, Maßstab **2,5:1**, mit den Einbaumaßen **37** (Reifenbreite) und **45** (Felgenboden bis Lauffläche).
4. **Tabellen › Stückliste** › Vorlage *bom-standard* › oberhalb des Schriftfelds verankern. Spalten: Pos. | Menge | Benennung | Sachnummer | Werkstoff | Masse. Diese werden aus den Dateieigenschaften gefüllt.
5. **Automatische Positionsnummer** in Detail B: **1** Felge, **2** Schlauch, **3** Mantel.
6. Notiz „Reifendruck 3,5–4,5 bar“. Speichern + PDF.

---

## 7. Automatisch per Makro (`solidworks_makros/Laufrad28.bas`)

1. SolidWorks öffnen › **Extras › Makro › Neu…** › z. B. `Laufrad28.swp` speichern. Der VBA-Editor öffnet sich.
2. Im VBA-Editor **Datei › Datei importieren…** › `Laufrad28.bas`. Das leere `Module1` kann gelöscht werden.
3. **F5** › `main` ausführen.
4. Ergebnis im Unterordner `Laufrad28\` neben der .swp-Datei:
   `LR28-001_Felge.SLDPRT`, `LR28-002_Schlauch.SLDPRT`, `LR28-003_Mantel.SLDPRT`, `LR28-000_Laufrad.SLDASM` und vier `.SLDDRW` mit **Vorderansicht 1:5 + Isometrie**.
5. Schnitt A–A, Details, Maße und Stückliste danach wie in Kapitel 6 ergänzen. Die Makro-Skizzen haben keine Maße (die Geometrie ist exakt über Koordinaten erzeugt), also die Maße per **Intelligenter Bemaßung** direkt in der Zeichnung setzen.

Hinweise zum Makro:
- Es nutzt die **Standardvorlagen** aus *Extras › Optionen › Standardvorlagen*. Diese müssen gesetzt sein.
- Es ist **sprachunabhängig**: Die Ebenen werden über ihre Reihenfolge gefunden, nicht über ihren Namen.
- Gelingt ein Schritt nicht (z. B. Kreismuster oder Verknüpfung in einer älteren Version), weicht das Makro aus: Es erzeugt einzelne Löcher bzw. fixiert die Komponente. Am Ende zeigt es eine Hinweisliste.
- Getestet wurde die Geometrie (identisch zu den STEP-Dateien). Das Makro selbst konnte ohne SolidWorks-Lizenz nicht ausgeführt werden. Bei einer Fehlermeldung bitte die Zeile notieren.

## 8. STEP-Dateien verwenden

- `cad_step/Felge.step`, `Schlauch.step`, `Mantel.step`: Einzelteile
- `cad_step/Laufrad_Baugruppe.step`: Baugruppe mit allen drei Teilen (öffnet als `.SLDASM`)

Öffnen über **Datei › Öffnen › STEP**. Mit **FeatureWorks** (Rechtsklick auf „Importiert1“ › Features erkennen) lassen sich die Rotationen und Bohrungen wieder als bearbeitbare Features erkennen.

## 9. Zusammenfassung der Hauptmaße

| | Felge | Schlauch | Mantel | Laufrad |
|---|---|---|---|---|
| Außen-Ø | 634 | 688 | **696** | 696 |
| Innen-Ø | 606 | 632 | 622 (Wulst) | 606 |
| Breite | 23 (Maul 19) | 28 | **37** | 37 |
| Werkstoff | EN AW-6063 T6 | Butyl IIR | NR/SBR | – |
| Masse | 465 g | 148 g | 716 g | 1,33 kg |
| Norm | ETRTO 19-622 | 32/47-622 | ETRTO 37-622 | – |
