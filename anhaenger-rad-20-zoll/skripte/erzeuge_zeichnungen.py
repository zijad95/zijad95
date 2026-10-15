"""Erzeugt bemasste Zeichnungen (DIN A3 quer) fuer Felge, Schlauch, Mantel und
Baugruppe des Anhaengerrads 20" - als PDF/PNG (Ansehen/Drucken) und als DXF
(bearbeitbar in SolidWorks, AutoCAD, DraftSight, LibreCAD ...).

Aufruf:  python erzeuge_zeichnungen.py      (benoetigt: matplotlib, ezdxf)
Ausgabe: ../zeichnungen/*.pdf, *.png, *.dxf
"""
import datetime
import json
import math
import pathlib

import ezdxf
import matplotlib
from ezdxf.enums import TextEntityAlignment

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Arc, Circle, PathPatch, Polygon
from matplotlib.path import Path

from geometrie import (FELGE, MANTEL, MANTEL_PUNKTE_HALB, NUMMER, RB, SCHLAUCH,
                       felge_kontur)

BASIS = pathlib.Path(__file__).resolve().parent.parent
AUS = BASIS / "zeichnungen"
AUS.mkdir(exist_ok=True)
try:
    MASSE = json.loads((BASIS / "cad_step" / "massen.json").read_text())
except FileNotFoundError:  # erst erzeuge_step.py ausfuehren
    MASSE = {"Felge": 0, "Schlauch": 0, "Mantel": 0, "Baugruppe": 0}

LW_DICK, LW_DUENN = 0.7, 0.35   # Linienbreiten in pt (ca. 0,5 / 0,25 mm)
TXT = 3.5                        # Schrifthoehe in mm
PT_PRO_MM = 72 / 25.4
DATUM = datetime.date.today().strftime("%d.%m.%Y")
SAMMEL = None                    # PdfPages fuer den gesamten Zeichnungssatz

MITTE = (0, (12, 3, 2, 3))       # Strichpunktlinie
VERDECKT = (0, (4, 2))           # Strichlinie

# Schraffuren: (matplotlib, DXF-Muster, DXF-Winkel, DXF-Skalierung)
H_ALU = ("////", "ANSI31", 0, 0.6)
H_GUMMI = ("\\\\\\\\", "ANSI31", 90, 0.6)
H_BUTYL = ("xxxx", "ANSI37", 0, 0.4)
H_KAPPE = ("....", "DOTS", 0, 0.5)


