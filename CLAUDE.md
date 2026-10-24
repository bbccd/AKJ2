# AKJ Trading-Indikator (PineScript v6)

Indikator (später auch Strategie) für TradingView nach dem „Aktien-Kann-Jeder Strategie-Guide“
(PDF: `~/Library/Mobile Documents/com~apple~CloudDocs/Trading/Dein Aktien-Kann-Jeder Strategie-Guide 2.pdf`).
Kommunikation auf Deutsch. Code kann nicht lokal kompiliert werden – der Nutzer testet in TradingView
und meldet Fehler zurück.

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
  reiner Weekly-Hintergrund wie in AKJ2 per Setting wählbar.

- Pine Screener (Nutzer hat Premium): Plots „Setup-Status (1 Long / -1 Short / 0)“, „Setup Entry“, „Setup SL“
  nur im Datenfenster (display.data_window). Plot-Titel nicht ändern – sonst brechen gespeicherte Screener-Filter.
  Im Screener ist earnings.future_time leer (getestet) → Earnings-Sperre greift dort nicht. Nutzer will KEINE
  Schätzung des Termins; Einschränkung ist im README dokumentiert, Treffer werden im Chart geprüft.

## Strategie-Regeln (wie mit dem Nutzer geklärt)
- BB 10 / 1, Williams %R Länge 4.
- Trend: 2x Close > oberes BB = Kauf, 2x Close < unteres BB = Verkauf. Gilt, bis der Gegentrigger kommt.
- Timeframes: nur Weekly + Daily, der Monatschart spielt keine Rolle (vom Nutzer ausdrücklich so gewollt).
  Daily-Chart: Trigger = Weekly UND Daily, Setups. Weekly-Chart: nur Weekly-Trigger, keine Setups.
- Nur abgeschlossene Kerzen (Tag bzw. Woche) erzeugen Trigger und %R-Signale – keine Signale aus laufenden Kerzen.
  Regime gilt ab der Kerze NACH der Trigger-Kerze (Grenze zwischen beiden), in W und D.
- Long-Setup: beide TFs Kauf, rote Kerze, %R-Close ≤ −80. Short spiegelbildlich (grüne Kerze, ≥ −20).
  Mehrere Setup-Tage in Folge → immer der aktuellste zählt (Entry/SL werden nachgezogen).
- Entry: Stop-Order Hoch + Puffer (Long) / Tief − Puffer (Short). Gaps ohne Auslösung ignorieren.
- SL: Tief − Puffer (Long) / Hoch + Puffer (Short). Puffer in Ticks einstellbar (Default 2), optional ‰-Minimum.
- Nachziehen laut Guide: solange Setup offen, zieht jeder weitere Downday (Long) / Upday (Short)
  den Entry nach – ohne erneute %R-Prüfung. Setup endet, sobald Entry erreicht wird.
- SL (vom Nutzer präzisiert): immer unter tiefstem Tief (Long) / über höchstem Hoch (Short) seit erster
  Signalkerze; auch Kerzen ohne Signal (z. B. grüne bei Long) ziehen ihn nach. SL wandert nie zurück.
- (Nur für spätere Strategie:) Ziel 1 bei CRV 1:1 → 50 % schließen, SL auf Einstand; Rest optional am BB-Mittelband nachziehen.
- Earnings: Sperrfenster (8 Kalendertage vorher bis Earnings-Tag/-Woche) grau hinterlegen, in allen Charts;
  dort standardmäßig keine Signale. Eigener „E“-Marker entfernt (lag auf der Folgekerze) – TradingView zeigt E selbst.
  Vergangene Fenster per bgcolor-Offset rückwirkend; bei Zahlen nach Börsenschluss ist der Folgetag mit grau.
- Risiko-Filter (Setting, Default an): Risiko % = |Entry − SL| / Entry, nur Setups mit 2–7 % anzeigen/im Screener.
  Filtert nur die Anzeige (Linien, Marker, Hervorhebung, Alerts, Screener), Setup-Zustand läuft intern weiter.
  Label des aktuellen Setups zeigt unten „R: 2.3 %“ (eine Nachkommastelle).
- Risiko: 0,5–1 % (normal) bzw. 1–2 % (stark) des max. akzeptierten Depot-Drawdowns pro Trade.

## Offene Punkte / Refinement
- Setup-Verfall: laut PDF keiner, in der Praxis aber gewünscht → Hook `setupExpired()` + Input vorhanden (Default aus).
- Puffer abhängig vom Kurs (z. B. „mind. 2 Ticks und mind. x ‰“) verfeinern.
- Earnings-Filter wirkt nur auf aktuelle Signale (TradingView liefert nur das nächste Datum) – für Backtest lösen.
  Folge: Nach den Earnings erscheinen beim Neuladen Setups aus dem ehemaligen Fenster. Vom Nutzer als
  akzeptabel/hilfreich bewertet (live war die Sperre aktiv); im README dokumentiert.
- Später: `strategy()`-Version für Backtests, Positionsgröße aus Risiko-Regeln.
