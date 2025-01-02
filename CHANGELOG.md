# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-02

### Added

- **Initial Release** of the `MT4Bridge` class for Python integration with MetaTrader 4 (MT4) using ZeroMQ.
  
  - **Core Functionality**:
    - Establishes communication between Python scripts and MT4 Expert Advisor (EA) via ZeroMQ's REQ/REP pattern.
    - Initializes a ZeroMQ REQ socket connected to the specified MT4 EA address.
  
  - **Features**:
    - **Send Requests**: Allows sending formatted request strings to the MT4 EA.
    - **Receive Responses**: Handles receiving and parsing JSON responses from the MT4 EA.
    - **Historical Data Retrieval**: Fetches historical candlestick/bar data for specified symbols and timeframes.
    - **Current Tick Information**: Retrieves real-time tick data including Bid, Ask, Last price, Volume, and Time for specified symbols.
    - **Multi-Timeframe Data**: Obtains the latest candlestick/bar data across all supported timeframes for a given symbol.
    - **Indicator Values**: Requests and retrieves indicator values based on configurable parameters.
  
  - **Error Handling**:
    - Comprehensive error handling for ZeroMQ connection issues, message sending/receiving failures, and JSON parsing errors.
    - Logs informative error messages to aid in troubleshooting.
  
  - **Resource Management**:
    - Provides a `close` method to gracefully terminate the ZeroMQ socket and context, ensuring proper resource cleanup.
  
  - **Documentation**:
    - Detailed docstrings for the `MT4Bridge` class and its methods, facilitating ease of use and understanding for developers.
  
  - **Dependencies**:
    - Utilizes `json`, `zmq`, and `decimal` modules for handling JSON data, ZeroMQ communication, and precise numerical operations, respectively.

### [Unreleased]
- Placeholder for future changes.

