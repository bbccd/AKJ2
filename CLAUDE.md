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
- Tests: zurückgestellt; zusammen mit der Library angehen (Einstieg: Regressionstest per Chart-CSV-Export gegen
  Referenz, später Pine-Testskript mit erfundenen Kerzen für die Sonderfälle aus Bug-Reports). Nicht von selbst anstoßen.
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
  damit sie unter der Statuszeile steht): Sektor (syminfo.sector) | Industrie (syminfo.industry) | „(evtl. XLY)“ – Sektor-ETF ist
  eigenes Mapping TradingView-Sektor → SPDR XL* (Näherung, nicht gegen ETF-Bestände geprüft, nur USD-Aktien);
  Select Sector SPDRs enthalten nur S&P-500-Aktien, Mitgliedschaft unbekannt → bewusst vorsichtig formuliert. Börsen-Spalte entfernt: syminfo.prefix = Datenquelle (bei Nutzer „BATS“),
  nicht Heimatbörse. Index-Mitgliedschaft nicht in Pine; Listen im Code vom Nutzer verworfen (zu groß).
- Pine Screener (Nutzer hat Premium): Plots „Setup-Status (1 Long / -1 Short / 0)“, „Setup Entry“, „Setup SL“
  nur im Datenfenster (display.data_window). Plot-Titel nicht ändern – sonst brechen gespeicherte Screener-Filter.
  Screener-Plots MÜSSEN die ersten plot()-Aufrufe im Skript bleiben (Screener zeigte „Setup-Status“ nicht mehr,
  als die MAs davor standen; nach Verschieben an den Anfang wieder da – vom Nutzer bestätigt).
  Im Screener ist earnings.future_time leer (getestet) → Earnings-Sperre greift dort nicht. Nutzer will KEINE
  Schätzung des Termins; Einschränkung ist im README dokumentiert, Treffer werden im Chart geprüft.

- `akj_strategy.pine` – Backtest-Strategie (nur Daily), Setup-Logik KOPIERT aus dem Indikator (synchron halten!).
  Positionsgröße: Max. Drawdown (2000 $) × Risiko/Trade (1 %) / |Entry − SL|, ganze Stück.
  Ausstieg: „CRV 1:1 (komplett)“ oder „Trailing BB-Mittelband“ (ab 1:1 SL auf BE, dann BB-Mid);
  Default Trailing nur Long, Short immer 1:1. Kein 50-%-Teilverkauf (Nutzer-Vorgabe). Kommission 1 $/Order,
  Slippage 2 Ticks (strategy()-Properties), Bar Magnifier an. Orders werden zum Close für die nächste Kerze
  gesetzt; dafür Trend „next“ (Daily ohne [1], Weekly am Freitag aus der laufenden Woche).

## Performance (Issue #21) – beim Weiterentwickeln beachten
- Höhere TFs: genau EIN request.security je Zeiteinheit (D/W/M, Funktion `htfData()` als Tupel). Neue HTF-Werte dort
  ergänzen statt neue Abrufe anzulegen. Nicht höhere TFs als das Chart werden als "" (Chart selbst) angefragt,
  sonst lädt TradingView Intrabar-Daten (z. B. alle Daily-Kerzen im Weekly-Chart).
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
  FVG zählt, bis komplett gefüllt (teilweise gefüllt → Restlücke). Wirkung wie Risiko-Filter (setupOk = riskOk
  und kein FVG). TFs 4h/D/W/M je mit Rückschau in Kerzen (W + D: D/W/M, M + W: W/M, D + 4h: alle). HTF-FVGs per request.security ([1] +
  lookahead) aus abgeschlossenen Kerzen, gefüllt mit Chart-Kerzen; nur ungefüllte werden gemerkt. Optionale
  Kontroll-Kästen. FVGs werden immer berechnet (auch Filter aus), damit die Screener-Spalte „FVG im
  Gewinnbereich (1 / 0)“ unabhängig vom Filter gefüllt ist. Strategie noch NICHT synchronisiert (erst nach Test im Indikator).
- Risiko: 0,5–1 % (normal) bzw. 1–2 % (stark) des max. akzeptierten Depot-Drawdowns pro Trade.

## Stand / nächste Schritte (Nov. 2026)
- Zuletzt gemergt: #21 Performance (PR #27), davor D + 4h (#14) und FVG-Filter (#18).
- Aktuelle Issues immer per `gh issue list -R bbccd/AKJ2` holen (diese Liste kann veralten).
- Kandidaten: FVG-Filter in `akj_strategy.pine` übernehmen (Indikator ist getestet); Idee #16 relative Stärke;
  Idee #17 Library + Tests (siehe „Tests“ oben). Nutzer meldet evtl. noch einen kleinen Bug aus D + 4h als Issue.
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
  Entscheidung: Setup-Logik zunächst aus dem Indikator KOPIEREN (eigene Datei). Später evtl. Library
  (privat veröffentlicht), dann zuerst nur für die Strategie; Indikator behält vorerst den vollen Code.
  Bei Regeländerungen bis dahin Indikator und Strategie synchron halten!
