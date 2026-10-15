Attribute VB_Name = "Anhaengerrad20"
'==============================================================================
' SolidWorks-Makro: Fahrradanhaenger-Rad 20" (ETRTO 406) - kostenguenstig
'
'   AR20-001  Felge 406x19, einwandig, Aluminium, 36 Loch, Ventilloch AV
'   AR20-002  Schlauch 20 x 1.75-2.125 Butyl mit AV-Ventil 35 mm
'   AR20-003  Mantel (Drahtreifen) 47-406 / 20 x 1.75
'   AR20-000  Baugruppe Anhaengerrad (ohne Nabe/Speichen)
'   + je eine Zeichnung (Vorderansicht 1:5, Isometrie) als Startpunkt
'
' Anwendung:
'   1. SolidWorks starten, Extras > Makro > Neu... > z.B. "Anhaengerrad20.swp" speichern
'   2. Im VBA-Editor: Datei > Datei importieren... > diese Datei (Anhaengerrad20.bas)
'   3. Das automatisch angelegte leere Modul "Module1" darf geloescht werden
'   4. Makro ausfuehren (F5) -> Sub "main"
'   Ergebnis liegt im Unterordner "Anhaengerrad20" neben der .swp-Datei.
'
' Koordinaten: Radachse = Z-Achse, Ventil bei +Y (12 Uhr). Masse in mm.
' Das Makro verwendet nur spaetes Binden (Object) und Zahlenkonstanten, damit
' keine zusaetzlichen Verweise noetig sind und es sprachunabhaengig laeuft
' (Ebenen werden ueber ihre Reihenfolge im FeatureManager gefunden).
'==============================================================================
Option Explicit

Private Const MM As Double = 0.001
Private Const PI As Double = 3.14159265358979

Private swApp As Object
Private gOrdner As String
Private gProtokoll As String

'------------------------------------------------------------------------------
Sub main()
    Set swApp = Application.SldWorks
    gOrdner = swApp.GetCurrentMacroPathFolder & "\Anhaengerrad20\"
    If Dir(gOrdner, vbDirectory) = "" Then MkDir gOrdner
    gProtokoll = ""

    Dim pFelge As String, pSchlauch As String, pMantel As String, pBg As String
    pFelge = ErzeugeFelge()
    pSchlauch = ErzeugeSchlauch()
    pMantel = ErzeugeMantel()
    If pFelge = "" Or pSchlauch = "" Or pMantel = "" Then
        MsgBox "Abbruch - mindestens ein Teil konnte nicht erzeugt werden." & vbCrLf & gProtokoll, vbCritical
        Exit Sub
    End If

    pBg = ErzeugeBaugruppe(pFelge, pSchlauch, pMantel)

    ErzeugeZeichnung pFelge, "AR20-001_Felge"
    ErzeugeZeichnung pSchlauch, "AR20-002_Schlauch"
    ErzeugeZeichnung pMantel, "AR20-003_Mantel"
    If pBg <> "" Then ErzeugeZeichnung pBg, "AR20-000_Anhaengerrad"

    MsgBox "Fertig. Dateien in:" & vbCrLf & gOrdner & vbCrLf & vbCrLf & _
           "Hinweise:" & vbCrLf & IIf(gProtokoll = "", "(keine)", gProtokoll), vbInformation
End Sub

