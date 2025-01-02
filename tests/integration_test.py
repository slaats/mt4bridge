import unittest
from mt4bridge import MT4Bridge


class TestMT4BridgeIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bridge = MT4Bridge(
            "tcp://localhost:5555"
        )  # Ensure the address matches the EA setup

    @classmethod
    def tearDownClass(cls):
        cls.bridge.close()

    def test_get_historical_data(self):
        result = self.bridge.get_historical_data("EURUSD", "H1", 10)
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for historical data."
        )
        if result:
            self.assertIsInstance(result[0], dict, "Each bar should be a dictionary.")

    def test_get_current_tick(self):
        result = self.bridge.get_current_tick("EURUSD")
        self.assertIsInstance(
            result, dict, "Expected a dictionary for current tick data."
        )
        self.assertIn("bid", result, "Current tick data should include 'bid'.")
        self.assertIn("ask", result, "Current tick data should include 'ask'.")

    def test_get_all_timeframes(self):
        result = self.bridge.get_all_timeframes("EURUSD.a")
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for all timeframes."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each timeframe data should be a dictionary."
            )

    def test_get_indicator_sma(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "SMA", "14", 10)
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for SMA indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each SMA indicator value should be a dictionary."
            )

    def test_get_indicator_ema(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "EMA", "14", 10)
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for EMA indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each EMA indicator value should be a dictionary."
            )

    def test_get_indicator_macd(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "MACD", "12,26,9", 10)
        if result is None or (isinstance(result, dict) and "error" in result):
            self.skipTest("MACD indicator not supported by the EA.")
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for MACD indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each MACD indicator value should be a dictionary."
            )

    def test_get_indicator_rsi(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "RSI", "14", 10)
        if result is None or (isinstance(result, dict) and "error" in result):
            self.skipTest("RSI indicator not supported by the EA.")
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for RSI indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each RSI indicator value should be a dictionary."
            )

    def test_get_indicator_roc(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "ROC", "14", 10)
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for ROC indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each ROC indicator value should be a dictionary."
            )

    def test_get_indicator_atr(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "ATR", "14", 10)
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for ATR indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each ATR indicator value should be a dictionary."
            )

    def test_get_indicator_vwap(self):
        result = self.bridge.get_indicator("EURUSD", "H1", "VWAP", "", 10)
        self.assertIsInstance(
            result, list, "Expected a list of dictionaries for VWAP indicator data."
        )
        if result:
            self.assertIsInstance(
                result[0], dict, "Each VWAP indicator value should be a dictionary."
            )


if __name__ == "__main__":
    unittest.main()
