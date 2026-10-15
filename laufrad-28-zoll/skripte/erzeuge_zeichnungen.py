"""Erzeugt bemasste Referenzzeichnungen (DIN A3 quer, PDF) fuer Felge, Schlauch,
Mantel und Baugruppe. Sie zeigen, wie die SolidWorks-Zeichnungen am Ende
aussehen sollen (Ansichten, Schnitte, Masse, Schriftfeld, Stueckliste).

Aufruf:  python erzeuge_zeichnungen.py      (benoetigt: pip install matplotlib)
Ausgabe: ../zeichnungen/*.pdf und *.png
"""
import datetime
import math
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Arc, Circle, Polygon

from geometrie import (FELGE, MANTEL, MANTEL_PUNKTE_HALB, SCHLAUCH,
                       felge_kontur)

AUS = pathlib.Path(__file__).resolve().parent.parent / "zeichnungen"
AUS.mkdir(exist_ok=True)

LW_DICK, LW_DUENN = 0.7, 0.35  # Linienbreiten in pt (ca. 0,5 / 0,25 mm)
TXT = 3.5                       # Schrifthoehe in mm
PT_PRO_MM = 72 / 25.4
DATUM = datetime.date.today().strftime("%d.%m.%Y")
SAMMEL = None  # PdfPages fuer den gesamten Zeichnungssatz


