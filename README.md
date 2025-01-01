# MT4Bridge

MT4Bridge is a Python package that facilitates communication between Python applications and MetaTrader 4 (MT4) using ZeroMQ. It allows fetching historical data, current tick information, data across all timeframes, and indicator values from MT4's Expert Advisor (EA).

## Features

- **Fetch Historical Data**: Retrieve candlestick/bar data for any symbol and timeframe.
- **Current Tick Information**: Get real-time Bid, Ask, Last price, Volume, and Time data.
- **All Timeframes**: Obtain the latest data across multiple timeframes in a single request.
- **Indicator Values**: Fetch indicator data like Moving Average (MA).

## Installation

You can install MT4Bridge using `pip`:

```bash
pip install mt4bridge
```

## Building a new release

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

python setup.py sdist bdist_wheel
```
