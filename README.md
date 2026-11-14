
# Binance Connection Test

Standalone connectivity test for Binance USD-M Futures API.

## Endpoints

- `/` : Service health check
- `/test` : Binance API connectivity test

## Binance endpoint

https://fapi.binance.com/fapi/v1/exchangeInfo

No API keys or trading permissions required.

## Render configuration

Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
python app.py
