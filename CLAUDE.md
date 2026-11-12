# AKJ Trading-Indikator (PineScript v6)

Indikator (später auch Strategie) für TradingView nach dem „Aktien-Kann-Jeder Strategie-Guide“
(PDF: `~/Library/Mobile Documents/com~apple~CloudDocs/Trading/Dein Aktien-Kann-Jeder Strategie-Guide 2.pdf`).
Kommunikation auf Deutsch. Code kann nicht lokal kompiliert werden – der Nutzer testet in TradingView
und meldet Fehler zurück.

## Zusammenarbeit (gilt auf jedem Rechner – Nutzer arbeitet am MacBook und am großen Mac)
- Vor Änderungen oder Erklärungen zur Trading-Logik den Strategie-Guide (PDF oben) SELBST lesen, nicht nur
  diese Zusammenfassung. Der Nutzer ärgert sich über Rückfragen zu Dingen, die im Guide stehen. Rückfragen nur
  zu Punkten, die der Guide offen lässt. PDF liegt in iCloud Drive; Read-Tool ohne `pages` (poppler fehlt ggf.).
- Git: jede Änderung auf eigenem Branch. Committen, pushen und mergen NUR auf ausdrücklichen Wunsch; nach dem
  Merge: GitHub löscht den Remote-Branch automatisch (Repo-Setting „Automatically delete head branches“ an);
  den lokalen Branch danach ohne Rückfrage löschen (Nutzer hat zugestimmt), `main` pullen. Zusammengehörige Themen ggf. als getrennte Commits.
- Branch-Namen mit Slash (Nutzer-Vorgabe, auf beiden Rechnern einheitlich): `feature/<kurzname>` für neue Funktionen,
  `fix/<issue-nr>-<kurzname>` für Fehler (z. B. `fix/1-earnings-grau`; Issue-Nr. nur, wenn ein GitHub-Issue existiert,
  sonst `fix/<kurzname>`), `docs/<kurzname>` für reine Doku. Kurzname englisch oder deutsch, klein, mit Bindestrichen.
  Nicht `bugfix/` oder Namen ohne Präfix verwenden.
- GitHub-Issues (Bugs und Ideen) über `gh` lesen (`gh issue list -R bbccd/AKJ2`); `gh` muss als bbccd angemeldet sein.
- Grundsatz: bestehende Funktionalität darf sich nicht ungewollt ändern (Defaults beibehalten).
- GitHub: privates Repo `bbccd/AKJ2` auf dem PRIVATEN Account bbccd, Remote über SSH-Alias
  `git@github-bbccd:bbccd/AKJ2.git` (Eintrag `Host github-bbccd` in `~/.ssh/config` mit eigenem Key). Niemals den
  Arbeits-Account bB-0202 (Alias `github-github-haeger`) verwenden. Fehlt der Alias auf einem Rechner: Nutzer fragen,
  nicht auf einen anderen Account ausweichen.
