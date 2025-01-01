import json
import zmq
from decimal import Decimal


class MT4Bridge:
    """A bridge class to facilitate communication between Python and MetaTrader
    4 (MT4) using ZeroMQ.

    This class allows Python scripts to send requests to an MT4 Expert Advisor (EA) and
    receive responses. Supported operations include fetching historical data, current
    tick information, data across all timeframes, and indicator values.
    The communication follows a request-reply (REQ/REP) pattern.

    Attributes:
        address (str): The ZeroMQ address to connect to the MT4 EA's REP socket.
        context (zmq.Context): The ZeroMQ context for managing sockets.
        socket (zmq.Socket): The ZeroMQ REQ socket for sending requests.
    """

    def __init__(self, address="tcp://localhost:5555"):
        """Initializes the MT4Bridge instance by setting up a ZeroMQ REQ socket
        connected to the specified address.

        Args:
            address (str, optional): The ZeroMQ address to connect to. Defaults to
                "tcp://localhost:5555".

        Raises:
            zmq.ZMQError: If the socket fails to connect.
        """
        self.address = address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        try:
            self.socket.connect(self.address)
            print(f"[Python] Connected to MT4 EA at {self.address}")
        except zmq.ZMQError as e:
            print(f"[Error] Failed to connect to MT4 EA at {self.address}: {e}")
            raise

    def send_request(self, request_str):
        """Sends a request string to the MT4 EA and waits for a reply.

        Args:
            request_str (str): The formatted request string to send (e.g.,
                "HIST:EURUSD:H1:100").

        Returns:
            str: The raw JSON string response from the MT4 EA.

        Raises:
            zmq.ZMQError: If sending or receiving the message fails.
        """
        print(f"[Python] Sending request: {request_str}")
        try:
            self.socket.send_string(request_str)
        except zmq.ZMQError as e:
            print(f"[Error] Failed to send request: {e}")
            return ""

        try:
            reply = self.socket.recv_string()
            print(f"[Python] Received reply: {reply}")
            return reply
        except zmq.ZMQError as e:
            print(f"[Error] Failed to receive reply: {e}")
            return ""

    def get_historical_data(self, symbol="EURUSD", timeframe="H1", bars=10):
        """Requests historical candlestick/bar data for a specific symbol and
        timeframe.

        Args:
            symbol (str, optional): The trading symbol (e.g., "EURUSD", "XAUUSD.a").
                Defaults to "EURUSD".
            timeframe (str, optional): The timeframe for the bars (e.g., "M1", "H1",
                "D1"). Defaults to "H1".
            bars (int, optional): The number of historical bars to retrieve.
                Defaults to 10.

        Returns:
            list[dict] or None: A list of dictionaries containing bar data, or None
                if an error occurs.
        """
        request_str = f"HIST:{symbol}:{timeframe}:{bars}"
        reply = self.send_request(request_str)
        return self._parse_response(reply)

    def get_current_tick(self, symbol: str):
        """Requests the current tick information (Bid, Ask, Last price, Volume,
        Time) for a specific symbol.

        Args:
            symbol (str): The trading symbol (e.g., "EURUSD", "XAUUSD.a").

        Returns:
            dict or None: A dictionary containing current tick information, or None
                if an error occurs.
        """
        request = f"CURRENT:{symbol}"
        reply = self.send_request(request)
        return self._parse_response(reply)

    def get_all_timeframes(self, symbol: str):
        """Requests the latest candlestick/bar data for all supported
        timeframes for a specific symbol.

        Args:
            symbol (str): The trading symbol (e.g., "EURUSD", "XAUUSD.a").

        Returns:
            list[dict] or None: A list of dictionaries, each containing the latest bar
                data for a timeframe, or None if an error occurs.
        """
        request = f"TIMEFRAMES:{symbol}"
        reply = self.send_request(request)
        return self._parse_response(reply)

    def get_indicator(self, symbol, timeframe, indicator_name, params, bars):
        """Requests indicator values for a specific symbol, timeframe, and
        indicator configuration.

        Args:
            symbol (str): The trading symbol (e.g., "EURUSD", "XAUUSD.a").
            timeframe (str): The timeframe for the indicator (e.g., "M1", "H1", "D1").
            indicator_name (str): The name of the indicator (e.g., "MA" for Moving
                Average).
            params (str): A comma-separated string of parameters required by the
                indicator (e.g., "14,0,1,0" for MA period=14, shift=0, method=1,
                applied_price=0).
            bars (int): The number of indicator values to retrieve.

        Returns:
            list[dict] or None: A list of dictionaries containing indicator values per
                bar, or None if an error occurs.
        """
        request = f"INDICATOR:{symbol}:{timeframe}:{indicator_name}:{params}:{bars}"
        reply = self.send_request(request)
        return self._parse_response(reply)

    def _parse_response(self, reply):
        """Parses the JSON response from the MT4 EA and handles any errors.

        Args:
            reply (str): The raw JSON string received from the MT4 EA.

        Returns:
            dict or list[dict] or None: The parsed JSON data as a dictionary or list
                of dictionaries, or None if parsing fails or an error is present.
        """
        if not reply:
            print("[Error] Empty reply received from MT4 EA.")
            return None

        try:
            data = json.loads(reply, parse_float=Decimal)
        except json.JSONDecodeError:
            print("[Error] Could not parse JSON. Response:", reply)
            return None

        # Check if the response contains an error
        if isinstance(data, dict) and "error" in data:
            print(f"[Error] EA returned error: {data['error']}")
            return None

        print("[Python] Parsed JSON data:", data)
        return data

    def close(self):
        """Closes the ZeroMQ socket and terminates the context.

        It's good practice to call this method when the bridge is no
        longer needed to free up resources.
        """
        self.socket.close()
        self.context.term()
        print("[Python] Closed connection to MT4 EA.")