'==============================================================================
' TEIL 1: FELGE  (AR20-001)
'==============================================================================
Private Function ErzeugeFelge() As String
    Dim doc As Object, sk As Object, koerper As Object, loch As Object
    Dim achse As Object, muster As Object, i As Long

    Set doc = NeuesDokument(8)
    If doc Is Nothing Then Exit Function

    ' --- Profil (rechte Haelfte z>=0, wird gespiegelt): Paare (z, r) in mm
    Dim h As Variant
    h = Array(0, 197, 4, 197, 5.5, 203, 9.5, 203, 9.5, 207.5, 9, 208, 9, 209, _
              11.5, 209, 11.5, 201, 7, 201, 5.5, 195, 0, 195)
    Dim p() As Double
    p = Spiegeln(h)

    SkizzeStarten doc, 3                         ' Ebene rechts
    Mittellinie doc, -20, 0, 20, 0               ' Radachse (Modell-Z)
    Polygonzug doc, p
    Set sk = SkizzeBeenden(doc, "Skizze_Felgenprofil")
    Set koerper = Rotation(doc, sk, False)
    If koerper Is Nothing Then Fehler "Felge: Rotation des Profils fehlgeschlagen": Exit Function
    koerper.Name = "Felgenkoerper"

    ' --- Ventilloch D8,5 bei 90 Grad (+Y)
    If RadialeBohrung(doc, 90, 8.5, 187, 204, "Ventilloch") Is Nothing Then _
        Fehler "Felge: Ventilloch fehlgeschlagen"

    ' --- Erstes Speichenloch D4,5 bei 95 Grad (5 Grad neben dem Ventil)
    Set loch = RadialeBohrung(doc, 95, 4.5, 187, 204, "Speichenloch")
    If loch Is Nothing Then Fehler "Felge: Speichenloch fehlgeschlagen": GoTo Abschluss

    ' --- Referenzachse = Schnitt Ebene oben / Ebene rechts (= Radachse Z)
    doc.ClearSelection2 True
    Ebene(doc, 2).Select2 False, 0
    Ebene(doc, 3).Select2 True, 0
    doc.InsertAxis2 True
    Set achse = doc.FeatureByPositionReverse(0)
    achse.Name = "Radachse"

    ' --- Kreismuster 36x gleichmaessig ueber 360 Grad
    On Error Resume Next
    doc.ClearSelection2 True
    loch.Select2 False, 4
    achse.Select2 True, 1
    Set muster = doc.FeatureManager.FeatureCircularPattern5(36, 2 * PI, False, "NULL", False, True, _
                 False, False, False, False, 1, 0, "NULL", False)
    If muster Is Nothing Then
        Err.Clear
        doc.ClearSelection2 True
        loch.Select2 False, 4
        achse.Select2 True, 1
        Set muster = doc.FeatureManager.FeatureCircularPattern4(36, 2 * PI, False, "NULL", False, True, False)
    End If
    On Error GoTo 0
    If muster Is Nothing Then
        ' Rueckfallebene: 35 weitere einzelne rotierte Schnitte
        For i = 1 To 35
            RadialeBohrung doc, 95 + 10 * i, 4.5, 187, 204, "Speichenloch" & (i + 1)
        Next i
        Fehler "Felge: Kreismuster per API nicht moeglich - Loecher einzeln erzeugt"
    Else
        muster.Name = "Speichenloecher_36x"
    End If

Abschluss:
    Material doc, "6063-T6"
    Eigenschaften doc, "Felge 406x19, 36 Loch, AV", "AR20-001", "EN AW-6063 T6"
    ErzeugeFelge = Speichern(doc, "AR20-001_Felge.SLDPRT")
End Function

'==============================================================================
' TEIL 2: SCHLAUCH  (AR20-002)
'==============================================================================
Private Function ErzeugeSchlauch() As String
    Dim doc As Object, sk As Object, f As Object

    Set doc = NeuesDokument(8)
    If doc Is Nothing Then Exit Function

    ' --- Schlauchkoerper: Kreisring D36,6 / Wand 1,0 um Radachse rotiert (Torus)
    SkizzeStarten doc, 3
    Mittellinie doc, -25, 0, 25, 0
    doc.SketchManager.CreateCircleByRadius 0, 228.5 * MM, 0, 18.3 * MM
    doc.SketchManager.CreateCircleByRadius 0, 228.5 * MM, 0, 17.3 * MM
    Set sk = SkizzeBeenden(doc, "Skizze_Schlauchquerschnitt")
    Set f = Rotation(doc, sk, False)
    If f Is Nothing Then Fehler "Schlauch: Rotation fehlgeschlagen": Exit Function
    f.Name = "Schlauchkoerper"

    ' --- AV-Ventil (Schaft D8, Kappe D10) auf Ebene vorne um die Y-Achse rotiert
    Dim v As Variant, p() As Double
    v = Array(0, 174, 5, 174, 5, 186, 4, 186, 4, 210.7, 0, 210.7)
    p = Punkte(v)
    SkizzeStarten doc, 1
    Mittellinie doc, 0, 165, 0, 220
    Polygonzug doc, p
    Set sk = SkizzeBeenden(doc, "Skizze_Ventil")
    Set f = Rotation(doc, sk, False)
    If f Is Nothing Then Fehler "Schlauch: Ventil fehlgeschlagen" Else f.Name = "Ventil_AV"

    Eigenschaften doc, "Schlauch 20"" AV 35 mm", "AR20-002", "Butylkautschuk IIR"
    ErzeugeSchlauch = Speichern(doc, "AR20-002_Schlauch.SLDPRT")