def f(x):
    """Zahl im deutschen Format (Komma, ohne unnoetige Nullen)."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


class Blatt:
    """DIN-A3-Blatt; alle Koordinaten in Papier-mm, Ursprung unten links."""

    def __init__(self):
        self.fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, 420)
        self.ax.set_ylim(0, 297)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.rahmen()

    # ---------------------------------------------------------- Grundlagen
    def linie(self, pts, lw=LW_DICK, ls="-", c="k", z=3):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle="butt", zorder=z)

    def mittellinie(self, p1, p2):
        self.linie([p1, p2], lw=LW_DUENN, ls=(0, (12, 3, 2, 3)))

    def text(self, x, y, s, h=TXT, ha="center", va="center", rot=0, bold=False):
        self.ax.text(x, y, s, fontsize=h * PT_PRO_MM / 0.72, ha=ha, va=va, rotation=rot,
                     fontweight="bold" if bold else "normal", family="DejaVu Sans",
                     rotation_mode="anchor", zorder=6)

    def pfeil(self, spitze, richtung, laenge=3.0, breite=1.0):
        dx, dy = richtung
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        bx, by = spitze[0] - dx * laenge, spitze[1] - dy * laenge
        px, py = -dy * breite / 2, dx * breite / 2
        self.ax.add_patch(Polygon([spitze, (bx + px, by + py), (bx - px, by - py)],
                                  closed=True, fc="k", ec="k", lw=0.2, zorder=5))

    def mass(self, p1, p2, abstand, txt, richtung="h", txt_pos=0.5):
        """Lineares Mass zwischen p1 und p2 (Papier-mm). richtung 'h' oder 'v'."""
        if richtung == "h":
            y = p1[1] + abstand if abstand else p1[1]
            y = max(p1[1], p2[1]) + abstand if abstand > 0 else min(p1[1], p2[1]) + abstand
            a, b = (p1[0], y), (p2[0], y)
            for p in (p1, p2):
                s = 1 if y > p[1] else -1
                self.linie([(p[0], p[1] + s * 1.0), (p[0], y + s * 2.0)], lw=LW_DUENN)
        else:
            x = max(p1[0], p2[0]) + abstand if abstand > 0 else min(p1[0], p2[0]) + abstand
            a, b = (x, p1[1]), (x, p2[1])
            for p in (p1, p2):
                s = 1 if x > p[0] else -1
                self.linie([(p[0] + s * 1.0, p[1]), (x + s * 2.0, p[1])], lw=LW_DUENN)
        laenge = math.dist(a, b)
        d = ((b[0] - a[0]) / laenge, (b[1] - a[1]) / laenge)
        if laenge > 8:
            self.linie([a, b], lw=LW_DUENN)
            self.pfeil(a, (-d[0], -d[1]))
            self.pfeil(b, d)
        else:  # Pfeile von aussen
            self.linie([(a[0] - d[0] * 7, a[1] - d[1] * 7), (b[0] + d[0] * 7, b[1] + d[1] * 7)],
                       lw=LW_DUENN)
            self.pfeil(a, d)
            self.pfeil(b, (-d[0], -d[1]))
        mx = a[0] + (b[0] - a[0]) * txt_pos
        my = a[1] + (b[1] - a[1]) * txt_pos
        if richtung == "h":
            self.text(mx, my + 1.0, txt, va="bottom")
        else:
            self.text(mx - 1.0, my, txt, va="bottom", rot=90)

    def radius(self, mitte, r, winkel, txt, aussen=10):
        """Radiusmass: Pfeil auf Kreisbogen von innen, Text aussen."""
        w = math.radians(winkel)
        d = (math.cos(w), math.sin(w))
        p = (mitte[0] + d[0] * r, mitte[1] + d[1] * r)
        q = (p[0] + d[0] * aussen, p[1] + d[1] * aussen)
        self.linie([mitte, q], lw=LW_DUENN)
        self.pfeil(p, d)
        self.text(q[0] + (2 if d[0] >= 0 else -2), q[1], txt,
                  ha="left" if d[0] >= 0 else "right")

    def durchmesser(self, mitte, r, winkel, txt, aussen=12):
        """Durchmessermass: Masslinie durch die Mitte, Text ausserhalb des Kreises."""
        w = math.radians(winkel)
        d = (math.cos(w), math.sin(w))
        p1 = (mitte[0] - d[0] * r, mitte[1] - d[1] * r)
        p2 = (mitte[0] + d[0] * r, mitte[1] + d[1] * r)
        q = (p2[0] + d[0] * aussen, p2[1] + d[1] * aussen)
        self.linie([p1, q], lw=LW_DUENN)
        q2 = (q[0] + (8 if d[0] >= 0 else -8), q[1])
        self.linie([q, q2], lw=LW_DUENN)
        self.pfeil(p1, (-d[0], -d[1]))
        self.pfeil(p2, d)
        self.text(q2[0], q2[1] + 1, txt, va="bottom", ha="right" if d[0] >= 0 else "left")

    def hinweis(self, ziel, text_pos, txt):
        self.linie([ziel, text_pos], lw=LW_DUENN)
        self.ax.add_patch(Circle(ziel, 0.6, color="k", zorder=5))
        self.text(text_pos[0] + (1 if text_pos[0] >= ziel[0] else -1), text_pos[1], txt,
                  ha="left" if text_pos[0] >= ziel[0] else "right")

    def schraffur(self, pts, hatch="////"):
        self.ax.add_patch(Polygon(pts, closed=True, fc="none", ec="k", lw=LW_DICK,
                                  hatch=hatch, zorder=2))

    def kreis(self, mitte, r, lw=LW_DICK, ls="-"):
        self.ax.add_patch(Circle(mitte, r, fc="none", ec="k", lw=lw, ls=ls, zorder=3))

    # ------------------------------------------------------- Blattaufbau
    def rahmen(self):
        self.linie([(20, 10), (410, 10), (410, 287), (20, 287), (20, 10)], lw=1.0)
        # Feldeinteilung
        for i in range(1, 8):
            x = 20 + i * 390 / 8
            self.linie([(x, 287), (x, 292)], lw=LW_DUENN)
            self.linie([(x, 10), (x, 5)], lw=LW_DUENN)
        for i in range(8):
            self.text(20 + (i + 0.5) * 390 / 8, 289.5, str(i + 1), h=2.5)
            self.text(20 + (i + 0.5) * 390 / 8, 7.5, str(i + 1), h=2.5)
        for i, b in enumerate("DCBA"):
            self.text(15, 10 + (i + 0.5) * 277 / 4, b, h=2.5)

    def schriftfeld(self, benennung, nummer, werkstoff, massstab, masse, blatt="1/1",
                    zusatz="Allgemeintoleranzen ISO 2768-m"):
        x0, y0, b, h = 230, 10, 180, 40
        self.linie([(x0, y0), (x0, y0 + h), (x0 + b, y0 + h)], lw=1.0)
        for y in (y0 + 10, y0 + 20, y0 + 30):
            self.linie([(x0, y), (x0 + b, y)], lw=LW_DUENN)
        for x in (x0 + 60, x0 + 120):
            self.linie([(x, y0 + 20), (x, y0 + 40)], lw=LW_DUENN)
        self.linie([(x0 + 140, y0), (x0 + 140, y0 + 20)], lw=LW_DUENN)
        k = 2.0
        def feld(x, y, titel, inhalt, bold=False, hh=TXT):
            self.text(x + 1.5, y + 8, titel, h=k, ha="left")
            self.text(x + 1.5, y + 3.5, inhalt, h=hh, ha="left", bold=bold)
        feld(x0, y0 + 30, "Werkstoff", werkstoff)
        feld(x0 + 60, y0 + 30, "Masstab", massstab)
        feld(x0 + 120, y0 + 30, "Masse", masse)
        feld(x0, y0 + 20, "Gezeichnet", f"{DATUM}")
        feld(x0 + 60, y0 + 20, "Projektionsmethode", "1 (DIN ISO 128)")
        feld(x0 + 120, y0 + 20, "Format", "A3")
        feld(x0, y0 + 10, "Benennung", benennung, bold=True, hh=4.5)
        feld(x0, y0, "Zeichnungsnummer", nummer, bold=True)
        feld(x0 + 140, y0 + 10, "Blatt", blatt)
        feld(x0 + 140, y0, "Status", "Entwurf")
        self.text(x0 + 1.5, y0 + h + 3, zusatz, h=2.5, ha="left")
        self.projektionssymbol(x0 + 165, y0 + 25)

    def projektionssymbol(self, x, y):
        # Methode 1: Kegelstumpf (Seitenansicht) rechts vom Kreis
        self.kreis((x - 4, y), 1.5, lw=LW_DUENN)
        self.kreis((x - 4, y), 3.0, lw=LW_DUENN)
        self.linie([(x + 1, y - 1.5), (x + 1, y + 1.5), (x + 7, y + 3), (x + 7, y - 3),
                    (x + 1, y - 1.5)], lw=LW_DUENN)

    def speichern(self, name):
        self.fig.savefig(AUS / f"{name}.pdf")
        self.fig.savefig(AUS / f"{name}.png", dpi=110)
        if SAMMEL is not None:
            SAMMEL.savefig(self.fig)
        plt.close(self.fig)
        print("geschrieben:", name)


# ------------------------------------------------------------------ Helfer
def transform(ursprung, massstab, flip_z=False):
    """Modell (z, r) -> Papier (x, y)."""
    ox, oy = ursprung
    sz = -1 if flip_z else 1
    return lambda p: (ox + sz * p[0] * massstab, oy + p[1] * massstab)


def mantel_kontur(n=40):
    p = MANTEL_PUNKTE_HALB
    rm, ra, ri = MANTEL["r_mitte"], MANTEL["r_aussen"], MANTEL["r_innen"]
    m = lambda q: (-q[0], q[1])

    def bogen(r, von, bis):
        a0 = math.atan2(von[1] - rm, von[0])
        a1 = math.atan2(bis[1] - rm, bis[0])
        if a1 < a0:
            a1 += 2 * math.pi
        return [(r * math.cos(a0 + (a1 - a0) * i / n), rm + r * math.sin(a0 + (a1 - a0) * i / n))
                for i in range(n + 1)]
    pts = [p["T1"], p["T2"], p["T3"], p["T4"], p["T5"], p["T6"]]
    pts += bogen(ra, p["T7"], m(p["T7"]))
    pts += [m(p["T6"]), m(p["T5"]), m(p["T4"]), m(p["T3"]), m(p["T2"]), m(p["T1"]),
            m(p["T9"])]
    innen = bogen(ri, p["T8"], m(p["T8"]))
    pts += list(reversed(innen))
    pts += [p["T9"]]
    return pts


def schlauch_ringe(n=90):
    s = SCHLAUCH
    def kreis(r):
        return [(r * math.cos(2 * math.pi * i / n), s["r_mitte"] + r * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]
    return kreis(s["r_aussen"]), kreis(s["r_aussen"] - s["wand"])


def vorderansicht(bl, mitte, m, radien, gestrichelt=()):
    for r in radien:
        bl.kreis(mitte, r * m)
    for r in gestrichelt:
        bl.kreis(mitte, r * m, lw=LW_DUENN, ls=(0, (4, 2)))
    gr = max(radien) * m + 5
    bl.mittellinie((mitte[0] - gr, mitte[1]), (mitte[0] + gr, mitte[1]))
    bl.mittellinie((mitte[0], mitte[1] - gr), (mitte[0], mitte[1] + gr))


def schnittkennung(bl, x, y_oben, y_unten, buchstabe="A"):
    """Schnittverlauf A-A als senkrechte Linie mit Blickrichtungspfeilen."""
    for y, s in ((y_oben, 1), (y_unten, -1)):
        bl.linie([(x, y), (x, y + s * 6)], lw=1.2)
        bl.linie([(x, y + s * 6), (x - 8, y + s * 6)], lw=LW_DUENN)
        bl.pfeil((x - 8, y + s * 6), (-1, 0), laenge=3, breite=1.2)
        bl.text(x - 12, y + s * 6 + 3 * s, buchstabe, h=5)


def schnitt_klein(bl, x, cy, m, konturen, kanten, detail_r=None, extra=None):
    """Kleine Schnittansicht A-A (Schnitt durch die Radachse) im Massstab m.

    konturen: Liste von (punkte, schraffur); kanten: (z, r) sichtbarer Kreiskanten,
    die im Schnitt als senkrechte Linien zwischen oberem und unterem Profil erscheinen.
    """
    for pts, hatch in konturen:
        for sgn in (1, -1):
            poly = [(x + z * m, cy + sgn * r * m) for z, r in pts]
            bl.ax.add_patch(Polygon(poly, closed=True, fc="white" if hatch is None else "none",
                                    ec="k", lw=LW_DUENN, hatch=hatch, zorder=2))
    for z, r in kanten:
        for sz in (1, -1):
            bl.linie([(x + sz * z * m, cy - r * m), (x + sz * z * m, cy + r * m)], lw=LW_DUENN)
    if extra:
        extra(x, cy, m)
    rmax = max(r for pts, _ in konturen for _, r in pts)
    bl.mittellinie((x - 12, cy), (x + 12, cy))
    bl.mittellinie((x, cy - rmax * m - 4), (x, cy + rmax * m + 4))
    bl.text(x, cy + rmax * m + 16, "Schnitt A–A  M 1:5", h=4, bold=True)
    if detail_r:
        yb = cy + detail_r * m
        bl.kreis((x, yb), 7, lw=LW_DUENN)
        bl.text(x + 9, yb + 6, "B", h=5)


# ================================================================ Felge ====
def zeichnung_felge():
    bl = Blatt()
    # --- Vorderansicht 1:5
    m1, c = 0.2, (95, 185)
    vorderansicht(bl, c, m1, [317, 303], gestrichelt=[311])
    # Speichenlochpositionen (radiale Bohrungen -> Mittellinien)
    for i in range(36):
        w = math.radians(95 + i * 10)
        p1 = (c[0] + 299 * m1 * math.cos(w), c[1] + 299 * m1 * math.sin(w))
        p2 = (c[0] + 321 * m1 * math.cos(w), c[1] + 321 * m1 * math.sin(w))
        bl.linie([p1, p2], lw=LW_DUENN, ls=(0, (6, 1.5, 1, 1.5)))
    bl.linie([(c[0], c[1] + 296 * m1), (c[0], c[1] + 324 * m1)], lw=LW_DICK)
    bl.hinweis((c[0], c[1] + 305 * m1), (c[0] - 30, c[1] + 42), "Ventilloch Ø8,5")
    # Winkel 5 Grad / 10 Grad (innerhalb des Kreises)
    for a0, a1, t, dx in ((90, 95, "5°", -3), (95, 105, "10°", -10)):
        for a in (a0, a1):
            w = math.radians(a)
            bl.linie([c, (c[0] + 56 * math.cos(w), c[1] + 56 * math.sin(w))], lw=LW_DUENN,
                     ls=(0, (6, 1.5, 1, 1.5)))
        bl.ax.add_patch(Arc(c, 100, 100, theta1=a0, theta2=a1, lw=LW_DUENN, zorder=3))
        bl.text(c[0] + dx, c[1] + 46, t, h=2.5)
    bl.durchmesser(c, 317 * m1, 35, "Ø634")
    bl.durchmesser(c, 303 * m1, -35, "Ø606", aussen=20)
    bl.hinweis((c[0] + 311 * m1 * math.cos(math.radians(-60)), c[1] + 311 * m1 * math.sin(math.radians(-60))),
               (c[0] + 55, c[1] - 78), "Wulstsitz Ø622 (BSD)")
    bl.text(c[0], 98, "36× Ø4,5 radial, gleichmäßig verteilt,", h=2.5)
    bl.text(c[0], 94, "um 5° zum Ventilloch versetzt", h=2.5)
    schnittkennung(bl, c[0], c[1] + 70, c[1] - 70)
    bl.text(c[0], 274, "Vorderansicht  M 1:5", h=4, bold=True)

    # --- Schnitt A-A Profil 5:1
    m5, o = 5.0, (300, -1365)   # r=303 -> y = 150
    T = transform(o, m5)
    k = [T(p) for p in felge_kontur()]
    bl.schraffur(k)
    bl.mittellinie(T((0, 300)), T((0, 320.5)))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 5:1", h=4, bold=True)
    schnitt_klein(bl, 190, c[1], m1, [(felge_kontur(), "////")],
                  [(5.5, 303), (7.0, 309), (11.5, 309)], detail_r=310)
    # Masse
    bl.mass(T((-11.5, 317)), T((11.5, 317)), 14, "23", "h")
    bl.mass(T((-9.5, 315.5)), T((9.5, 315.5)), 31, "19 (Maulweite)", "h")
    bl.mass(T((-4, 305)), T((4, 305)), -27, "8", "h")
    bl.mass(T((-5.5, 303)), T((5.5, 303)), -10, "11", "h")
    bl.mass(T((5.5, 311)), T((9.5, 311)), -8, "4", "h")
    bl.mass(T((11.5, 309)), T((11.5, 317)), 10, "8", "v")
    bl.mass(T((9.5, 311)), T((11.5, 317)), 24, "6", "v")
    bl.mass(T((11.5, 303)), T((11.5, 317)), 38, "14", "v")
    bl.mass(T((-4, 303)), T((-4, 305)), -42, "2", "v")
    bl.mass(T((-9.5, 311)), T((-9.5, 305)), -26, "6 (Betttiefe)", "v")
    bl.hinweis(T((9.0, 316.5)), (360, 262), "Hakenlippe 0,5×1")
    bl.hinweis(T((7.5, 311)), (350, 128), "Wulstsitz Ø622")
    bl.hinweis(T((0, 304)), (245, 95), "Ø4,5 Speichen- / Ø8,5 Ventilloch")
    bl.text(300, 108, "Schnittfläche zeigt das Rotationsprofil;", h=2.5)
    bl.text(300, 104, "untere Hälfte symmetrisch.", h=2.5)

    # --- Detail C aus der Draufsicht (Blick von aussen auf das Ventilloch) 2:1
    m2, c2 = 2.0, (95, 42)
    r_ab = 304.0  # Mittelflaeche Felgenboden
    x5 = r_ab * math.sin(math.radians(5)) * m2
    bl.linie([(c2[0] - 70, c2[1] - 11.5 * m2), (c2[0] + 70, c2[1] - 11.5 * m2)])
    bl.linie([(c2[0] - 70, c2[1] + 11.5 * m2), (c2[0] + 70, c2[1] + 11.5 * m2)])
    for zz in (-5.5, 5.5):
        bl.linie([(c2[0] - 70, c2[1] + zz * m2), (c2[0] + 70, c2[1] + zz * m2)], lw=LW_DUENN)
    bl.kreis(c2, 4.25 * m2)
    for s in (-1, 1):
        bl.kreis((c2[0] + s * x5, c2[1]), 2.25 * m2)
        bl.mittellinie((c2[0] + s * x5, c2[1] - 7), (c2[0] + s * x5, c2[1] + 7))
    bl.mittellinie((c2[0] - 72, c2[1]), (c2[0] + 72, c2[1]))
    bl.mittellinie((c2[0], c2[1] - 12), (c2[0], c2[1] + 12))
    bl.mass((c2[0] - x5, c2[1] + 2.25 * m2), (c2[0] + x5, c2[1] + 2.25 * m2), 22,
            f"2× {f(round(r_ab * math.sin(math.radians(5)), 1))} (≙ 5°)", "h")
    bl.hinweis((c2[0] + 4.25 * m2 * 0.7, c2[1] - 4.25 * m2 * 0.7), (c2[0] + 40, c2[1] - 25), "Ø8,5")
    bl.hinweis((c2[0] + x5 + 1.6 * m2, c2[1] - 1.6 * m2), (c2[0] + 78, c2[1] - 18), "Ø4,5")
    bl.text(c2[0], c2[1] + 38, "Detail C (aus Draufsicht)  M 2:1", h=4, bold=True)

    bl.text(232, 64, "Material: EN AW-6063 T6, eloxiert (silber). Stoß gepinnt.", h=2.5, ha="left")
    bl.text(232, 60, "Nicht bemaßte Radien R0,5. Ventilloch und Speichenlöcher entgratet.", h=2.5, ha="left")
    bl.schriftfeld("Felge 622×19, 36 Loch, AV", "LR28-001", "EN AW-6063 T6", "1:5 / 5:1 / 2:1",
                   "≈ 465 g")
    bl.speichern("LR28-001_Felge")


# ============================================================== Schlauch ===
def zeichnung_schlauch():
    bl = Blatt()
    s = SCHLAUCH
    m1, c = 0.2, (95, 160)
    vorderansicht(bl, c, m1, [s["r_mitte"] + s["r_aussen"], s["r_mitte"] - s["r_aussen"]],
                  gestrichelt=[s["r_mitte"]])
    # Ventil
    for sx in (-0.8, 0.8):
        bl.linie([(c[0] + sx, c[1] + 316 * m1), (c[0] + sx, c[1] + 282 * m1)])
    bl.durchmesser(c, 344 * m1, 35, "Ø688")
    bl.durchmesser(c, 316 * m1, -35, "Ø632", aussen=20)
    schnittkennung(bl, c[0], c[1] + 72, c[1] - 72)
    bl.text(c[0], 274, "Vorderansicht  M 1:5", h=4, bold=True)
    bl.hinweis((c[0], c[1] + 290 * m1), (c[0] - 20, c[1] + 28), "Ventil AV bei 12 Uhr")

    # Schnitt A-A 2:1 durch Ventil
    m2, o = 2.0, (300, -440)  # r=330 -> y=220
    T = transform(o, m2)
    aussen, innen = schlauch_ringe()
    ring = [T(p) for p in aussen] + [T(p) for p in reversed(innen)]
    bl.ax.add_patch(Polygon([T(p) for p in aussen], closed=True, fc="none", ec="k", lw=LW_DICK,
                            hatch="xxxx", zorder=2))
    bl.ax.add_patch(Polygon([T(p) for p in innen], closed=True, fc="white", ec="k", lw=LW_DICK,
                            zorder=2))
    # Ventilschaft + Kappe
    def rechteck(z0, z1, r0, r1):
        return [T((z0, r0)), T((z1, r0)), T((z1, r1)), T((z0, r1))]
    bl.schraffur(rechteck(-4, 4, s["ventil_unten"], s["r_mitte"] - s["r_aussen"] + 0.4), "xxxx")
    bl.schraffur(rechteck(-5, 5, s["kappe_unten"], s["kappe_oben"]), "....")
    bl.mittellinie(T((0, 276)), T((0, 348)))
    bl.mittellinie(T((-18, 330)), T((18, 330)))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 2:1", h=4, bold=True)
    aussen_k, innen_k = schlauch_ringe(60)

    def ventil(x, cy, mm):
        for z0, z1, r0, r1 in ((-4, 4, s["ventil_unten"], 316.5), (-5, 5, s["kappe_unten"], s["kappe_oben"])):
            bl.ax.add_patch(Polygon([(x + z0 * mm, cy + r0 * mm), (x + z1 * mm, cy + r0 * mm),
                                     (x + z1 * mm, cy + r1 * mm), (x + z0 * mm, cy + r1 * mm)],
                                    closed=True, fc="white", ec="k", lw=LW_DUENN, zorder=4))
    schnitt_klein(bl, 190, c[1], m1, [(aussen_k, "xxxx"), (innen_k, None)],
                  [(14, 330)], detail_r=318, extra=ventil)
    bl.mass(T((-14, 330)), T((14, 330)), 34, "Ø28", "h")
    bl.radius(T((0, 330)), 13.1 * m2, 35, "Wand 0,9", aussen=22)
    bl.hinweis(T((4, 300)), (345, 165), "Ø8 (Gewinde 8V1)")
    bl.mass(T((-5, 280)), T((5, 280)), -8, "Ø10", "h")
    bl.mass(T((5, 280)), T((5, 316)), 22, "36", "v")
    bl.mass(T((5, 280)), T((5, 292)), 10, "12", "v")
    bl.hinweis(T((4, 305)), (345, 145), "Ventilschaft (Messing)")
    bl.hinweis(T((5, 286)), (345, 125), "Ventilkappe (Kunststoff)")
    bl.text(300, 92, "Schlauch im Einbauzustand (teilaufgepumpt) vereinfacht als Torus.", h=2.5)

    bl.text(232, 64, "Größe 28\" × 1 3/8 – 1 5/8 (ETRTO 32/47-622), Butyl (IIR).", h=2.5, ha="left")
    bl.text(232, 60, "Ventil AV 40 mm, max. 4,5 bar. Torus-Mitte R330.", h=2.5, ha="left")
    bl.schriftfeld("Schlauch 28\" AV 40 mm", "LR28-002", "Butylkautschuk IIR", "1:5 / 2:1",
                   "≈ 148 g")
    bl.speichern("LR28-002_Schlauch")


# ================================================================ Mantel ===
def zeichnung_mantel():
    bl = Blatt()
    m1, c = 0.2, (95, 160)
    vorderansicht(bl, c, m1, [348, 311], gestrichelt=[329.5])
    bl.durchmesser(c, 348 * m1, 35, "Ø696")
    bl.durchmesser(c, 311 * m1, -35, "Ø622 (Wulst)", aussen=24)
    schnittkennung(bl, c[0], c[1] + 74, c[1] - 74)
    bl.text(c[0], 274, "Vorderansicht  M 1:5", h=4, bold=True)

    m2, o = 2.5, (300, -620)  # r=311 -> y=157.5
    T = transform(o, m2)
    bl.schraffur([T(p) for p in mantel_kontur()], "\\\\\\\\")
    bl.mittellinie(T((0, 307)), T((0, 351)))
    bl.mittellinie(T((-21, 329.5)), T((21, 329.5)))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 2,5:1", h=4, bold=True)
    schnitt_klein(bl, 190, c[1], m1, [(mantel_kontur(20), "\\\\\\\\")],
                  [(18.5, 329.5), (9.5, 311), (5.5, 311)], detail_r=330)
    bl.mass(T((-18.5, 329.5)), T((18.5, 329.5)), 0, "", "h")
    bl.text(300 - 9 * m2, T((0, 329.5))[1] + 1, "37", va="bottom")
    bl.radius(T((0, 329.5)), 18.5 * m2, 40, "R18,5", aussen=14)
    bl.radius(T((0, 329.5)), 15.5 * m2, 125, "R15,5", aussen=30)
    bl.mass(T((-9.5, 311)), T((9.5, 311)), -12, "19", "h")
    bl.mass(T((-5.5, 311)), T((5.5, 311)), -22, "11", "h")
    bl.mass(T((-23, 311)), T((-23, 348)), -6, "37", "v")
    bl.mass(T((19, 311)), T((19, 329.5)), 12, "18,5", "v")
    bl.mass(T((9.5, 311)), T((9.5, 317)), 4, "6", "v")
    bl.mass(T((0, 345)), T((0, 348)), 0, "", "v")
    bl.hinweis(T((0, 346)), (345, 262), "Lauffläche 3")
    bl.hinweis(T((7.5, 312)), (345, 118), "Wulst mit Drahtkern")
    bl.hinweis(T((13, 319)), (340, 132), "passend zu LR28-001")
    bl.text(300, 92, "Lauffläche glatt vereinfacht (Profil optional als Rotationsschnitt).", h=2.5)

    bl.text(232, 64, "Größe 37-622 (28 × 1.40), Drahtreifen, 50 TPI, max. 4,5 bar.", h=2.5, ha="left")
    bl.text(232, 60, "Reflexstreifen und Profil nicht dargestellt.", h=2.5, ha="left")
    bl.schriftfeld("Mantel 37-622 (28×1.40)", "LR28-003", "NR/SBR, Nylonkarkasse",
                   "1:5 / 2,5:1", "≈ 716 g")
    bl.speichern("LR28-003_Mantel")


# ============================================================= Baugruppe ===
def zeichnung_baugruppe():
    bl = Blatt()
    m1, c = 0.2, (95, 160)
    vorderansicht(bl, c, m1, [348, 317, 303], gestrichelt=[311])
    for sx in (-0.8, 0.8):
        bl.linie([(c[0] + sx, c[1] + 303 * m1), (c[0] + sx, c[1] + 282 * m1)])
    bl.durchmesser(c, 348 * m1, 35, "Ø696")
    schnittkennung(bl, c[0], c[1] + 74, c[1] - 74)
    bl.text(c[0], 274, "Vorderansicht  M 1:5", h=4, bold=True)

    m2, o = 2.5, (300, -617.5)  # r=303 -> y=140
    T = transform(o, m2)
    bl.schraffur([T(p) for p in felge_kontur()], "////")
    bl.ax.add_patch(Polygon([T(p) for p in mantel_kontur()], closed=True, fc="none", ec="k",
                            lw=LW_DICK, hatch="\\\\\\\\", zorder=2))
    aussen, innen = schlauch_ringe()
    bl.ax.add_patch(Polygon([T(p) for p in aussen], closed=True, fc="none", ec="k",
                            lw=LW_DICK, hatch="xxxxx", zorder=2))
    bl.ax.add_patch(Polygon([T(p) for p in innen], closed=True, fc="white", ec="k",
                            lw=LW_DICK, zorder=2))
    bl.mittellinie(T((0, 299)), T((0, 351)))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 2,5:1", h=4, bold=True)
    a_k, i_k = schlauch_ringe(60)
    schnitt_klein(bl, 190, c[1], m1, [(mantel_kontur(20), "\\\\\\\\"), (felge_kontur(), "////"),
                                      (a_k, "xxxx"), (i_k, None)],
                  [(18.5, 329.5), (11.5, 309), (5.5, 303)], detail_r=325)
    bl.mass(T((-18.5, 330)), T((18.5, 330)), 0, "", "h")
    bl.text(300 - 9 * m2, T((0, 330))[1] + 1, "37", va="bottom")
    bl.mass(T((-24, 303)), T((-24, 348)), -4, "45", "v")
    # Positionsnummern
    for nr, ziel, pos in ((1, T((-10.5, 312)), (225, 150)), (2, T((10, 332)), (380, 205)),
                          (3, T((14, 342)), (380, 240))):
        bl.linie([ziel, pos], lw=LW_DUENN)
        bl.ax.add_patch(Circle(ziel, 0.6, color="k", zorder=5))
        bl.ax.add_patch(Circle(pos, 5, fc="white", ec="k", lw=LW_DUENN, zorder=5))
        bl.text(pos[0], pos[1], str(nr), h=4.5)

    # Stueckliste ueber dem Schriftfeld
    x0, y0 = 230, 70
    spalten = [(0, "Pos."), (12, "Menge"), (26, "Benennung"), (80, "Sachnummer"),
               (112, "Werkstoff"), (155, "Masse")]
    zeilen = [("3", "1", "Mantel 37-622", "LR28-003", "NR/SBR", "716 g"),
              ("2", "1", "Schlauch 28\" AV", "LR28-002", "Butyl IIR", "148 g"),
              ("1", "1", "Felge 622×19 36L", "LR28-001", "EN AW-6063", "465 g")]
    for i, z in enumerate(zeilen):
        y = y0 + i * 7
        for (dx, _), wert in zip(spalten, z):
            bl.text(x0 + dx + 1.5, y + 3.5, wert, h=2.5, ha="left")
        bl.linie([(x0, y + 7), (x0 + 180, y + 7)], lw=LW_DUENN)
    yk = y0 + len(zeilen) * 7
    for dx, t in spalten:
        bl.text(x0 + dx + 1.5, yk + 3.5, t, h=2.5, ha="left", bold=True)
        bl.linie([(x0 + dx, y0), (x0 + dx, yk + 7)], lw=LW_DUENN)
    bl.linie([(x0, yk + 7), (x0 + 180, yk + 7), (x0 + 180, y0)], lw=LW_DUENN)
    bl.linie([(x0, y0), (x0 + 180, y0)], lw=LW_DUENN)

    bl.schriftfeld("Laufrad 28\" (ohne Nabe/Speichen)", "LR28-000", "siehe Stückliste",
                   "1:5 / 2,5:1", "≈ 1,33 kg", zusatz="Reifendruck 3,5–4,5 bar")
    bl.speichern("LR28-000_Baugruppe")


if __name__ == "__main__":
    with PdfPages(AUS / "LR28_Zeichnungssatz.pdf") as SAMMEL:
        zeichnung_baugruppe()
        zeichnung_felge()
        zeichnung_schlauch()
        zeichnung_mantel()
