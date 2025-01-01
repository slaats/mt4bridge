import unittest
from unittest.mock import patch, MagicMock
from mt4bridge import MT4Bridge
import json
from decimal import Decimal


class TestMT4Bridge(unittest.TestCase):
    """
    Test cases for the MT4Bridge class using mocked ZeroMQ socket interactions.
    """

    @patch("mt4bridge.bridge.zmq.Context")
    def setUp(self, mock_zmq_context):
        """
        Set up the MT4Bridge instance with mocked ZeroMQ context and socket.
        """
        # Create a mock socket instance
        self.mock_socket = MagicMock()

        # Configure the mock context to return the mock socket
        mock_zmq_context.return_value.socket.return_value = self.mock_socket

        # Initialize MT4Bridge (uses the mocked context and socket)
        self.bridge = MT4Bridge(address="tcp://localhost:5555")

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.bridge.close()

    def test_get_historical_data_success(self):
        """
        Test fetching historical data successfully.
        """
        # Define the expected request string
        expected_request = "HIST:EURUSD.a:H1:5"

        # Define the mock reply JSON
        mock_reply = json.dumps(
            [
                {
                    "time": "2024.12.31 23:00",
                    "open": 1.02910,
                    "high": 1.03010,
                    "low": 1.02900,
                    "close": 1.02950,
                    "volume": 163,
                },
                # Add more bars as needed
            ]
        )

        # Configure the mock socket to return the mock_reply when recv_string is called
        self.mock_socket.recv_string.return_value = mock_reply

        # Call the method
        data = self.bridge.get_historical_data("EURUSD.a", "H1", 5)

        # Assert that send_string was called with the correct request
        self.mock_socket.send_string.assert_called_with(expected_request)

        # Assert that the data returned is as expected
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("time", data[0])
        self.assertIn("open", data[0])
        self.assertIn("high", data[0])
        self.assertIn("low", data[0])
        self.assertIn("close", data[0])
        self.assertIn("volume", data[0])

    def test_get_current_tick_success(self):
        """
        Test fetching current tick data successfully.
        """
        expected_request = "CURRENT:EURUSD.a"

        mock_reply = json.dumps(
            {
                "symbol": "EURUSD.a",
                "bid": 1.23456,
                "ask": 1.23478,
                "last": 1.23470,
                "volume": 123,
                "time": "2025.01.01 12:34",
            }
        )

        self.mock_socket.recv_string.return_value = mock_reply

        data = self.bridge.get_current_tick("EURUSD.a")

        self.mock_socket.send_string.assert_called_with(expected_request)

        self.assertIsInstance(data, dict)
        self.assertEqual(data.get("symbol"), "EURUSD.a")
        self.assertEqual(data.get("bid"), Decimal("1.23456"))
        self.assertEqual(data.get("ask"), Decimal("1.23478"))
        self.assertEqual(data.get("last"), Decimal("1.23470"))
        self.assertEqual(data.get("volume"), Decimal("123"))
        self.assertEqual(data.get("time"), "2025.01.01 12:34")

    def test_get_all_timeframes_success(self):
        """
        Test fetching all timeframes successfully.
        """
        expected_request = "TIMEFRAMES:EURUSD.a"

        mock_reply = json.dumps(
            [
                {
                    "tf": "M1",
                    "time": "2025.01.01 12:00",
                    "open": 1.23456,
                    "high": 1.23478,
                    "low": 1.23450,
                    "close": 1.23470,
                    "volume": 123,
                },
                {
                    "tf": "H1",
                    "time": "2025.01.01 12:00",
                    "open": 1.23460,
                    "high": 1.23500,
                    "low": 1.23440,
                    "close": 1.23480,
                    "volume": 150,
                },
                # Add more timeframes as needed
            ]
        )

        self.mock_socket.recv_string.return_value = mock_reply

        data = self.bridge.get_all_timeframes("EURUSD.a")

        self.mock_socket.send_string.assert_called_with(expected_request)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        for tf_bar in data:
            self.assertIn("tf", tf_bar)
            self.assertIn("time", tf_bar)
            self.assertIn("open", tf_bar)
            self.assertIn("high", tf_bar)
            self.assertIn("low", tf_bar)
            self.assertIn("close", tf_bar)
            self.assertIn("volume", tf_bar)

    def test_get_indicator_success(self):
        """
        Test fetching indicator data successfully.
        """
        expected_request = "INDICATOR:EURUSD.a:H1:MA:14,0,1,0:10"

        mock_reply = json.dumps(
            [
                {"tf": "H1", "shift": 0, "ma": 1.02910},
                {"tf": "H1", "shift": 1, "ma": 1.02920},
                # Add more indicator data as needed
            ]
        )

        self.mock_socket.recv_string.return_value = mock_reply

        data = self.bridge.get_indicator("EURUSD.a", "H1", "MA", "14,0,1,0", 10)

        self.mock_socket.send_string.assert_called_with(expected_request)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        for ma_bar in data:
            self.assertIn("tf", ma_bar)
            self.assertIn("shift", ma_bar)
            self.assertIn("ma", ma_bar)

    def test_send_request_empty_reply(self):
        """
        Test handling of empty reply from the EA.
        """
        expected_request = "CURRENT:EURUSD.a"

        # Configure the mock to return an empty string
        self.mock_socket.recv_string.return_value = ""

        data = self.bridge.get_current_tick("EURUSD.a")

        self.mock_socket.send_string.assert_called_with(expected_request)
        self.assertIsNone(data)

    def test_send_request_invalid_json(self):
        """
        Test handling of invalid JSON reply from the EA.
        """
        expected_request = "HIST:EURUSD.a:H1:5"

        # Configure the mock to return invalid JSON
        self.mock_socket.recv_string.return_value = "INVALID_JSON"

        data = self.bridge.get_historical_data("EURUSD.a", "H1", 5)

        self.mock_socket.send_string.assert_called_with(expected_request)
        self.assertIsNone(data)

    def test_send_request_ea_error(self):
        """
        Test handling of error messages returned by the EA.
        """
        expected_request = "INDICATOR:EURUSD.a:H1:MA:14,0,1,0:10"

        # Configure the mock to return an error JSON
        mock_reply = json.dumps({"error": "Symbol not found"})
        self.mock_socket.recv_string.return_value = mock_reply

        data = self.bridge.get_indicator("EURUSD.a", "H1", "MA", "14,0,1,0", 10)

        self.mock_socket.send_string.assert_called_with(expected_request)
        self.assertIsNone(data)


if __name__ == "__main__":
    unittest.main()