def f(x):
    """Zahl im deutschen Format (Komma, ohne unnoetige Nullen)."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def R(dr):
    """Radius relativ zum Wulstsitz (RB = 203)."""
    return RB + dr


def kleiner(h):
    """Schraffur fuer kleine Ansichten (1:5) enger setzen."""
    return (h[0], h[1], h[2], h[3] * 0.35)


class Blatt:
    """DIN-A3-Blatt; alle Koordinaten in Papier-mm, Ursprung unten links.
    Jede Zeichenoperation wird parallel in matplotlib und in ein DXF geschrieben."""

    def __init__(self):
        self.fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, 420)
        self.ax.set_ylim(0, 297)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.dxf = ezdxf.new("R2010", setup=True, units=4)  # 4 = Millimeter
        self.dxf.header["$LTSCALE"] = 1.0
        self.dxf.header["$MEASUREMENT"] = 1
        self.dxf.styles.add("ISO", font="arial.ttf")
        self.dxf.styles.add("ISO_FETT", font="arialbd.ttf")
        self.dxf.linetypes.add("MITTE_ISO", pattern=[20.0, 12.0, -3.0, 2.0, -3.0],
                               description="Strichpunkt __ . __")
        self.dxf.linetypes.add("VERDECKT_ISO", pattern=[6.0, 4.0, -2.0],
                               description="Strich __ __")
        for name, farbe, lw, lt in (("KONTUR", 7, 50, "Continuous"), ("DUENN", 7, 25, "Continuous"),
                                    ("MITTELLINIE", 1, 25, "MITTE_ISO"),
                                    ("VERDECKT", 3, 25, "VERDECKT_ISO"),
                                    ("MASSE", 4, 25, "Continuous"), ("TEXT", 7, 25, "Continuous"),
                                    ("SCHRAFFUR", 8, 18, "Continuous"), ("RAHMEN", 7, 70, "Continuous")):
            self.dxf.layers.add(name, color=farbe, lineweight=lw, linetype=lt)
        self.msp = self.dxf.modelspace()
        self.rahmen()

    # ---------------------------------------------------------- Grundlagen
    @staticmethod
    def _layer(lw, ls):
        if ls == "-":
            return "KONTUR" if lw >= LW_DICK else "DUENN"
        return "MITTELLINIE" if len(ls[1]) == 4 else "VERDECKT"

    def linie(self, pts, lw=LW_DICK, ls="-", layer=None):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color="k", lw=lw, ls=ls, solid_capstyle="butt", zorder=3)
        self.msp.add_lwpolyline(pts, dxfattribs={"layer": layer or self._layer(lw, ls)})

    def mittellinie(self, p1, p2):
        self.linie([p1, p2], lw=LW_DUENN, ls=MITTE)

    def text(self, x, y, s, h=TXT, ha="center", va="center", rot=0, bold=False):
        self.ax.text(x, y, s, fontsize=h * PT_PRO_MM / 0.72, ha=ha, va=va, rotation=rot,
                     fontweight="bold" if bold else "normal", family="DejaVu Sans",
                     rotation_mode="anchor", zorder=6)
        ausr = {"bottom": "BOTTOM", "center": "MIDDLE", "top": "TOP"}[va] + "_" + \
            {"left": "LEFT", "center": "CENTER", "right": "RIGHT"}[ha]
        t = self.msp.add_text(s.replace("≙", "="), height=h, rotation=rot,
                              dxfattribs={"layer": "TEXT", "style": "ISO_FETT" if bold else "ISO"})
        t.set_placement((x, y), align=TextEntityAlignment[ausr])

    def pfeil(self, spitze, richtung, laenge=3.0, breite=1.0):
        dx, dy = richtung
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        bx, by = spitze[0] - dx * laenge, spitze[1] - dy * laenge
        px, py = -dy * breite / 2, dx * breite / 2
        tri = [spitze, (bx + px, by + py), (bx - px, by - py)]
        self.ax.add_patch(Polygon(tri, closed=True, fc="k", ec="k", lw=0.2, zorder=5))
        self.msp.add_solid(tri, dxfattribs={"layer": "MASSE"})

    def punkt(self, p, r=0.6):
        self.ax.add_patch(Circle(p, r, color="k", zorder=5))
        h = self.msp.add_hatch(color=256, dxfattribs={"layer": "MASSE"})
        h.paths.add_edge_path().add_arc(p, r, 0, 360)

    def kreis(self, mitte, r, lw=LW_DICK, ls="-", weiss=False):
        self.ax.add_patch(Circle(mitte, r, fc="white" if weiss else "none", ec="k", lw=lw, ls=ls,
                                 zorder=5 if weiss else 3))
        self.msp.add_circle(mitte, r, dxfattribs={"layer": self._layer(lw, ls)})

    def bogen(self, mitte, r, a0, a1, lw=LW_DUENN):
        self.ax.add_patch(Arc(mitte, 2 * r, 2 * r, theta1=a0, theta2=a1, lw=lw, zorder=3))
        self.msp.add_arc(mitte, r, a0, a1, dxfattribs={"layer": self._layer(lw, "-")})

    def flaeche(self, aussen, loecher=(), hatch=H_ALU, lw=LW_DICK, weiss=False):
        """Geschlossene Flaeche (optional mit Loechern) mit Schraffur."""
        def flaeche_vz(ring):  # doppelte vorzeichenbehaftete Flaeche
            return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]))
        verts, codes = [], []
        for i, ring in enumerate([aussen, *loecher]):
            ring = list(ring)
            if (flaeche_vz(ring) > 0) == (i > 0):  # Loecher gegenlaeufig (Nonzero-Regel)
                ring = ring[::-1]
            verts += ring + [ring[0]]
            codes += [Path.MOVETO] + [Path.LINETO] * (len(ring) - 1) + [Path.CLOSEPOLY]
        self.ax.add_patch(PathPatch(Path(verts, codes), fc="white" if weiss else "none", ec="k",
                                    lw=lw, hatch=hatch[0] if hatch else None,
                                    zorder=4 if weiss else 2))
        lay = self._layer(lw, "-")
        for ring in [aussen, *loecher]:
            self.msp.add_lwpolyline(ring, close=True, dxfattribs={"layer": lay})
        if hatch:
            h = self.msp.add_hatch(dxfattribs={"layer": "SCHRAFFUR"})
            h.set_pattern_fill(hatch[1], angle=hatch[2], scale=hatch[3])
            for ring in [aussen, *loecher]:
                h.paths.add_polyline_path(ring, is_closed=True)

    # ------------------------------------------------------------ Masse
    def mass(self, p1, p2, abstand, txt, richtung="h", txt_pos=0.5):
        """Lineares Mass zwischen p1 und p2 (Papier-mm). richtung 'h' oder 'v'."""
        if richtung == "h":
            y = max(p1[1], p2[1]) + abstand if abstand > 0 else min(p1[1], p2[1]) + abstand
            a, b = (p1[0], y), (p2[0], y)
            for p in (p1, p2):
                if abs(y - p[1]) > 0.5:
                    s = 1 if y > p[1] else -1
                    self.linie([(p[0], p[1] + s * 1.0), (p[0], y + s * 2.0)], lw=LW_DUENN,
                               layer="MASSE")
        else:
            x = max(p1[0], p2[0]) + abstand if abstand > 0 else min(p1[0], p2[0]) + abstand
            a, b = (x, p1[1]), (x, p2[1])
            for p in (p1, p2):
                if abs(x - p[0]) > 0.5:
                    s = 1 if x > p[0] else -1
                    self.linie([(p[0] + s * 1.0, p[1]), (x + s * 2.0, p[1])], lw=LW_DUENN,
                               layer="MASSE")
        laenge = math.dist(a, b)
        d = ((b[0] - a[0]) / laenge, (b[1] - a[1]) / laenge)
        if laenge > 8:
            self.linie([a, b], lw=LW_DUENN, layer="MASSE")
            self.pfeil(a, (-d[0], -d[1]))
            self.pfeil(b, d)
        else:  # Pfeile von aussen
            self.linie([(a[0] - d[0] * 7, a[1] - d[1] * 7), (b[0] + d[0] * 7, b[1] + d[1] * 7)],
                       lw=LW_DUENN, layer="MASSE")
            self.pfeil(a, d)
            self.pfeil(b, (-d[0], -d[1]))
        if not txt:
            return
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
        self.linie([mitte, q], lw=LW_DUENN, layer="MASSE")
        self.pfeil(p, d)
        self.text(q[0] + (2 if d[0] >= 0 else -2), q[1], txt, ha="left" if d[0] >= 0 else "right")

    def durchmesser(self, mitte, r, winkel, txt, aussen=12):
        """Durchmessermass: Masslinie durch die Mitte, Text ausserhalb des Kreises."""
        w = math.radians(winkel)
        d = (math.cos(w), math.sin(w))
        p1 = (mitte[0] - d[0] * r, mitte[1] - d[1] * r)
        p2 = (mitte[0] + d[0] * r, mitte[1] + d[1] * r)
        q = (p2[0] + d[0] * aussen, p2[1] + d[1] * aussen)
        q2 = (q[0] + (14 if d[0] >= 0 else -14), q[1])
        self.linie([p1, q, q2], lw=LW_DUENN, layer="MASSE")
        self.pfeil(p1, (-d[0], -d[1]))
        self.pfeil(p2, d)
        self.text(q2[0], q2[1] + 1, txt, va="bottom", ha="right" if d[0] >= 0 else "left")

    def hinweis(self, ziel, text_pos, txt):
        self.linie([ziel, text_pos], lw=LW_DUENN, layer="MASSE")
        self.punkt(ziel)
        rechts = text_pos[0] >= ziel[0]
        self.text(text_pos[0] + (1 if rechts else -1), text_pos[1], txt,
                  ha="left" if rechts else "right")

    def positionsnummer(self, nr, ziel, pos):
        self.linie([ziel, pos], lw=LW_DUENN, layer="MASSE")
        self.punkt(ziel)
        self.kreis(pos, 5, lw=LW_DUENN, weiss=True)
        self.text(pos[0], pos[1], str(nr), h=4.5)

    # ------------------------------------------------------- Blattaufbau
    def rahmen(self):
        self.linie([(20, 10), (410, 10), (410, 287), (20, 287), (20, 10)], lw=1.0, layer="RAHMEN")
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
        self.linie([(x0, y0), (x0, y0 + h), (x0 + b, y0 + h)], lw=1.0, layer="RAHMEN")
        for y in (y0 + 10, y0 + 20, y0 + 30):
            self.linie([(x0, y), (x0 + b, y)], lw=LW_DUENN)
        for x in (x0 + 60, x0 + 120):
            self.linie([(x, y0 + 20), (x, y0 + 40)], lw=LW_DUENN)
        self.linie([(x0 + 140, y0), (x0 + 140, y0 + 20)], lw=LW_DUENN)

        def feld(x, y, titel, inhalt, bold=False, hh=TXT):
            self.text(x + 1.5, y + 8, titel, h=2.0, ha="left")
            self.text(x + 1.5, y + 3.5, inhalt, h=hh, ha="left", bold=bold)
        feld(x0, y0 + 30, "Werkstoff", werkstoff)
        feld(x0 + 60, y0 + 30, "Maßstab", massstab)
        feld(x0 + 120, y0 + 30, "Masse", masse)
        feld(x0, y0 + 20, "Gezeichnet", DATUM)
        feld(x0 + 60, y0 + 20, "Projektionsmethode", "1 (DIN ISO 128)")
        feld(x0 + 120, y0 + 20, "Format", "A3")
        feld(x0, y0 + 10, "Benennung", benennung, bold=True, hh=4.5)
        feld(x0, y0, "Zeichnungsnummer", nummer, bold=True)
        feld(x0 + 140, y0 + 10, "Blatt", blatt)
        feld(x0 + 140, y0, "Status", "Entwurf")
        self.text(x0 + 1.5, y0 + h + 3, zusatz, h=2.5, ha="left")
        # Projektionssymbol Methode 1
        x, y = x0 + 165, y0 + 25
        self.kreis((x - 4, y), 1.5, lw=LW_DUENN)
        self.kreis((x - 4, y), 3.0, lw=LW_DUENN)
        self.linie([(x + 1, y - 1.5), (x + 1, y + 1.5), (x + 7, y + 3), (x + 7, y - 3),
                    (x + 1, y - 1.5)], lw=LW_DUENN)

    def stueckliste(self, zeilen, x0=230, y0=70):
        spalten = [(0, "Pos."), (12, "Menge"), (26, "Benennung"), (80, "Sachnummer"),
                   (112, "Werkstoff"), (155, "Masse")]
        for i, z in enumerate(reversed(zeilen)):
            y = y0 + i * 7
            for (dx, _), wert in zip(spalten, z):
                self.text(x0 + dx + 1.5, y + 3.5, wert, h=2.5, ha="left")
            self.linie([(x0, y + 7), (x0 + 180, y + 7)], lw=LW_DUENN)
        yk = y0 + len(zeilen) * 7
        for dx, t in spalten:
            self.text(x0 + dx + 1.5, yk + 3.5, t, h=2.5, ha="left", bold=True)
            self.linie([(x0 + dx, y0), (x0 + dx, yk + 7)], lw=LW_DUENN)
        self.linie([(x0, yk + 7), (x0 + 180, yk + 7), (x0 + 180, y0), (x0, y0)], lw=LW_DUENN)

    def speichern(self, name):
        self.fig.savefig(AUS / f"{name}.pdf")
        self.fig.savefig(AUS / f"{name}.png", dpi=110)
        if SAMMEL is not None:
            SAMMEL.savefig(self.fig)
        plt.close(self.fig)
        self.dxf.saveas(AUS / f"{name}.dxf")
        print("geschrieben:", name)


# ------------------------------------------------------------------ Helfer
def transform(ursprung, massstab):
    """Modell (z, r) -> Papier (x, y)."""
    ox, oy = ursprung
    return lambda p: (ox + p[0] * massstab, oy + p[1] * massstab)


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
    pts += [m(p["T6"]), m(p["T5"]), m(p["T4"]), m(p["T3"]), m(p["T2"]), m(p["T1"]), m(p["T9"])]
    pts += list(reversed(bogen(ri, p["T8"], m(p["T8"]))))
    pts += [p["T9"]]
    return pts


def schlauch_ringe(n=90):
    s = SCHLAUCH

    def kreis(r):
        return [(r * math.cos(2 * math.pi * i / n), s["r_mitte"] + r * math.sin(2 * math.pi * i / n))
                for i in range(n)]
    return kreis(s["r_aussen"]), kreis(s["r_aussen"] - s["wand"])


def rechteck(z0, z1, r0, r1):
    return [(z0, r0), (z1, r0), (z1, r1), (z0, r1)]


def vorderansicht(bl, mitte, m, radien, gestrichelt=()):
    for r in radien:
        bl.kreis(mitte, r * m)
    for r in gestrichelt:
        bl.kreis(mitte, r * m, lw=LW_DUENN, ls=VERDECKT)
    gr = max(radien) * m + 5
    bl.mittellinie((mitte[0] - gr, mitte[1]), (mitte[0] + gr, mitte[1]))
    bl.mittellinie((mitte[0], mitte[1] - gr), (mitte[0], mitte[1] + gr))
    bl.text(mitte[0], 274, "Vorderansicht  M 1:5", h=4, bold=True)
    # Schnittverlauf A-A (senkrecht durch die Achse) mit Blickrichtungspfeilen
    for s in (1, -1):
        y = mitte[1] + s * (gr + 3)
        bl.linie([(mitte[0], y), (mitte[0], y + s * 6)], lw=1.2)
        bl.linie([(mitte[0], y + s * 6), (mitte[0] - 8, y + s * 6)], lw=LW_DUENN)
        bl.pfeil((mitte[0] - 8, y + s * 6), (-1, 0), laenge=3, breite=1.2)
        bl.text(mitte[0] - 12, y + s * 9, "A", h=5)


def schnitt_klein(bl, x, cy, m, flaechen, kanten, detail_r, extra=None):
    """Kleine Schnittansicht A-A (Schnitt durch die Radachse) im Massstab m.

    flaechen: Liste von (aussen, loecher, schraffur); kanten: (z, r) sichtbarer Kreiskanten,
    die im Schnitt als senkrechte Linien zwischen oberem und unterem Profil erscheinen."""
    for aussen, loecher, hatch in flaechen:
        for sgn in (1, -1):
            tr = lambda pts: [(x + z * m, cy + sgn * r * m) for z, r in pts]
            bl.flaeche(tr(aussen), [tr(lo) for lo in loecher], kleiner(hatch), lw=LW_DUENN)
    for z, r in kanten:
        for sz in (1, -1):
            bl.linie([(x + sz * z * m, cy - r * m), (x + sz * z * m, cy + r * m)], lw=LW_DUENN)
    if extra:
        extra(x, cy, m)
    rmax = max(r for aussen, _, _ in flaechen for _, r in aussen)
    bl.mittellinie((x - 12, cy), (x + 12, cy))
    bl.mittellinie((x, cy - rmax * m - 4), (x, cy + rmax * m + 4))
    bl.text(x, cy + rmax * m + 14, "Schnitt A–A  M 1:5", h=4, bold=True)
    yb = cy + detail_r * m
    bl.kreis((x, yb), 7, lw=LW_DUENN)
    bl.text(x + 9, yb + 6, "B", h=5)


# ================================================================ Felge ====
def zeichnung_felge():
    bl = Blatt()
    m1, c = 0.2, (95, 185)
    vorderansicht(bl, c, m1, [R(6), R(-8)], gestrichelt=[R(0)])
    for i in range(36):  # Speichenlochpositionen (radiale Bohrungen)
        w = math.radians(95 + i * 10)
        bl.linie([(c[0] + R(-10) * m1 * math.cos(w), c[1] + R(-10) * m1 * math.sin(w)),
                  (c[0] + R(10) * m1 * math.cos(w), c[1] + R(10) * m1 * math.sin(w))],
                 lw=LW_DUENN, ls=MITTE)
    bl.linie([(c[0], c[1] + R(-12) * m1), (c[0], c[1] + R(12) * m1)])
    bl.hinweis((c[0], c[1] + R(-6) * m1), (c[0] - 30, c[1] + 28), "Ventilloch Ø8,5")
    for a0, a1, t, rb, rt in ((90, 95, "5°", 32, 35.5), (95, 105, "10°", 22, 18)):  # Winkel innen
        for a in (a0, a1):
            w = math.radians(a)
            bl.linie([c, (c[0] + 36 * math.cos(w), c[1] + 36 * math.sin(w))], lw=LW_DUENN, ls=MITTE)
        bl.bogen(c, rb, a0, a1)
        w = math.radians((a0 + a1) / 2)
        bl.text(c[0] + rt * math.cos(w) - 2.5, c[1] + rt * math.sin(w), t, h=2.5, ha="right")
    bl.durchmesser(c, R(6) * m1, 35, "Ø418")
    bl.durchmesser(c, R(-8) * m1, -35, "Ø390", aussen=20)
    w = math.radians(-60)
    bl.hinweis((c[0] + R(0) * m1 * math.cos(w), c[1] + R(0) * m1 * math.sin(w)),
               (c[0] + 45, c[1] - 62), "Wulstsitz Ø406 (BSD)")
    bl.text(c[0], 108, "36× Ø4,5 radial, gleichmäßig verteilt,", h=2.5)
    bl.text(c[0], 104, "um 5° zum Ventilloch versetzt", h=2.5)

    schnitt_klein(bl, 180, c[1], m1, [(felge_kontur(), [], H_ALU)],
                  [(5.5, R(-8)), (7.0, R(-2)), (11.5, R(-2))], detail_r=R(-1))

    # --- Detail B 5:1
    m5 = 5.0
    T = transform((300, 150 - R(-8) * m5), m5)  # Felgenboden unten -> y = 150
    bl.flaeche([T(p) for p in felge_kontur()], hatch=H_ALU)
    bl.mittellinie(T((0, R(-11))), T((0, R(9.5))))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 5:1", h=4, bold=True)
    bl.mass(T((-11.5, R(6))), T((11.5, R(6))), 14, "23", "h")
    bl.mass(T((-9.5, R(4.5))), T((9.5, R(4.5))), 31, "19 (Maulweite)", "h")
    bl.mass(T((-4, R(-6))), T((4, R(-6))), -27, "8", "h")
    bl.mass(T((-5.5, R(-8))), T((5.5, R(-8))), -10, "11", "h")
    bl.mass(T((5.5, R(0))), T((9.5, R(0))), -8, "4", "h")
    bl.mass(T((11.5, R(-2))), T((11.5, R(6))), 10, "8", "v")
    bl.mass(T((9.5, R(0))), T((11.5, R(6))), 24, "6", "v")
    bl.mass(T((11.5, R(-8))), T((11.5, R(6))), 38, "14", "v")
    bl.mass(T((-4, R(-8))), T((-4, R(-6))), -42, "2", "v")
    bl.mass(T((-9.5, R(0))), T((-9.5, R(-6))), -26, "6 (Betttiefe)", "v")
    bl.hinweis(T((9.0, R(5.5))), (360, 262), "Hakenlippe 0,5×1")
    bl.hinweis(T((7.5, R(0))), (350, 128), "Wulstsitz Ø406")
    bl.hinweis(T((0, R(-7))), (245, 92), "Ø4,5 Speichen- / Ø8,5 Ventilloch")
    bl.text(300, 108, "Schnittfläche zeigt das Rotationsprofil;", h=2.5)
    bl.text(300, 104, "untere Hälfte symmetrisch.", h=2.5)

    # --- Detail C aus der Draufsicht (Blick von aussen auf das Ventilloch) 2:1
    m2, c2 = 2.0, (95, 42)
    r_m = R(-7)  # Mittelflaeche Felgenboden
    x5 = r_m * math.sin(math.radians(5)) * m2
    for zz, lw in ((-11.5, LW_DICK), (11.5, LW_DICK), (-5.5, LW_DUENN), (5.5, LW_DUENN)):
        bl.linie([(c2[0] - 60, c2[1] + zz * m2), (c2[0] + 60, c2[1] + zz * m2)], lw=lw)
    bl.kreis(c2, 4.25 * m2)
    for s in (-1, 1):
        bl.kreis((c2[0] + s * x5, c2[1]), 2.25 * m2)
        bl.mittellinie((c2[0] + s * x5, c2[1] - 7), (c2[0] + s * x5, c2[1] + 7))
    bl.mittellinie((c2[0] - 62, c2[1]), (c2[0] + 62, c2[1]))
    bl.mittellinie((c2[0], c2[1] - 12), (c2[0], c2[1] + 12))
    bl.mass((c2[0] - x5, c2[1] + 2.25 * m2), (c2[0] + x5, c2[1] + 2.25 * m2), 22,
            f"2× {f(round(r_m * math.sin(math.radians(5)), 1))} (≙ 5°)", "h")
    bl.hinweis((c2[0] + 4.25 * m2 * 0.7, c2[1] - 4.25 * m2 * 0.7), (c2[0] + 40, c2[1] - 25), "Ø8,5")
    bl.hinweis((c2[0] + x5 + 1.6 * m2, c2[1] - 1.6 * m2), (c2[0] + 68, c2[1] - 18), "Ø4,5")
    bl.text(c2[0], c2[1] + 38, "Detail C (aus Draufsicht)  M 2:1", h=4, bold=True)

    bl.text(232, 64, "Material: EN AW-6063 T6, eloxiert (silber). Stoß gepinnt.", h=2.5, ha="left")
    bl.text(232, 60, "Nicht bemaßte Radien R0,5. Ventilloch und Speichenlöcher entgratet.", h=2.5,
            ha="left")
    bl.schriftfeld("Felge 406×19, 36 Loch, AV", NUMMER["Felge"], "EN AW-6063 T6",
                   "1:5 / 5:1 / 2:1", f"≈ {MASSE['Felge']} g")
    bl.speichern(f"{NUMMER['Felge']}_Felge")


# ============================================================== Schlauch ===
def zeichnung_schlauch():
    bl = Blatt()
    s = SCHLAUCH
    ra, ri = s["r_mitte"] + s["r_aussen"], s["r_mitte"] - s["r_aussen"]
    m1, c = 0.2, (95, 175)
    vorderansicht(bl, c, m1, [ra, ri], gestrichelt=[s["r_mitte"]])
    for sx in (-0.8, 0.8):
        bl.linie([(c[0] + sx, c[1] + ri * m1), (c[0] + sx, c[1] + s["kappe_unten"] * m1)])
    bl.durchmesser(c, ra * m1, 35, f"Ø{f(2 * ra)}")
    bl.durchmesser(c, ri * m1, -35, f"Ø{f(2 * ri)}", aussen=20)
    bl.hinweis((c[0], c[1] + R(-20) * m1), (c[0] + 32, c[1] + 62), "Ventil AV bei 12 Uhr")

    def ventil_klein(x, cy, mm):
        for z0, z1, r0, r1 in ((-4, 4, s["ventil_unten"], ri), (-5, 5, s["kappe_unten"], s["kappe_oben"])):
            bl.flaeche([(x + z * mm, cy + r * mm) for z, r in rechteck(z0, z1, r0, r1)],
                       hatch=None, lw=LW_DUENN, weiss=True)
    a_k, i_k = schlauch_ringe(60)
    schnitt_klein(bl, 180, c[1], m1, [(a_k, [i_k], H_BUTYL)], [(s["r_aussen"], s["r_mitte"])],
                  detail_r=ri, extra=ventil_klein)

    # --- Detail B 2:1 durch das Ventil
    m2 = 2.0
    T = transform((300, 105 - s["kappe_unten"] * m2), m2)   # Kappe unten -> y = 105
    aussen, innen = schlauch_ringe()
    bl.flaeche([T(p) for p in aussen], [[T(p) for p in innen]], H_BUTYL)
    bl.flaeche([T(p) for p in rechteck(-4, 4, s["ventil_unten"], ri + 0.3)], hatch=H_BUTYL)
    bl.flaeche([T(p) for p in rechteck(-5, 5, s["kappe_unten"], s["kappe_oben"])], hatch=H_KAPPE)
    bl.mittellinie(T((0, s["kappe_unten"] - 4)), T((0, ra + 4)))
    bl.mittellinie(T((-s["r_aussen"] - 4, s["r_mitte"])), T((s["r_aussen"] + 4, s["r_mitte"])))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 2:1", h=4, bold=True)
    bl.mass(T((-s["r_aussen"], s["r_mitte"])), T((s["r_aussen"], s["r_mitte"])),
            s["r_aussen"] * m2 + 8, f"Ø{f(2 * s['r_aussen'])}", "h")
    bl.radius(T((0, s["r_mitte"])), (s["r_aussen"] - s["wand"]) * m2, 35, f"Wand {f(s['wand'])}",
              aussen=22)
    bl.hinweis(T((4, s["kappe_oben"] + 6)), (345, 150), "Ø8 (Gewinde 8V1)")
    bl.mass(T((-5, s["kappe_unten"])), T((5, s["kappe_unten"])), -8, "Ø10", "h")
    bl.mass(T((5, s["kappe_unten"])), T((5, ri)), 22, f(ri - s["kappe_unten"]), "v")
    bl.mass(T((5, s["kappe_unten"])), T((5, s["kappe_oben"])), 10, "12", "v")
    bl.hinweis(T((-4, s["kappe_oben"] + 12)), (250, 165), "Ventilschaft (Messing)")
    bl.hinweis(T((-5, s["kappe_unten"] + 5)), (250, 120), "Ventilkappe (Kunststoff)")
    bl.text(300, 92, "Schlauch im Einbauzustand (teilaufgepumpt) vereinfacht als Torus.", h=2.5)

    bl.text(232, 64, "Größe 20 × 1.75–2.125 (ETRTO 47/57-406), Butyl (IIR).", h=2.5, ha="left")
    bl.text(232, 60, f"Ventil AV 35 mm, max. 3,5 bar. Torus-Mitte R{f(s['r_mitte'])}.", h=2.5,
            ha="left")
    bl.schriftfeld("Schlauch 20\" AV 35 mm", NUMMER["Schlauch"], "Butylkautschuk IIR", "1:5 / 2:1",
                   f"≈ {MASSE['Schlauch']} g")
    bl.speichern(f"{NUMMER['Schlauch']}_Schlauch")


# ================================================================ Mantel ===
def zeichnung_mantel():
    bl = Blatt()
    M = MANTEL
    rm, ra, ri = M["r_mitte"], M["r_aussen"], M["r_innen"]
    m1, c = 0.2, (95, 175)
    vorderansicht(bl, c, m1, [rm + ra, RB], gestrichelt=[rm])
    bl.durchmesser(c, (rm + ra) * m1, 35, "Ø500")
    bl.durchmesser(c, RB * m1, -35, "Ø406 (Wulst)", aussen=24)
    schnitt_klein(bl, 180, c[1], m1, [(mantel_kontur(20), [], H_GUMMI)],
                  [(ra, rm), (9.5, RB), (5.5, RB)], detail_r=rm)

    m2 = 2.0
    T = transform((300, 145 - RB * m2), m2)  # Wulst -> y = 145
    bl.flaeche([T(p) for p in mantel_kontur()], hatch=H_GUMMI)
    bl.mittellinie(T((0, RB - 4)), T((0, rm + ra + 3)))
    bl.mittellinie(T((-ra - 3, rm)), T((ra + 3, rm)))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 2:1", h=4, bold=True)
    bl.mass(T((-ra, rm)), T((ra, rm)), ra * m2 + 10, "47", "h")
    bl.radius(T((0, rm)), ra * m2, 40, f"R{f(ra)}", aussen=14)
    bl.radius(T((0, rm)), ri * m2, 145, f"R{f(ri)}", aussen=25)
    bl.mass(T((-9.5, RB)), T((9.5, RB)), -12, "19", "h")
    bl.mass(T((-5.5, RB)), T((5.5, RB)), -22, "11", "h")
    bl.mass(T((-ra - 4, RB)), T((-ra - 4, rm + ra)), -6, "47", "v")
    bl.mass(T((ra + 1, RB)), T((ra + 1, rm)), 12, f(rm - RB), "v")
    bl.mass(T((9.5, RB)), T((9.5, R(6))), 4, "6", "v")
    bl.mass(T((0, rm + ri)), T((0, rm + ra)), 0, "", "v")
    bl.hinweis(T((0, rm + ri + 1.5)), (345, 262), "Lauffläche 3")
    bl.hinweis(T((7.5, R(1))), (345, 112), "Wulst mit Drahtkern")
    bl.hinweis(T((13, R(6.8))), (345, 126), f"passend zu {NUMMER['Felge']}")
    bl.text(300, 92, "Lauffläche glatt vereinfacht (Profil optional als Rotationsschnitt).", h=2.5)

    bl.text(232, 64, "Größe 47-406 (20 × 1.75), Drahtreifen, 30 TPI, max. 3,5 bar (50 psi).",
            h=2.5, ha="left")
    bl.text(232, 60, "Reflexstreifen und Profil nicht dargestellt.", h=2.5, ha="left")
    bl.schriftfeld("Mantel 47-406 (20×1.75)", NUMMER["Mantel"], "NR/SBR, Nylonkarkasse",
                   "1:5 / 2:1", f"≈ {MASSE['Mantel']} g")
    bl.speichern(f"{NUMMER['Mantel']}_Mantel")


# ============================================================= Baugruppe ===
def zeichnung_baugruppe():
    bl = Blatt()
    M, S = MANTEL, SCHLAUCH
    rm, ra = M["r_mitte"], M["r_aussen"]
    m1, c = 0.2, (95, 175)
    vorderansicht(bl, c, m1, [rm + ra, R(6), R(-8)], gestrichelt=[RB])
    for sx in (-0.8, 0.8):
        bl.linie([(c[0] + sx, c[1] + R(-8) * m1), (c[0] + sx, c[1] + S["kappe_unten"] * m1)])
    bl.durchmesser(c, (rm + ra) * m1, 35, "Ø500")

    a_k, i_k = schlauch_ringe(60)
    schnitt_klein(bl, 180, c[1], m1, [(mantel_kontur(20), [], H_GUMMI),
                                      (felge_kontur(), [], H_ALU), (a_k, [i_k], H_BUTYL)],
                  [(ra, rm), (11.5, R(-2)), (5.5, R(-8))], detail_r=rm - 4)

    m2 = 2.0
    T = transform((300, 140 - R(-8) * m2), m2)  # Felgenboden -> y = 140
    bl.flaeche([T(p) for p in felge_kontur()], hatch=H_ALU)
    bl.flaeche([T(p) for p in mantel_kontur()], hatch=H_GUMMI)
    aussen, innen = schlauch_ringe()
    bl.flaeche([T(p) for p in aussen], [[T(p) for p in innen]], H_BUTYL)
    bl.mittellinie(T((0, R(-11))), T((0, rm + ra + 3)))
    bl.text(300, 274, "Detail B (aus Schnitt A–A)  M 2:1", h=4, bold=True)
    bl.mass(T((-ra, rm)), T((ra, rm)), ra * m2 + 10, "47", "h")
    bl.mass(T((-ra - 5, R(-8))), T((-ra - 5, rm + ra)), -4, f(rm + ra - R(-8)), "v")
    for nr, ziel, pos in ((1, T((-10.5, R(1))), (230, 130)), (2, T((12, S["r_mitte"])), (380, 205)),
                          (3, T((17, rm + 17)), (380, 240))):
        bl.positionsnummer(nr, ziel, pos)

    bl.stueckliste([
        ("1", "1", "Felge 406×19 36L", NUMMER["Felge"], "EN AW-6063", f"{MASSE['Felge']} g"),
        ("2", "1", "Schlauch 20\" AV", NUMMER["Schlauch"], "Butyl IIR", f"{MASSE['Schlauch']} g"),
        ("3", "1", "Mantel 47-406", NUMMER["Mantel"], "NR/SBR", f"{MASSE['Mantel']} g")])
    bl.schriftfeld("Anhängerrad 20\" (o. Nabe)", NUMMER["Baugruppe"],
                   "siehe Stückliste", "1:5 / 2:1",
                   f"≈ {f(MASSE['Baugruppe'] / 1000)} kg", zusatz="Reifendruck 2,5–3,5 bar")
    bl.speichern(f"{NUMMER['Baugruppe']}_Baugruppe")


if __name__ == "__main__":
    with PdfPages(AUS / "AR20_Zeichnungssatz.pdf") as SAMMEL:
        zeichnung_baugruppe()
        zeichnung_felge()
        zeichnung_schlauch()
        zeichnung_mantel()
