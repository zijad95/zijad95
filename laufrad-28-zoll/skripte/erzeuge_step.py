"""Erzeugt Felge, Schlauch, Mantel und die Baugruppe als STEP (AP214) mit CadQuery.

Aufruf:  python erzeuge_step.py            (benoetigt: pip install cadquery)
Ausgabe: ../cad_step/*.step
"""
import math
import pathlib

import cadquery as cq

from geometrie import (DICHTE, FELGE, MANTEL, MANTEL_PUNKTE_HALB, SCHLAUCH,
                       felge_kontur)

AUS = pathlib.Path(__file__).resolve().parent.parent / "cad_step"
AUS.mkdir(exist_ok=True)

# Workplane "ZY": lokales x = Modell-Z (axial), lokales y = Modell-Y (radial)
ACHSE = ((0, 0, 0), (1, 0, 0))  # lokale x-Achse = Radachse Z


def radial_zylinder(winkel_grad, d, r_von, r_bis):
    """Zylinder in radialer Richtung (Winkel in der XY-Ebene, 90 Grad = +Y)."""
    w = math.radians(winkel_grad)
    richtung = cq.Vector(math.cos(w), math.sin(w), 0)
    basis = richtung * r_von
    return cq.Solid.makeCylinder(d / 2, r_bis - r_von, basis, richtung)


def felge():
    k = felge_kontur()
    body = cq.Workplane("ZY").polyline(k).close().revolve(360, *ACHSE)
    solid = body.val()
    # Ventilloch bei +Y (90 Grad)
    solid = solid.cut(radial_zylinder(90, FELGE["ventilloch_d"], 295, 315))
    # 36 Speichenloecher, um 5 Grad zum Ventil versetzt
    n = FELGE["speichenloecher"]
    for i in range(n):
        solid = solid.cut(radial_zylinder(95 + i * 360 / n, FELGE["speichenloch_d"], 295, 310))
    return solid


def mantel():
    p = MANTEL_PUNKTE_HALB
    m = lambda pt: (-pt[0], pt[1])
    r_m = MANTEL["r_mitte"]
    w = (cq.Workplane("ZY")
         .moveTo(*p["T1"]).lineTo(*p["T2"]).lineTo(*p["T3"]).lineTo(*p["T4"])
         .lineTo(*p["T5"]).lineTo(*p["T6"]).lineTo(*p["T7"])
         .threePointArc((0, r_m + MANTEL["r_aussen"]), m(p["T7"]))
         .lineTo(*m(p["T6"])).lineTo(*m(p["T5"])).lineTo(*m(p["T4"]))
         .lineTo(*m(p["T3"])).lineTo(*m(p["T2"])).lineTo(*m(p["T1"]))
         .lineTo(*m(p["T9"])).lineTo(*m(p["T8"]))
         .threePointArc((0, r_m + MANTEL["r_innen"]), p["T8"])
         .lineTo(*p["T9"]).close())
    return w.revolve(360, *ACHSE).val()


def schlauch():
    s = SCHLAUCH
    aussen = cq.Workplane("ZY").center(0, s["r_mitte"]).circle(s["r_aussen"]).revolve(
        360, (0, -s["r_mitte"], 0), (1, -s["r_mitte"], 0))
    innen = cq.Workplane("ZY").center(0, s["r_mitte"]).circle(s["r_aussen"] - s["wand"]).revolve(
        360, (0, -s["r_mitte"], 0), (1, -s["r_mitte"], 0))
    solid = aussen.val().cut(innen.val())
    schaft = radial_zylinder(90, s["ventil_d"], s["ventil_unten"], s["ventil_oben"])
    kappe = radial_zylinder(90, s["kappe_d"], s["kappe_unten"], s["kappe_oben"])
    return solid.fuse(schaft).fuse(kappe).clean()


def main():
    teile = {"Felge": felge(), "Schlauch": schlauch(), "Mantel": mantel()}
    farben = {"Felge": cq.Color(0.75, 0.77, 0.80), "Schlauch": cq.Color(0.15, 0.15, 0.15),
              "Mantel": cq.Color(0.08, 0.08, 0.08)}
    for name, solid in teile.items():
        assert solid.isValid(), name
        cq.exporters.export(cq.Workplane().add(solid), str(AUS / f"{name}.step"))
        v = solid.Volume()
        bb = solid.BoundingBox()
        print(f"{name:9s} V={v / 1000:8.1f} cm3  m={v / 1000 * DICHTE[name]:6.0f} g  "
              f"D={bb.xlen:6.1f} mm  B={bb.zlen:5.1f} mm")

    asm = cq.Assembly(name="Laufrad_28_Zoll")
    for name, solid in teile.items():
        asm.add(solid, name=name, color=farben[name])
    asm.export(str(AUS / "Laufrad_Baugruppe.step"))

    # Kollisionspruefung
    namen = list(teile)
    for i in range(len(namen)):
        for j in range(i + 1, len(namen)):
            a, b = teile[namen[i]], teile[namen[j]]
            v = a.intersect(b).Volume()
            print(f"Kollision {namen[i]} / {namen[j]}: {v:.4f} mm3")


if __name__ == "__main__":
    main()
