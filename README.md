# AKJ2.0 – Trend & Setup Detector

TradingView-Indikator (Pine Script v6) nach dem „Aktien-Kann-Jeder Strategie-Guide“.
Er dient dazu, Aktien schnell auf mögliche Setups zu scannen. Er simuliert keine Trades und
führt keine Orders aus.

**Installation:** Inhalt von [`akj_setup_indikator.pine`](akj_setup_indikator.pine) in den
Pine-Editor von TradingView kopieren → „Zum Chart hinzufügen“. Gedacht für Daily-Charts
(Setups) und Weekly-Charts (Weekly-Trigger).

**Anzeige im Chart**

- Bollinger-Bänder 10 / 1
- Hintergrund: türkis = Long-Trigger, pink = Short-Trigger (Farben einstellbar)
- Marker **L** (grün, unter der Kerze) / **S** (rot, darüber) auf der Signalkerze
- Blaue Linie = Entry (Stop-Order), rote Linie = Stop-Loss, solange das Setup offen ist
- **Aktuelles Setup** (offen auf der jüngsten Kerze): Hintergrund leuchtend blau (Long) bzw. violett (Short)
  ab der ersten Signalkerze plus Label mit Entry und SL rechts der Kerze – per Setting abschaltbar
- Grauer Hintergrund = Earnings-Sperrfenster (x Tage vorher bis einschließlich Earnings-Tag/-Woche).
  Den Earnings-Termin selbst zeigt TradingView mit seinem eigenen „E“-Symbol an.

## Trendzustand je Timeframe

Der Zustand wird für Weekly und Daily getrennt nach derselben Regel bestimmt. Er bleibt
bestehen, bis der Trigger in die Gegenrichtung kommt. Der Trigger steht erst mit dem Close
der zweiten Kerze fest, deshalb gilt das neue Regime **ab der Kerze danach**.

```mermaid
stateDiagram-v2
    [*] --> Neutral
    Neutral --> Kauf: 2x Close über oberem BB
    Neutral --> Verkauf: 2x Close unter unterem BB
    Kauf --> Verkauf: 2x Close unter unterem BB
    Verkauf --> Kauf: 2x Close über oberem BB
```

## Ablauf je Kerze

```mermaid
flowchart TD
    Start(["Neue Kerze"]) --> TF{"Chart-Timeframe?"}
    TF -- "Weekly" --> W1["Weekly-Zustand bis Vorwoche"]
    W1 --> W2["Hintergrund nach<br/>Weekly-Zustand"]
    W2 --> Ende(["Fertig"])
    TF -- "anderer" --> X["Nur Bollinger-Bänder"]
    X --> Ende

    TF -- "Daily" --> D1["Weekly-Zustand der letzten<br/>abgeschlossenen Woche"]
    D1 --> D2["Daily-Zustand bis gestern"]
    D2 --> T{"Weekly und Daily?"}
    T -- "beide Kauf" --> TL["Long-Trigger<br/>Hintergrund grün"]
    T -- "beide Verkauf" --> TS["Short-Trigger<br/>Hintergrund orange"]
    T -- "sonst" --> TN["Kein Trigger<br/>kein Hintergrund"]
    TL --> O
    TS --> O
    TN --> O

    O{"Setup offen?"} -- "nein" --> K
    O -- "ja" --> C{"Trigger weg, Earnings in<br/>≤ 8 Tagen oder Setup verfallen?"}
    C -- "ja" --> CX["Setup löschen"]
    CX --> K
    C -- "nein" --> F{"Entry heute erreicht?<br/>Long: Hoch ≥ Entry<br/>Short: Tief ≤ Entry"}
    F -- "ja" --> FX["Setup endet:<br/>Entry ausgelöst"]
    FX --> Ende
    F -- "nein" --> K

    K{"Kerze abgeschlossen?"} -- "nein" --> Ende
    K -- "ja" --> M{"Setup noch offen?"}
    M -- "ja" --> MV{"Neuer Downday (Long)<br/>bzw. Upday (Short)?"}
    MV -- "ja" --> MVX["Entry auf diese Kerze nachziehen,<br/>SL nur, wenn Tief tiefer (Long)<br/>bzw. Hoch höher (Short), Marker"]
    MV -- "nein" --> SLX["Entry bleibt; SL nachziehen, wenn<br/>Tief tiefer (Long) bzw. Hoch höher (Short)"]
    SLX --> Ende
    MVX --> Ende
    M -- "nein" --> NS{"Trigger aktiv, keine Earnings und<br/>Long: rote Kerze, %R ≤ −80<br/>Short: grüne Kerze, %R ≥ −20?"}
    NS -- "ja" --> NSX["Neues Setup<br/>Long: Entry = Hoch + Puffer, SL = Tief − Puffer<br/>Short: Entry = Tief − Puffer, SL = Hoch + Puffer<br/>Marker L / S"]
    NS -- "nein" --> Ende
    NSX --> Ende
```

**Hinweise**

- Puffer = 2 Ticks (einstellbar), optional mindestens x ‰ vom Kurs.
- Der SL liegt immer unter dem tiefsten Tief (Long) bzw. über dem höchsten Hoch (Short) seit der
  ersten Signalkerze – auch Kerzen ohne Signal ziehen ihn nach. Er wandert nie zurück in die Bewegung.
- Gaps, die den Entry nicht erreichen, werden ignoriert. Das Setup bleibt dann offen.
- Der Abbruch wird vor dem Entry geprüft, weil Trendwechsel, Earnings und Verfall schon zur
  Eröffnung bekannt sind. Man würde die Order dann vor Handelsbeginn löschen.
- Signale und Trigger entstehen nur aus abgeschlossenen Kerzen.