End Function

'==============================================================================
' TEIL 3: MANTEL  (AR20-003)
'==============================================================================
Private Function ErzeugeMantel() As String
    Dim doc As Object, sk As Object, f As Object
    Dim za As Double, zi As Double, sm As Object

    Set doc = NeuesDokument(8)
    If doc Is Nothing Then Exit Function

    za = Sqr(23.5 ^ 2 - (226.5 - 210.5) ^ 2)     ' 17,212 (Aussenbogen R23,5 bei r=210,5)
    zi = Sqr(20.5 ^ 2 - (226.5 - 213) ^ 2)       ' 15,427 (Innenbogen R20,5 bei r=213)

    SkizzeStarten doc, 3
    Set sm = doc.SketchManager
    Mittellinie doc, -30, 0, 30, 0
    ' rechte Wulst + Flanke
    Linie doc, 5.5, 203, 9.5, 203
    Linie doc, 9.5, 203, 9.5, 207.5
    Linie doc, 9.5, 207.5, 9, 208
    Linie doc, 9, 208, 9, 209
    Linie doc, 9, 209, 11.5, 209
    Linie doc, 11.5, 209, za, 210.5
    ' Aussenbogen R23,5 ueber die Laufflaeche (gegen Uhrzeigersinn)
    sm.CreateArc 0, 226.5 * MM, 0, za * MM, 210.5 * MM, 0, -za * MM, 210.5 * MM, 0, 1
    ' linke Flanke + Wulst
    Linie doc, -za, 210.5, -11.5, 209
    Linie doc, -11.5, 209, -9, 209
    Linie doc, -9, 209, -9, 208
    Linie doc, -9, 208, -9.5, 207.5
    Linie doc, -9.5, 207.5, -9.5, 203
    Linie doc, -9.5, 203, -5.5, 203
    Linie doc, -5.5, 203, -5.5, 210
    Linie doc, -5.5, 210, -zi, 213
    ' Innenbogen R20,5 (von rechts nach links gegen Uhrzeigersinn)
    sm.CreateArc 0, 226.5 * MM, 0, zi * MM, 213 * MM, 0, -zi * MM, 213 * MM, 0, 1
    Linie doc, zi, 213, 5.5, 210
    Linie doc, 5.5, 210, 5.5, 203
    Set sk = SkizzeBeenden(doc, "Skizze_Mantelquerschnitt")
    Set f = Rotation(doc, sk, False)
    If f Is Nothing Then Fehler "Mantel: Rotation fehlgeschlagen": Exit Function
    f.Name = "Mantelkoerper"

    Eigenschaften doc, "Mantel 47-406 (20x1.75)", "AR20-003", "NR/SBR, Nylonkarkasse"
    ErzeugeMantel = Speichern(doc, "AR20-003_Mantel.SLDPRT")
End Function

