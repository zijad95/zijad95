"""Gemeinsame Geometriedaten: Fahrradanhaenger-Rad 20" (ETRTO 406).

Felge 406x19 (einwandig, Alu, 36 Loch, AV), Schlauch 20x1.75 AV, Mantel 47-406.

Koordinatensystem (identisch zu SolidWorks bei Skizze auf "Ebene rechts"):
  - Radachse          = Z-Achse
  - Profil-Koordinate = (z, r)  ->  z = axial (Breite), r = radial (Abstand zur Achse)
  - Ventil liegt bei +Y (oben, 90 Grad)
Alle Masse in Millimeter.
"""
import math

RB = 203.0  # Wulstsitzradius = BSD/2 (Bead Seat Diameter 406)

# ---------------------------------------------------------------- Felge ----
# Einwandige Aluminium-Hakenfelge 406x19 (ETRTO 19-406), 36 Loch, AV-Ventil
FELGE = dict(
    bsd=2 * RB,
    maulweite=19.0,
    aussenbreite=23.0,
    hornhoehe=6.0,
    wand=2.0,
    speichenloecher=36,
    speichenloch_d=4.5,
    ventilloch_d=8.5,          # AV (Schrader / Autoventil)
    r_aussen=RB + 6.0,         # 209  -> D418 Hornoberkante
    r_unten=RB - 8.0,          # 195  -> D390 Felgenboden unten
    r_bett=RB - 6.0,           # 197  -> D394 Tiefbettboden
)

# Profil rechte Haelfte (z >= 0), wird an z = 0 gespiegelt.
FELGE_PROFIL_HALB = [
    (0.0, RB - 6.0),     # P1  Tiefbettboden (Reifenseite)
    (4.0, RB - 6.0),     # P2
    (5.5, RB),           # P3  Schraege hoch zum Wulstsitz
    (9.5, RB),           # P4  Wulstsitz (BSD 406)
    (9.5, RB + 4.5),     # P5  Hornflanke innen
    (9.0, RB + 5.0),     # P6  Hakenlippe
    (9.0, RB + 6.0),     # P7  Hornoberkante innen
    (11.5, RB + 6.0),    # P8  Hornoberkante aussen
    (11.5, RB - 2.0),    # P9  Hornflanke aussen
    (7.0, RB - 2.0),     # P10 Unterseite Wulstsitz
    (5.5, RB - 8.0),     # P11 Unterseite Schraege
    (0.0, RB - 8.0),     # P12 Felgenboden Unterseite
]

# ------------------------------------------------------------- Mantel ----
# Drahtreifen 47-406 (20 x 1.75), Aussendurchmesser 500 mm
MANTEL = dict(
    etrto="47-406",
    breite=47.0,
    aussen_d=500.0,
    r_mitte=RB + 23.5,    # 226,5  Mittelpunkt der Querschnittsboegen
    r_aussen=23.5,        # Aussenbogen (Breite 47)
    r_innen=20.5,         # Innenbogen -> Laufflaeche 3 mm
)


def _kreis_z(r_mitte, radius, r):
    """z-Koordinate (>0) eines Kreises um (0, r_mitte) auf Hoehe r."""
    return math.sqrt(radius ** 2 - (r - r_mitte) ** 2)


T7_R = RB + 7.5   # 210,5  Uebergang Flanke -> Aussenbogen
T8_R = RB + 10.0  # 213    Uebergang Wulst -> Innenbogen
_ZA = _kreis_z(MANTEL["r_mitte"], MANTEL["r_aussen"], T7_R)   # 17,21
_ZI = _kreis_z(MANTEL["r_mitte"], MANTEL["r_innen"], T8_R)    # 15,43

MANTEL_PUNKTE_HALB = dict(
    T1=(5.5, RB),          # Wulst innen unten
    T2=(9.5, RB),          # Wulst aussen unten (liegt auf Wulstsitz)
    T3=(9.5, RB + 4.5),    # Wulst an Hornflanke
    T4=(9.0, RB + 5.0),    # unter Hakenlippe
    T5=(9.0, RB + 6.0),
    T6=(11.5, RB + 6.0),   # liegt auf Hornoberkante
    T7=(_ZA, T7_R),        # Uebergang in Aussenbogen R23,5
    T8=(_ZI, T8_R),        # Uebergang in Innenbogen R20,5
    T9=(5.5, RB + 7.0),    # Wulst innen oben
)

# ------------------------------------------------------------ Schlauch ----
# Butylschlauch 20 x 1.75-2.125 (ETRTO 47/57-406) mit AV-Ventil 35 mm
SCHLAUCH = dict(
    r_mitte=RB + 25.5,    # 228,5 Torus-Mittenradius
    r_aussen=18.3,        # Querschnitt aussen (D 36,6)
    wand=1.0,
    ventil_d=8.0,
    ventil_oben=RB + 7.7,     # 210,7 Ventilschaft endet in der Schlauchwand
    ventil_unten=RB - 27.0,   # 176
    kappe_d=10.0,
    kappe_oben=RB - 17.0,     # 186
    kappe_unten=RB - 29.0,    # 174
)

DICHTE = {  # g/cm^3
    "Felge": 2.70,      # EN AW-6063 (AlMgSi0,5)
    "Schlauch": 0.92,   # Butylkautschuk (IIR)
    "Mantel": 1.15,     # Gummimischung (NR/SBR) mit Karkasse
}

NUMMER = {"Baugruppe": "AR20-000", "Felge": "AR20-001", "Schlauch": "AR20-002",
          "Mantel": "AR20-003"}


def felge_kontur():
    """Geschlossenes Felgenprofil (rechte Haelfte + gespiegelte linke Haelfte)."""
    h = FELGE_PROFIL_HALB
    links = [(-z, r) for z, r in reversed(h[1:-1])]
    return h + links
