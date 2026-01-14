# UC Journey Kit

A lightweight Selenium automation starter using `undetected_chromedriver` with reusable helpers for waits, clicks, and inputs.

## Features
- Reusable helpers: wait for page load, find by XPath, click, and input text
- Chrome profile support to persist sessions
- Simple example flow in `main.py`

## Requirements
- Python 3.9+
- Google Chrome installed

## Setup
```bash
python -m venv venv
```

Windows:
```bash
.\venv\Scripts\activate
```

Install dependencies:
```bash
pip install selenium undetected-chromedriver
```

## Run
```bash
python main.py
```

## Notes
- The Chrome profile directory is `chrome_profile/`.
- If you see missing import warnings, select the correct Python interpreter in your IDE.
- Update the XPath selectors in `main.py` to match your target pages.

## Roadmap
- Add configurable targets via a config file
- Add retry/backoff helpers
- Add optional headless mode