- Library + Tests (Issue #17, Nov. 2026, Nutzer-Entscheidung): `akj_lib.pine` = Pine-Library „AKJ2“ mit den reinen
  Funktionen (alle Eingaben als Parameter, kein Zugriff auf Inputs/Serien/syminfo; `// @function/@param/@returns`
  dokumentieren). Nutzer veröffentlicht sie PRIVAT auf TradingView; jede Änderung = neue Version, Einbinden per
  `import bBccdde/AKJ2/<Version> as akj` (TradingView-Benutzername bBccdde). `tests/akj_tests.pine` importiert die Library und prüft sie mit
  erfundenen Werten (Tabelle im Chart); Benutzername/Version in der Importzeile vom Nutzer einzutragen. Reihenfolge
  (vom Nutzer vorgegeben): 1. Library erstellen/veröffentlichen, 2. Tests dagegen schreiben, 3. erst bei guter
  Abdeckung die Kopien aus Indikator und Strategie entfernen und importieren – seit v5 umgesetzt: beide Skripte
  importieren die Library; Regeländerungen gehören in die Library (neue Version, Importzeile in Indikator, Strategie
  und Tests hochsetzen). Library-Inhalt:
  Setup-Zustandsautomat, FVG-Funktionen (seit v4), bbTrendState/maCalc auf Serien (v5; Tests mit synthetischer
  Serie aus bar_index), fvgFill mit Füllregeln partial/ce + Feld Fvg.mid (v6, Issue #36). Damit ist die gesamte Logik in der Library – nächster Schritt: Indikator und Strategie
  umschalten – erledigt auf feature/library (Regressionstest mit tests/compare_reference.py vorher/nachher).
- Regressionstest (`tests/compare_reference.py`): TradingView-Exporte in `tests/reference/` (Daily, Defaults, ADJ
  aus) sind die Referenz; neue Exporte nach `tests/current/` (gitignored), `--all` vergleicht die Indikator-Plots
  Kerze für Kerze (Liste COLUMNS im Skript; „Tage bis Earnings“ bewusst nicht). Der Export enthält auch die
  Datenfenster-Plots (geprüft). Pflicht vor/nach dem Umschalten von Indikator und Strategie auf die Library.
  ACHTUNG: Die Referenzen stammen von VOR Issue #36 (alte FVG-Füllregeln). Für einen Vergleich im Indikator
  einstellen: „Dochte zählen“ an, „Teilweise Füllung verkleinert“ an, „Gefüllt, wenn: Komplett abgedeckt“ –
  sonst weichen „Offene FVGs (Anzahl)“ und „FVG im Gewinnbereich“ ab. Alternativ Referenzen neu exportieren.
- Offen, nicht entschieden: Farbe „Kein Regime“ evtl. in „Regime endet“ umbenennen.

## Dateien
- `akj_setup_indikator.pine` – aktueller Indikator „AKJ2.0 – Trend & Setup Detector“ (v6).
  Zweck: Aktien schnell auf Setups scannen. Bewusst schlank: kein Trade-Management, keine
  Entry-/Exit-Marker im Chart (Nutzer will keine Marker-Flut). Setup = blaue Entry- + rote SL-Linie
  plus Marker auf der Signalkerze: gefülltes Label mit Spitze zur Kerze, weißer fetter Text
  („L“ unter der Kerze / „S“ darüber; Stil wie die früheren UP/DOWN-Labels). Keine weiteren Marker.
  Marker-Farbe = Trigger-Hintergrundfarbe (deckend); Marker des aktuellen Setups = Hervorhebungsfarbe.
  Ausnahme: aktuelles (auf der jüngsten Kerze offenes) Setup wird hervorgehoben – Hintergrund blau/violett ab
  erster Signalkerze (max. 10) + Label mit Entry/SL; per Setting „Aktuelles Setup hervorheben“ abschaltbar.
  Basiert auf dem früheren Nutzer-Indikator „AKJ2 – Weekly Trend Detector“ (v5); dessen Darstellung
  (BB-Farben, Trigger-Hintergrund) soll erhalten bleiben; Farben jetzt türkis (Long) / pink (Short), da der Nutzer einen weiteren Indikator mit grün/roten Balken nutzt. Die senkrechten UP/DOWN-Linien wurden
  auf Wunsch entfernt (lassen sich nicht auf die Grenze zwischen zwei Kerzen legen; Hintergrund zeigt sie).
  Hintergrund zeigt standardmäßig den Trigger (beide TFs Kauf = türkis, beide Verkauf = pink, sonst keiner);
  reiner Hintergrund des übergeordneten Trends wie in AKJ2 per Setting „Übergeordneter Trend“ wählbar
  (hieß bis Nov. 2026 „Weekly-Trend“).
- Einstellungen (Nov. 2026 umgebaut): Gruppen „Regeln – …“ (Spielweise & Trend, Setup & Entry, Earnings, Fair
  Value Gaps) zuerst, dann „Anzeige – …“ (Trend & Setup, Moving Averages, Zusatzinfos), zuletzt „Zeitraum“.
  Farbe/Dicke/Linienart von plot()/fill() (BB, BB-Füllung, MAs, Entry/SL) sind KONSTANT im Code, damit sie im
  Reiter „Style“ erscheinen (TradingView zeigt sie dort nur bei konstanten Werten) – keine Inputs dafür anlegen.
  Bedingte Farben (bgcolor für Regime/aktuelles Setup, Labels, Tabellen, line.new) kann der Style-Reiter nicht →
  bleiben Inputs. Datenfenster-Plots (Screener, Diagnose) und per Input gesteuerte bgcolor() haben `editable = false`, damit der
  Style-Reiter nur Linien/Füllungen zeigt (BB, MAs, Entry/SL); ohne das konnte man die Screener-Plots dort versehentlich
  im Chart einschalten. Input-Titel sind die Schlüssel gespeicherter Werte: Umbenennen setzt sie beim Nutzer zurück;
  Reihenfolge/Gruppe ändern ist unkritisch. Inline-Zeilen: Titel nur am ersten Input (sonst Editor-Warnung).

- BB-Füllung zwischen den Bändern (Issue #15): Grau #787B86 mit 8 % Deckkraft (#787B8614), Default an,
  im Style-Reiter abschaltbar; bewusst schwächer als Trigger- (25 %) und Earnings-Hintergrund (45 %), hell/dunkel tauglich.
- Moving Averages im Indikator (nur Anzeige, keine Setup-Logik): 20/50/150/200, SMA/EMA für alle gemeinsam,
  jede MA einzeln + Paket gesamt abschaltbar; Farbe, Dicke (3), Linienart (gestrichelt) je MA im Style-Reiter.
  Farben wie TradingView-„MA Ribbon“ (Gelb → Orange → Rot = kurz → lang); 200er-Rot liegt nahe an
  SL-Linie/unterem BB – ggf. anpassen.
- Zusatzinfos (Gruppe „Zusatzinfos“, nur Anzeige): All-Time High als dicke Linie (extend.both) + Label
  „All-Time High <Preis>“, Buttergelb #FFE135 (bewusst heller als MA 20 #F6C309). ATH aus Monatsdaten
  (ganze Historie) + Chart-Kerzen (laufender Monat).
  ATH-Label rechts neben der jüngsten Kerze (bar_index + 5, Spitze links). Früher am linken sichtbaren Rand
  (chart.left_visible_bar_time) – auf Nutzerwunsch aufgegeben (Issue #21): chart.left/right_visible_* zwingt
  TradingView zur kompletten Neuberechnung bei jedem Scrollen/Zoomen. NICHT wieder verwenden.
  Tabelle oben Mitte (unten überlappte Volumen; unsichtbare Abstandszeile „Abstand von oben“ Default 6 %,
  damit sie unter der Statuszeile steht): Sektor (syminfo.sector) | Industrie (syminfo.industry) | „(evtl. XLY)“ | Sektor-Trend „XLY  W ▲  D ▲“ (Issue #16) – Sektor-ETF ist
  eigenes Mapping TradingView-Sektor → SPDR XL* (Näherung, nicht gegen ETF-Bestände geprüft, nur USD-Aktien);
  Select Sector SPDRs enthalten nur S&P-500-Aktien, Mitgliedschaft unbekannt → bewusst vorsichtig formuliert. Börsen-Spalte entfernt: syminfo.prefix = Datenquelle (bei Nutzer „BATS“),
  nicht Heimatbörse. Index-Mitgliedschaft nicht in Pine; Listen im Code vom Nutzer verworfen (zu groß).
- Pine Screener (Nutzer hat Premium): Plots „Setup-Status (1 Long / -1 Short / 0)“, „Setup Entry“, „Setup SL“
  nur im Datenfenster (display.data_window). Plot-Titel nicht ändern – sonst brechen gespeicherte Screener-Filter.
  Screener-Plots MÜSSEN die ersten plot()-Aufrufe im Skript bleiben (Screener zeigte „Setup-Status“ nicht mehr,
  als die MAs davor standen; nach Verschieben an den Anfang wieder da – vom Nutzer bestätigt).
  Im Screener ist earnings.future_time leer (getestet) → Earnings-Sperre greift dort nicht. Nutzer will KEINE
  Schätzung des Termins; Einschränkung ist im README dokumentiert, Treffer werden im Chart geprüft.

- `akj_strategy.pine` – Backtest-Strategie (nur Daily), Setup-Logik aus der Library (akj.setupStep) wie im Indikator.
  Positionsgröße: Max. Drawdown (2000 $) × Risiko/Trade (1 %) / |Entry − SL|, ganze Stück.
  Ausstieg: „CRV 1:1 (komplett)“ oder „Trailing BB-Mittelband“ (ab 1:1 SL auf BE, dann BB-Mid);
  Default Trailing nur Long, Short immer 1:1. Kein 50-%-Teilverkauf (Nutzer-Vorgabe). Kommission 1 $/Order,
  Slippage 2 Ticks (strategy()-Properties), Bar Magnifier an. Orders werden zum Close für die nächste Kerze
  gesetzt; dafür Trend „next“ (Daily ohne [1], Weekly am Freitag aus der laufenden Woche).

- Dividendenbereinigung (Issue #26): Schalter „ADJ“ gilt je Chart und steckt in syminfo.tickerid
  (`={"adjustment":"dividends",…}`); request.security erbt sie. Bei Wochenschluss nahe am BB kann der Weekly-Trend
  im Daily-Chart (ADJ aus) anders sein als im Weekly-Chart (ADJ an) – kein Code-Fehler, Charts gleich einstellen.
  Indikator warnt in der Chart-Mitte bei aktiver Bereinigung (Input „Warnung bei Dividendenbereinigung (ADJ)“,
  Default an; Erkennung über str.contains(syminfo.tickerid, "adjustment"), vom Nutzer bestätigt. Nicht unten
  links/rechts: dort überdeckt der Volumen-Indikator die Meldung). Nichts im Code
  erzwingen (sonst laufen Chart-Trend und abgerufener HTF-Trend auseinander).

## Performance (Issue #21) – beim Weiterentwickeln beachten
- Höhere TFs: genau EIN request.security je Zeiteinheit (D/W/M, Funktion `htfData()` als Tupel). Neue HTF-Werte dort
  ergänzen statt neue Abrufe anzulegen. Abrufe laufen nur, wenn Spielweise + Chart sie brauchen (`htfReq(need, tf)`,
  dynamische Requests): D nur im 4h-Chart, W nur im Trade-Chart von W + D / D + 4h, M immer (ATH). Nie eine
  Zeiteinheit abrufen, die nicht höher als das Chart ist – sonst lädt TradingView Intrabar-Daten.
- Zeichnen auf der jüngsten Kerze (Kästen, Tabellen) nur, wenn sich etwas geändert hat (`fvgDrawn`-Muster), nicht
  bei jedem Tick – `barstate.islast` ist während der Handelszeit bei jedem Kurs-Update wahr.
- Plot-Budget: TradingView erlaubt max. 64 plot/bgcolor/fill-Aufrufe je Skript; der Indikator nutzt ~51
  (19 plot, 31 bgcolor, 1 fill). Neue Features sparsam mit plot()/bgcolor() umsetzen.
- FVGs: sortierte Listen (bullisch absteigend nach top, bärisch aufsteigend nach bot) + Ablauf-Warteschlange je TF;
  Füllen und Treffer-Prüfung brechen früh ab. Keine Schleife über alle FVGs pro Kerze einbauen.
- Kein chart.left_visible_bar_time / chart.right_visible_bar_time (Neuberechnung bei jedem Scrollen).
- Messen: Pine Profiler im Pine-Editor (Drei-Punkte-Menü → Profiler-Modus) zeigt die Zeit je Zeile; im Popover
  der teuersten Zeilen steht die Gesamtzeit („… s total“). Vergleich: frühere Version über die Version History
  im Pine-Editor wiederherstellen, gleiche Aktie/TF/Einstellungen. Stand nach #21: etwa halbe Laufzeit wie vorher.
- FVG-Kästen: max. 400 (die nächsten am Kurs, abwechselnd unter/über dem Kurs); sind es mehr, Hinweis
  „FVG-Anzeige: X von Y“ unten rechts. Der Filter prüft immer alle offenen FVGs (vom Nutzer so gewünscht:
  Anzeige darf nicht stillschweigend FVGs weglassen).

## Strategie-Regeln (wie mit dem Nutzer geklärt)
- BB 10 / 1, Williams %R Länge 4.
- Trend: 2x Close > oberes BB = Kauf, 2x Close < unteres BB = Verkauf. Gilt, bis der Gegentrigger kommt.
- Spielweise (Setting, Default „W + D“ – muss sich exakt wie vor Einführung der Spielweisen verhalten!):
  „W + D“: Daily-Chart = Trigger W UND D + Setups; Weekly-Chart nur Weekly-Trigger; Monat spielt hier keine Rolle.
  „M + W“: Weekly-Chart = Trigger M UND W + Setups (gleiche Regeln eine Ebene höher); Daily-Chart nichts.
  „D + 4h“ (Issue #14, nicht im Guide, mit Nutzer analog geklärt): 4h-Chart = Trigger D UND 4h + Setups; Daily- und
  Weekly-Chart nur ihr eigener Trigger. Tagesende = session.islastbar_regular (4h-Chart mit regulären Handelszeiten).
  Risiko 1–5 %, Earnings 8 Tage, FVGs 4h/D/W/M (4h-Rückschau 1000 Kerzen), Earnings-Linie auch im 4h.
  Monthly-Chart: in allen Spielweisen nur Monthly-Trigger-Hintergrund, KEIN Earnings-Grau (sonst 2 von 3 Monaten grau). Eigene Risiko-Grenzen (W+D 2–7 %,
  M+W 3–12 %, D+4h 1–5 %) und Earnings-Fenster (je 8 Tage) pro Spielweise. Ein Skript; für beide Spielweisen im selben
  Chart den Indikator zweimal hinzufügen. Strategie: nur W + D.
- Nur abgeschlossene Kerzen (Tag bzw. Woche) erzeugen Trigger und %R-Signale – keine Signale aus laufenden Kerzen.
  Regime gilt ab der Kerze NACH der Trigger-Kerze (Grenze zwischen beiden), in W und D.
  Regimewechsel-Ankündigung: Nach Close der jüngsten Kerze Hintergrund per bgcolor offset = 1 auf dem Platz der
  nächsten Kerze, in der neuen Regime-Farbe bzw. „Kein Regime“; eigene Farben, abschaltbar. Gleichbleibendes Regime:
  normale Hintergrundfarbe (Checkbox „Auch gleichbleibendes Regime zeigen“), ohne Regime leer. Nächste Kerze im
  Sperrfenster: Earnings-Grau darüber (wie bei normalen Kerzen; Folgetag-Grau nach Börsenschluss-Zahlen nicht vorhersehbar).
  Ausnahme Setups: Ist der Close der Kerze im Trade-TF selbst der Gegentrigger, entsteht kein Setup/Marker und ein
  offenes Setup endet sofort (longNext/shortNext). Gilt auch für den übergeordneten TF am Periodenende
  (W: Freitag wie in der Strategie, M: nächste Weekly-Kerze beginnt im neuen Monat). Bekannte Lücke: Feiertags-Freitag.
- Long-Setup: beide TFs Kauf, rote Kerze, %R-Close ≤ −80. Short spiegelbildlich (grüne Kerze, ≥ −20).
  Mehrere Setup-Tage in Folge → immer der aktuellste zählt (Entry/SL werden nachgezogen).
- Entry: Stop-Order Hoch + Puffer (Long) / Tief − Puffer (Short). Gaps ohne Auslösung ignorieren.
- SL: Tief − Puffer (Long) / Hoch + Puffer (Short).
- Puffer (Issue #24, aus dem Handelsplan des Nutzers, nicht im Guide): bis zur Kurs-Schwelle (Default 100) fest
  3 Ticks, darüber 0,3 ‰ vom Kurs (Issue-Beispiel 500 $ → 0,15 $; Nutzer hatte „3 ‰“ geschrieben, auf Nachfrage
  0,3 ‰ bestätigt), auf den Tick aufgerundet. Ein Puffer für Entry und SL (vorher getrennte Tick-Inputs, je 2).
  „Glatte Zahlen meiden“ (Default an, Raster 0,50): Level mindestens einen Puffer jenseits der nächsten
  Rasterstufe, falls es sonst innerhalb eines Puffers davor läge (`bufLevel(price, dir)` in beiden Skripten).
- Nachziehen laut Guide: solange Setup offen, zieht jeder weitere Downday (Long) / Upday (Short)
  den Entry nach – ohne erneute %R-Prüfung. Setup endet, sobald Entry erreicht wird.
- SL (vom Nutzer präzisiert): immer unter tiefstem Tief (Long) / über höchstem Hoch (Short) seit erster
  Signalkerze; auch Kerzen ohne Signal (z. B. grüne bei Long) ziehen ihn nach. SL wandert nie zurück.
- Earnings: Sperrfenster (8 Kalendertage vorher bis Earnings-Tag/-Woche) grau hinterlegen, in allen Charts;
  dort standardmäßig keine Signale. Eigener „E“-Marker entfernt (lag auf der Folgekerze) – TradingView zeigt E selbst.
  Vergangene Fenster per bgcolor-Offset rückwirkend; bei Zahlen nach Börsenschluss ist der Folgetag mit grau.
  Earnings-Linie: dick, dunkelgrau, nur Daily (in D + 4h auch 4h), abschaltbar; auf der letzten grauen Kerze (Mitte der Kerze, nicht deren Rand).
- Risiko-Filter (Setting, Default an): Risiko % = |Entry − SL| / Entry, nur Setups mit 2–7 % anzeigen/im Screener.
  Filtert nur die Anzeige (Linien, Marker, Hervorhebung, Alerts, Screener), Setup-Zustand läuft intern weiter.
  Label des aktuellen Setups zeigt unten „R: 2.3 %“ (eine Nachkommastelle).
- FVG-Filter (Issue #18, mit Nutzer geklärt; nicht im Guide): Setting, Default AUS (Nutzer: muss abschaltbar sein).
  Long ungültig bei ungefülltem BÄRISCHEM FVG, Short bei bullischem, das [Entry, Ziel 1:1] irgendwie überlappt.
  Füllregeln (Issue #36, Nutzer-Vorgabe nach Recherche, kein allgemeiner Standard): Default nur Kerzenkörper
  (Open–Close) der Folgekerzen, geschlossen erst bei kompletter Abdeckung, bis dahin unverändert. Optionen:
  „Mitte berührt (Consequent Encroachment)“ = geschlossen ab 50 % der URSPRÜNGLICHEN Lücke (Fvg.mid), „Teilweise
  Füllung verkleinert“ + „Dochte zählen“ = Verhalten bis v5. Die Lücke selbst entsteht immer aus Hoch/Tief der
  Kerzen 1 und 3. Wirkung wie Risiko-Filter (setupOk = riskOk
  und kein FVG). TFs 4h/D/W/M je mit Rückschau in Kerzen (W + D: D/W/M, M + W: W/M, D + 4h: alle). HTF-FVGs per request.security ([1] +
  lookahead) aus abgeschlossenen Kerzen, gefüllt mit Chart-Kerzen; nur ungefüllte werden gemerkt. Optionale
  Kontroll-Kästen. FVGs werden immer berechnet (auch Filter aus), damit die Screener-Spalte „FVG im
  Gewinnbereich (1 / 0)“ unabhängig vom Filter gefüllt ist. Strategie (seit Nov. 2026, mit #36): gleicher Filter als
  Order-Bedingung (fvgOk), Default aus; FVGs dort NUR bei aktivem Filter berechnet, Monthly-Abruf nur dann; Weekly-Kerzen
  kommen aus dem bestehenden Weekly-Abruf (htfData wie im Indikator).
- Risiko: 0,5–1 % (normal) bzw. 1–2 % (stark) des max. akzeptierten Depot-Drawdowns pro Trade.
- Sektor-Trend (Issue #16, Nutzer-Regel, nicht im Guide): Trend des Sektor-ETF (akj.sectorEtf oder Input „Sektor-ETF“,
  auch Index möglich) in den beiden Zeiteinheiten der Spielweise, gleiche Trigger-Regel wie die Aktie, aus
  abgeschlossenen Kerzen. Indikator: NUR Anzeige (Sektor-Tabelle 4. Spalte, Status-Tabelle, Setup-Label) plus
  Screener-Plot „Sektor-Trend (1 / -1 / 0)“; zwei zusätzliche Abrufe, abschaltbar. Strategie: Filter, Default AN –
  Order nur, wenn ETF-Trend für die nächste Kerze (W am Freitag aus der laufenden Woche, D nach dem Close) der
  Setup-Richtung entspricht; ohne bekannten ETF keine Trades + orange Warnung. Setup-Zustand bleibt unabhängig
  (nur Orders gefiltert). Logik bewusst (noch) nicht in der Library – wenige Zeilen, nächste Version bündeln.

## Stand / nächste Schritte (Nov. 2026)
- Zuletzt gemergt (12.11.2026): PR #37 FVG-Füllregeln (#36, Library v6) + FVG-Filter in der Strategie (#18).
  Davor am selben Tag PR #35 Sektor-Trend (#16) + %R-Inputs zu den BB. Davor (11.11.): PR #34 Library-
  Umstellung (#17), PR #32 Performance-Nachtrag (HTF-Abrufe nur bei Bedarf, FVG-Kästen einmal je Kerze,
  Strategie ein Weekly-Abruf), PR #31 ADJ-Warnung (#26), PR #30 Einstellungen/Style-Reiter, PR #29 Puffer (#24).
  Davor #21 Performance (PR #27), D + 4h (#14), FVG-Filter (#18). Issue #26 war kein Bug (Dividendenbereinigung je Chart).
- Aktuelle Issues immer per `gh issue list -R bbccd/AKJ2` holen (diese Liste kann veralten). Stand 12.11.2026:
  keine offenen Issues. Der Nutzer testet den Indikator (Stand PR #37) ausführlich; Bugs kommen als Issues.
- Vorgeschlagene nächste Schritte (Reihenfolge nach Nutzen, nichts davon dringend):
  1. Regressions-Referenzen neu exportieren (`tests/reference/`, XLU/EBAY/AAPL Daily, Defaults, ADJ aus), damit
     der Vergleich wieder mit den Defaults läuft (seit #36 nur noch mit den alten Füll-Einstellungen, siehe oben).
  2. Sektor-Logik (secTrend/secNext aus Indikator und Strategie) in die Library – als Library v7 bündeln mit der
     nächsten Regeländerung, nicht allein (jede Version = Importzeile in drei Skripten hochsetzen).
  3. Backtest mit FVG-Filter an/aus über mehrere Aktien vergleichen (wie beim Sektor-Filter: Max. Drawdown und
     Trefferquote, nicht nur Nettogewinn) – entscheidet, ob der Default in der Strategie auf „an“ wechselt.
  4. Earnings im Backtest (vergangene Termine) bleibt ungelöst – Pine liefert sie nicht im Voraus; nur erneut
     prüfen, falls TradingView `request.earnings` mit Zeitpunkt der Ankündigung anbietet.
- Arbeitsweise des Nutzers: kopiert den Code in den Pine-Editor, testet im Chart/Screener und meldet Fehler zurück.
  Änderungen deshalb klein und nachvollziehbar halten und erklären, was zu prüfen ist.

## Offene Punkte / Refinement
- Externe Daten (z. B. Index-Mitgliedschaft): Pine hat keinen Internetzugriff. Einziger Weg wäre Pine Seeds
  (request.seed, CSV in GitHub-Repo) – Stand Okt. 2026: Anlage NEUER Repositories von TradingView ausgesetzt,
  bestehende laufen weiter; Interesse per Google-Formular im Repo tradingview-pine-seeds/docs. Später erneut prüfen.
- Setup-Verfall: laut PDF keiner, in der Praxis aber gewünscht → Hook `setupExpired()` + Input vorhanden (Default aus).
- Earnings-Filter wirkt nur auf aktuelle Signale (TradingView liefert nur das nächste Datum) – für Backtest lösen.
  Folge: Nach den Earnings erscheinen beim Neuladen Setups aus dem ehemaligen Fenster. Vom Nutzer als
  akzeptabel/hilfreich bewertet (live war die Sperre aktiv); im README dokumentiert.
- `strategy()`-Version für Backtests (`akj_strategy.pine`, in `main`), Positionsgröße aus Risiko-Regeln.
  Setup-Logik seit Nov. 2026 aus der Library (siehe „Library + Tests“ oben); FVG-Filter seit #36 auch in der
  Strategie (Default aus).