'==============================================================================
' BAUGRUPPE  (AR20-000)
'==============================================================================
Private Function ErzeugeBaugruppe(ByVal pF As String, ByVal pS As String, ByVal pM As String) As String
    Dim asm As Object, cF As Object, cS As Object, cM As Object

    Set asm = NeuesDokument(9)
    If asm Is Nothing Then Exit Function

    Set cF = asm.AddComponent5(pF, 0, "", False, "", 0, 0, 0)
    Set cS = asm.AddComponent5(pS, 0, "", False, "", 0, 0, 0)
    Set cM = asm.AddComponent5(pM, 0, "", False, "", 0, 0, 0)
    If cF Is Nothing Or cS Is Nothing Or cM Is Nothing Then
        Fehler "Baugruppe: Komponenten konnten nicht eingefuegt werden"
        Exit Function
    End If

    ' Felge fixieren, Schlauch + Mantel ueber die drei Hauptebenen ausrichten
    asm.ClearSelection2 True
    cF.Select4 False, Nothing, False
    asm.FixComponent

    Dim comp As Variant, i As Integer
    For Each comp In Array(cS, cM)
        For i = 1 To 3
            If Not EbenenDeckungsgleich(asm, cF, comp, i) Then
                asm.ClearSelection2 True
                comp.Select4 False, Nothing, False
                asm.FixComponent
                Fehler "Baugruppe: Verknuepfung nicht moeglich - " & comp.Name2 & " fixiert"
                Exit For
            End If
        Next i
    Next comp

    asm.EditRebuild3
    Eigenschaften asm, "Anhaengerrad 20"" (ohne Nabe/Speichen)", "AR20-000", "siehe Stueckliste"
    ErzeugeBaugruppe = Speichern(asm, "AR20-000_Anhaengerrad.SLDASM")
End Function

Private Function EbenenDeckungsgleich(asm As Object, a As Object, b As Variant, ByVal nr As Integer) As Boolean
    Dim ea As Object, eb As Object, mate As Object, fehlerCode As Long
    Set ea = KompEbene(a, nr)
    Set eb = KompEbene(b, nr)
    If ea Is Nothing Or eb Is Nothing Then Exit Function
    asm.ClearSelection2 True
    ea.Select2 False, 1
    eb.Select2 True, 1
    ' 0 = deckungsgleich, 2 = naechstgelegene Ausrichtung
    Set mate = asm.AddMate5(0, 2, False, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, fehlerCode)
    asm.ClearSelection2 True
    EbenenDeckungsgleich = Not (mate Is Nothing)
End Function

'==============================================================================
' ZEICHNUNGEN (Grundgeruest: Vorderansicht 1:5 + Isometrie 1:10)
' Schnitt A-A, Detail B, Bemassung und Stueckliste -> siehe ANLEITUNG.md
'==============================================================================
Private Sub ErzeugeZeichnung(ByVal modellPfad As String, ByVal name As String)
    Dim dw As Object, vV As Object, vI As Object
    Set dw = NeuesDokument(10)
    If dw Is Nothing Then Exit Sub

    Set vV = Modellansicht(dw, modellPfad, Array("*Front", "*Vorderansicht", "*Vorne"), 0.1, 0.165)
    If vV Is Nothing Then
        Fehler "Zeichnung " & name & ": Vorderansicht nicht erzeugt"
    Else
        vV.UseSheetScale = False
        vV.ScaleDecimal = 0.2
    End If

    Set vI = Modellansicht(dw, modellPfad, Array("*Isometric", "*Isometrisch"), 0.36, 0.225)
    If Not vI Is Nothing Then
        vI.UseSheetScale = False
        vI.ScaleDecimal = 0.1
    End If

    dw.ForceRebuild3 True
    Speichern dw, name & ".SLDDRW"
End Sub

Private Function Modellansicht(dw As Object, ByVal pfad As String, namen As Variant, _
                               ByVal x As Double, ByVal y As Double) As Object
    Dim n As Variant, v As Object
    On Error Resume Next
    For Each n In namen
        Set v = dw.CreateDrawViewFromModelView3(pfad, CStr(n), x, y, 0)
        If Not v Is Nothing Then Exit For
    Next n
    On Error GoTo 0
    Set Modellansicht = v
End Function

