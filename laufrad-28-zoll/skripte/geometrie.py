"""Gemeinsame Geometriedaten fuer Felge, Schlauch und Mantel (28" / ETRTO 622).

Koordinatensystem (identisch zu SolidWorks bei Skizze auf "Ebene rechts"):
  - Radachse          = Z-Achse
  - Profil-Koordinate = (z, r)  ->  z = axial (Breite), r = radial (Abstand zur Achse)
  - Ventil liegt bei +Y (oben, 90 Grad)
Alle Masse in Millimeter.
"""
import math

# ---------------------------------------------------------------- Felge ----
# Einwandige Aluminium-Hakenfelge 622x19 (ETRTO 19-622), 36 Loch, AV-Ventil
FELGE = dict(
    bsd=622.0,            # Bead Seat Diameter (Wulstsitzdurchmesser)
    maulweite=19.0,       # Innenbreite zwischen den Hornen
    aussenbreite=23.0,
    hornhoehe=6.0,        # Horn ueber Wulstsitz
    wand=2.0,
    speichenloecher=36,
    speichenloch_d=4.5,
    ventilloch_d=8.5,     # AV (Schrader / Autoventil)
)

# Profil rechte Haelfte (z >= 0), wird an z = 0 gespiegelt.
# Reihenfolge: Bettmitte innen -> Horn -> aussen herum -> Unterseite Mitte
FELGE_PROFIL_HALB = [
    (0.0, 305.0),    # P1  Tiefbettboden (Reifenseite)
    (4.0, 305.0),    # P2
    (5.5, 311.0),    # P3  Schraege hoch zum Wulstsitz
    (9.5, 311.0),    # P4  Wulstsitz (BSD 622)
    (9.5, 315.5),    # P5  Hornflanke innen
    (9.0, 316.0),    # P6  Hakenlippe
    (9.0, 317.0),    # P7  Hornoberkante innen
    (11.5, 317.0),   # P8  Hornoberkante aussen
    (11.5, 309.0),   # P9  Hornflanke aussen
    (7.0, 309.0),    # P10 Unterseite Wulstsitz
    (5.5, 303.0),    # P11 Unterseite Schraege
    (0.0, 303.0),    # P12 Felgenboden Unterseite
]

# ------------------------------------------------------------- Mantel ----
# Drahtreifen 37-622 (28 x 1.40), Aussendurchmesser ~ 696 mm
MANTEL = dict(
    etrto="37-622",
    breite=37.0,
    aussen_d=696.0,
    r_mitte=329.5,        # Mittelpunkt der Querschnittsboegen
    r_aussen=18.5,        # Aussenbogen (Breite 37)
    r_innen=15.5,         # Innenbogen (Karkasse innen)
)


def _kreis_z(r_mitte, radius, r):
    """z-Koordinate (>0) eines Kreises um (0, r_mitte) auf Hoehe r."""
    return math.sqrt(radius ** 2 - (r - r_mitte) ** 2)


_ZA = round(_kreis_z(MANTEL["r_mitte"], MANTEL["r_aussen"], 318.5), 2)  # 14.87
_ZI = round(_kreis_z(MANTEL["r_mitte"], MANTEL["r_innen"], 320.0), 2)   # 12.25

# Geschlossene Kontur rechte Seite (z>0) von Wulst unten innen nach aussen oben.
MANTEL_PUNKTE_HALB = dict(
    T1=(5.5, 311.0),     # Wulst innen unten
    T2=(9.5, 311.0),     # Wulst aussen unten (liegt auf Wulstsitz)
    T3=(9.5, 315.5),     # Wulst an Hornflanke
    T4=(9.0, 316.0),     # unter Hakenlippe
    T5=(9.0, 317.0),
    T6=(11.5, 317.0),    # liegt auf Hornoberkante
    T7=(_ZA, 318.5),     # Uebergang in Aussenbogen R18.5
    T8=(_ZI, 320.0),     # Uebergang in Innenbogen R15.5
    T9=(5.5, 317.0),     # Wulst innen oben
)

# ------------------------------------------------------------ Schlauch ----
# Butylschlauch 28" (ETRTO 32/47-622) mit AV-Ventil 40 mm
SCHLAUCH = dict(
    r_mitte=330.0,        # Torus-Mittenradius
    r_aussen=14.0,        # Querschnitt aussen (D 28)
    wand=0.9,
    ventil_d=8.0,
    ventil_oben=316.5,    # Ventilschaft beginnt in der Schlauchwand
    ventil_unten=282.0,   # Ende Ventilschaft
    kappe_d=10.0,
    kappe_oben=292.0,
    kappe_unten=280.0,
)

DICHTE = {  # g/cm^3
    "Felge": 2.70,      # EN AW-6063 (AlMgSi0,5)
    "Schlauch": 0.92,   # Butylkautschuk (IIR)
    "Mantel": 1.15,     # Gummimischung (NR/SBR) mit Karkasse
}


def felge_kontur():
    """Geschlossenes Felgenprofil (ohne Doppelpunkte auf der Achse)."""
    h = FELGE_PROFIL_HALB
    # rechte Haelfte P1..P12, dann linke Haelfte P11'..P2' (rueckwaerts)
    links = [(-z, r) for z, r in reversed(h[1:-1])]
    return h + links
