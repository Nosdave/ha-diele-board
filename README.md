# Diele Departure Board

Eine RGB-Dot-Matrix-Anzeige im Stil einer **Abfahrtstafel**, montiert über der Lifttür in der Diele
(Penthouse, Brüssel). Sie zeigt live:

- 🚊 **STIB** Tram + Bus (konfigurierbare Haltestellen)
- 🚆 **SNCB** Zug (stadteinwärts, per Gleis gefiltert)
- 🌤️ **Wetter** (min/max + Symbol)
- 🚗 **Waze**-Wegzeit zur Arbeit (morgens)
- 🕒 Uhr/Datum — und erweiterbar (Kalender-Reisen, Leave-Timer, Alerts …)

Realisiert mit **ESPHome** (ESP32-S3) + **Home Assistant**. Daten so **standalone wie möglich** (der ESP holt
Transit selbst), HA liefert **Fallback** und eine flexible **„Injection"-Schicht** (Präsenz, Tageszeit-Modi,
adaptive Helligkeit, Waze/Wetter, später beliebige Inhalte).

> Status: **Phase 0 (Setup & Recon)** — Plan freigegeben, Gerüst & Doku im Aufbau, noch keine Hardware bestellt.

## Hardware (Kurzfassung)

| | |
|---|---|
| Display | 192×64 px @ **P4** ≈ **76,8 × 25,6 cm** = 3× 64×64-P4-HUB75-Panels |
| Controller | **Adafruit MatrixPortal S3** (ESP32-S3, HUB75-Buchse, Level-Shifter, PSRAM) |
| Netzteil | Meanwell 5V/150W (LRS-150-5) + Power-Injection + Sicherung |
| Sensor | VEML7700 Lichtsensor (adaptive Helligkeit) |
| Finish | Eiche-Rahmen + dunkel getönte Front (passt zu Eiche/Marmor/weißer Wand) |

Vollständige Stückliste mit Links: [docs/01-hardware.md](docs/01-hardware.md) · [hardware/bom.md](hardware/bom.md)

## Architektur (Kurzfassung)

```
STIB (OAuth2) ─┐                          ┌─ Home Assistant ─────────────┐
iRail (frei) ──┤──► ESP32-S3 (Firmware) ◄─┤  scene-JSON (Wetter, Waze,    │
               │     • Uhr/Helligkeit     │  Trip, Alert, Mode, Fallback) │
               │     • eigener Fetch      │  Präsenz · Brightness · Power │
               │     • Render-Engine      └──────────────────────────────┘
               ▼
        3× 64×64 P4 HUB75 (192×64)
```

Details + Entity-Vertrag + scene-JSON-Schema: [docs/02-architecture.md](docs/02-architecture.md)

## Repo-Struktur

```
ha-diele-board/
├─ custom_components/diele_board/   HACS-Integration (manifest.json, config_flow, coordinator, entities)
├─ hacs.json                        HACS-Metadaten (Repo-Root)
├─ docs/            01-hardware · 02-architecture · 03-esphome · 04-homeassistant
│                   05-stib-irail · 06-design · roadmap
├─ esphome/         diele-board.yaml · packages/ · fonts/ · icons/ · secrets.yaml.example
└─ hardware/        bom.md · bom.csv · wiring-diagram · enclosure/
```

## Quickstart (Überblick — Details in den docs)

1. **Recon** (Phase 0): STIB-Key/Secret + Haltestellen-IDs besorgen → [docs/05-stib-irail.md](docs/05-stib-irail.md)
2. **Bestellen** (Phase 1): [hardware/bom.md](hardware/bom.md)
3. **Firmware** (Phase 2): `esphome/` flashen, Display + Fetch testen → [docs/03-esphome.md](docs/03-esphome.md)
4. **HA-Integration** (Phase 3): via **HACS** installieren (Custom-Repo) → [docs/04-homeassistant.md](docs/04-homeassistant.md)
5. **Integration & Gehäuse** (Phase 4–6) → [docs/06-design.md](docs/06-design.md)

## „Flip"-Hinweise

Dieses Repo ist so aufgebaut, dass jemand anderes es nachbauen kann: Stückliste mit Bezugsquellen,
reproduzierbare ESPHome- und HA-Konfiguration, Secrets nur als `*.example`, Doku pro Schicht. Vor einer
Veröffentlichung: Secrets prüfen, Lizenz festlegen (aktuell **TBD**), Fotos ergänzen.

## Abgrenzung

Das bestehende „transit"-HTML-Dashboard in HA ist **keine** Abhängigkeit dieses Projekts — es dient nur als
Lernquelle (Key/IDs). Dessen Überführung in eine echte HA-Integration ist ein **separates** Projekt.