'==============================================================================
' HILFSFUNKTIONEN
'==============================================================================
' art: 8 = Teil, 9 = Baugruppe, 10 = Zeichnung (swUserPreferenceStringValue_e)
Private Function NeuesDokument(ByVal art As Long) As Object
    Dim vorlage As String
    vorlage = swApp.GetUserPreferenceStringValue(art)
    If vorlage = "" Then
        Fehler "Keine Standardvorlage (Extras > Optionen > Standardvorlagen)"
        Exit Function
    End If
    If art = 10 Then
        Set NeuesDokument = swApp.NewDocument(vorlage, 8, 0.42, 0.297)   ' 8 = A3
    Else
        Set NeuesDokument = swApp.NewDocument(vorlage, 0, 0, 0)
    End If
End Function

' nr: 1 = Ebene vorne, 2 = Ebene oben, 3 = Ebene rechts
Private Function Ebene(doc As Object, ByVal nr As Integer) As Object
    Dim f As Object, n As Integer
    Set f = doc.FirstFeature
    Do While Not f Is Nothing
        If f.GetTypeName2 = "RefPlane" Then
            n = n + 1
            If n = nr Then
                Set Ebene = f
                Exit Function
            End If
        End If
        Set f = f.GetNextFeature
    Loop
End Function

Private Function KompEbene(ByVal comp As Object, ByVal nr As Integer) As Object
    Dim f As Object, n As Integer
    Set f = comp.FirstFeature
    Do While Not f Is Nothing
        If f.GetTypeName2 = "RefPlane" Then
            n = n + 1
            If n = nr Then
                Set KompEbene = f
                Exit Function
            End If
        End If
        Set f = f.GetNextFeature
    Loop
End Function

Private Sub SkizzeStarten(doc As Object, ByVal nr As Integer)
    doc.ClearSelection2 True
    Ebene(doc, nr).Select2 False, 0
    doc.SketchManager.InsertSketch True
    doc.SketchManager.AddToDB = True            ' exakte Koordinaten, kein Fangen
    doc.SketchManager.DisplayWhenAdded = False
End Sub

Private Function SkizzeBeenden(doc As Object, ByVal name As String) As Object
    Dim f As Object
    doc.SketchManager.DisplayWhenAdded = True
    doc.SketchManager.AddToDB = False
    doc.SketchManager.InsertSketch True
    Set f = doc.FeatureByPositionReverse(0)
    If Not f Is Nothing Then f.Name = name
    Set SkizzeBeenden = f
End Function

Private Sub Linie(doc As Object, ByVal x1 As Double, ByVal y1 As Double, ByVal x2 As Double, ByVal y2 As Double)
    doc.SketchManager.CreateLine x1 * MM, y1 * MM, 0, x2 * MM, y2 * MM, 0
End Sub

Private Sub Mittellinie(doc As Object, ByVal x1 As Double, ByVal y1 As Double, ByVal x2 As Double, ByVal y2 As Double)
    doc.SketchManager.CreateCenterLine x1 * MM, y1 * MM, 0, x2 * MM, y2 * MM, 0
End Sub

' Geschlossener Linienzug durch alle Punkte pts(i, 0..1) in mm
Private Sub Polygonzug(doc As Object, pts() As Double)
    Dim i As Long, j As Long, n As Long
    n = UBound(pts, 1)
    For i = 0 To n
        If i = n Then j = 0 Else j = i + 1
        Linie doc, pts(i, 0), pts(i, 1), pts(j, 0), pts(j, 1)
    Next i
End Sub

' Flache Liste (x0, y0, x1, y1, ...) -> Punktfeld
Private Function Punkte(v As Variant) As Double()
    Dim n As Long, i As Long, p() As Double
    n = (UBound(v) + 1) \ 2
    ReDim p(0 To n - 1, 0 To 1)
    For i = 0 To n - 1
        p(i, 0) = v(2 * i): p(i, 1) = v(2 * i + 1)
    Next i
    Punkte = p
End Function

