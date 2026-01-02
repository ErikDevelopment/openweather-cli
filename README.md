# 🌦️ OpenWeather CLI

A lightweight **Python CLI client** for fetching **current weather** and **forecast summaries**
using the **OpenWeather API**.

---

## ✨ Features

- **Current weather** by city
- **Forecast summary** (daily min/max, condition, avg wind)
- Supports **units** (`metric`, `imperial`, `standard`) + **language**
- Optional **raw JSON output** (`--json`)
- Config via **ENV** or **config.yaml**
- Tests with mocks (CI-friendly)

---

## 📦 Installation

```bash
git clone https://github.com/your-username/openweather-cli.git
cd openweather-cli

python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .

```
Kein Problem 👍
Hier ist **alles sauber, übersichtlich und GitHub-konform neu formatiert**, **direkt im Chat**, sodass du es **einfach markieren & weiterbearbeiten** kannst.

---

## 🔑 API Key Setup

### Option A: Environment variable (recommended)

```bash
export OPENWEATHER_API_KEY="YOUR_KEY"
```

### Option B: config.yaml

Create `config.yaml` in the project root **or**
`~/.config/openweather-cli/config.yaml`

```yaml
api_key: YOUR_KEY
units: metric
lang: en
timeout: 8
```

---

## 🧑‍💻 Usage

### Current weather

```bash
weather current berlin
```

### With country code

```bash
weather current berlin --country DE
```

### Raw JSON output

```bash
weather --json current berlin
```

---

### Forecast (daily summary)

```bash
weather forecast berlin --days 3
```

---

## ⚙️ Options

### Global options

* `--config PATH` – Path to `config.yaml`
* `--units metric | imperial | standard`
* `--lang en | de | ...`
* `--timeout SECONDS`
* `--json` – Output raw JSON

---

## 🧪 Running Tests

```bash
pip install pytest
pytest
```
---
## 📄 License

MIT

---

## ⚡ Quickstart

```bash
pip install -r requirements.txt
pip install -e .
export OPENWEATHER_API_KEY="DEIN_KEY"
weather current berlin
``
