# AKJ Trading-Indikator (PineScript v6)

Indikator (später auch Strategie) für TradingView nach dem „Aktien-Kann-Jeder Strategie-Guide“
(PDF: `~/Library/Mobile Documents/com~apple~CloudDocs/Trading/Dein Aktien-Kann-Jeder Strategie-Guide 2.pdf`).
Kommunikation auf Deutsch. Code kann nicht lokal kompiliert werden – der Nutzer testet in TradingView
und meldet Fehler zurück.

## Dateien
- `akj_setup_indikator.pine` – aktueller Indikator „AKJ2.0 – Trend & Setup Detector“ (v6).
  Zweck: Aktien schnell auf Setups scannen. Bewusst schlank: kein Trade-Management, keine
  Entry-/Exit-Marker im Chart (Nutzer will keine Marker-Flut). Setup = blaue Entry- + rote SL-Linie.
  Basiert auf dem früheren Nutzer-Indikator „AKJ2 – Weekly Trend Detector“ (v5); dessen Darstellung
  (BB-Farben, grün/oranger Hintergrund, senkrechte UP/DOWN-Linien) soll erhalten bleiben.
  Hintergrund zeigt standardmäßig den Trigger (beide TFs Kauf = grün, beide Verkauf = orange, sonst keiner);
  reiner Weekly-Hintergrund wie in AKJ2 per Setting wählbar.

## Strategie-Regeln (wie mit dem Nutzer geklärt)
- BB 10 / 1, Williams %R Länge 4.
- Trend: 2x Close > oberes BB = Kauf, 2x Close < unteres BB = Verkauf. Gilt, bis der Gegentrigger kommt.
- Timeframes: nur Weekly + Daily, der Monatschart spielt keine Rolle (vom Nutzer ausdrücklich so gewollt).
  Daily-Chart: Trigger = Weekly UND Daily, Setups. Weekly-Chart: nur Weekly-Trigger, keine Setups.
- Long-Setup: beide TFs Kauf, rote Kerze, %R-Close ≤ −80. Short spiegelbildlich (grüne Kerze, ≥ −20).
  Mehrere Setup-Tage in Folge → immer der aktuellste zählt (Entry/SL werden nachgezogen).
- Entry: Stop-Order Hoch + Puffer (Long) / Tief − Puffer (Short). Gaps ohne Auslösung ignorieren.
- SL: Tief − Puffer (Long) / Hoch + Puffer (Short). Puffer in Ticks einstellbar (Default 2), optional ‰-Minimum.
- Nachziehen laut Guide: solange Setup offen, zieht jeder weitere Downday (Long) / Upday (Short)
  Entry und SL nach – ohne erneute %R-Prüfung. Setup endet, sobald Entry erreicht wird.
- (Nur für spätere Strategie:) Ziel 1 bei CRV 1:1 → 50 % schließen, SL auf Einstand; Rest optional am BB-Mittelband nachziehen.
- Earnings: anzeigen; Signale in den 8 Tagen davor standardmäßig ausblenden.
- Risiko: 0,5–1 % (normal) bzw. 1–2 % (stark) des max. akzeptierten Depot-Drawdowns pro Trade.

## Offene Punkte / Refinement
- Setup-Verfall: laut PDF keiner, in der Praxis aber gewünscht → Hook `setupExpired()` + Input vorhanden (Default aus).
- Puffer abhängig vom Kurs (z. B. „mind. 2 Ticks und mind. x ‰“) verfeinern.
- Earnings-Filter wirkt nur auf aktuelle Signale (TradingView liefert nur das nächste Datum) – für Backtest lösen.
- Später: `strategy()`-Version für Backtests, Positionsgröße aus Risiko-Regeln.