' Rechte Profilhaelfte (erster und letzter Punkt auf z=0) an z=0 spiegeln
Private Function Spiegeln(h As Variant) As Double()
    Dim n As Long, i As Long, k As Long, p() As Double
    n = (UBound(h) + 1) \ 2
    ReDim p(0 To 2 * n - 3, 0 To 1)
    For i = 0 To n - 1
        p(i, 0) = h(2 * i): p(i, 1) = h(2 * i + 1)
    Next i
    k = n
    For i = n - 2 To 1 Step -1
        p(k, 0) = -h(2 * i): p(k, 1) = h(2 * i + 1)
        k = k + 1
    Next i
    Spiegeln = p
End Function

' Aufsatz/Schnitt rotieren um die (einzige) Mittellinie der Skizze, 360 Grad
Private Function Rotation(doc As Object, skizze As Object, ByVal schnitt As Boolean) As Object
    doc.ClearSelection2 True
    skizze.Select2 False, 0
    Set Rotation = doc.FeatureManager.FeatureRevolve2(True, True, False, schnitt, False, False, _
                   0, 0, 2 * PI, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    doc.ClearSelection2 True
End Function

' Radiale Bohrung als rotierter Schnitt: Skizze auf Ebene vorne, Mittellinie
' unter dem Winkel (0 Grad = +X, 90 Grad = +Y), Rechteck = halber Bohrungsquerschnitt
Private Function RadialeBohrung(doc As Object, ByVal winkel As Double, ByVal d As Double, _
                                ByVal rVon As Double, ByVal rBis As Double, ByVal name As String) As Object
    Dim w As Double, c As Double, s As Double, rr As Double, sk As Object, f As Object
    Dim p(0 To 3, 0 To 1) As Double
    w = winkel * PI / 180: c = Cos(w): s = Sin(w): rr = d / 2
    p(0, 0) = c * rVon: p(0, 1) = s * rVon
    p(1, 0) = c * rBis: p(1, 1) = s * rBis
    p(2, 0) = c * rBis - s * rr: p(2, 1) = s * rBis + c * rr
    p(3, 0) = c * rVon - s * rr: p(3, 1) = s * rVon + c * rr

    SkizzeStarten doc, 1
    Mittellinie doc, 0, 0, c * (rBis + 5), s * (rBis + 5)
    Polygonzug doc, p
    Set sk = SkizzeBeenden(doc, "Skizze_" & name)
    Set f = Rotation(doc, sk, True)
    If Not f Is Nothing Then f.Name = name
    Set RadialeBohrung = f
End Function

Private Sub Material(doc As Object, ByVal werkstoff As String)
    On Error Resume Next
    doc.SetMaterialPropertyName2 "", "solidworks materials.sldmat", werkstoff
    If Err.Number <> 0 Then Fehler "Werkstoff '" & werkstoff & "' bitte manuell zuweisen"
    On Error GoTo 0
End Sub

Private Sub Eigenschaften(doc As Object, ByVal benennung As String, ByVal nummer As String, _
                         ByVal werkstoff As String)
    Dim cpm As Object
    Set cpm = doc.Extension.CustomPropertyManager("")
    ' 30 = Text, 2 = vorhandenen Wert ersetzen
    cpm.Add3 "Benennung", 30, benennung, 2
    cpm.Add3 "Zeichnungsnummer", 30, nummer, 2
    cpm.Add3 "Werkstoff", 30, werkstoff, 2
    cpm.Add3 "Description", 30, benennung, 2
    cpm.Add3 "PartNo", 30, nummer, 2
End Sub

Private Function Speichern(doc As Object, ByVal dateiname As String) As String
    Dim fehlerCode As Long, warnung As Long, pfad As String
    pfad = gOrdner & dateiname
    doc.ShowNamedView2 "", 7                    ' 7 = Isometrie
    doc.ViewZoomtofit2
    If doc.Extension.SaveAs(pfad, 0, 1, Nothing, fehlerCode, warnung) Then
        Speichern = pfad
    Else
        Fehler "Speichern fehlgeschlagen: " & dateiname & " (Code " & fehlerCode & ")"
    End If
End Function

Private Sub Fehler(ByVal text As String)
    gProtokoll = gProtokoll & "- " & text & vbCrLf
    Debug.Print text
End Sub
