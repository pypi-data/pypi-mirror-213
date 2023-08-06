from typing import TypeVar, Union
from enum import Enum

import json
import socket
import requests
import validators

# Allowed HTTP verbs
class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"

# Supported connection methods
class Connection(Enum):
    HTTP = 1
    AF_UNIX = 2

class Client:
    # Use this HTTP method if no method specified to call()
    HTTP_DEFAULT_METHOD = Method.GET
    # The amount of bytes to read for each chunk from socket
    SOCKET_READ_BYTES = 2048

    # Bind current class name to a variable we can reference elsewhere in the class
    # without having to type the name of the class each time
    #__CLASS__ = TypeVar("__CLASS__", bound="Client")

    def __init__(self, endpoint: str, key: str = None, con: Connection = None, https_peer_verify: bool = True):
        self._con = con if isinstance(con, Connection) else self.resolve_connection(endpoint)
        self._endpoint = endpoint
        self._key = key

        if (self._con == Connection.AF_UNIX):
            # Connect to Reflect UNIX socket
            self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._socket.connect(endpoint)
        elif (self._con == Connection.HTTP):
            # Append tailing "/" for HTTP if absent
            self._endpoint = self._endpoint if self._endpoint[-1] == "/" else self._endpoint + "/"
            # Flag which enables or disables SSL peer validation (for self-signed certificates)
            self._https_peer_verify = https_peer_verify

    # Close socket connection when class instance removed
    def __del__(self):
        # Close socket if connected
        if (self._con == Connection.AF_UNIX):
            self._socket.close()

    # Resolve connection type from endpoint string.
    # If the string is a valid URL we will treat it as HTTP otherwise we will assume it's a path on disk to a UNIX socket file.
    def resolve_connection(self, endpoint: str) -> Connection:
        return Connection.HTTP if validators.url(endpoint) else Connection.AF_UNIX

    # Check if provided "method" is an instance of the Method enum. Else return default
    def resolve_method(self, method: Union[Method, str, None]) -> Method:
        return method if isinstance(method, Method) else __class__.HTTP_DEFAULT_METHOD

    # Construct list of headers to send with HTTP request
    def http_headers(self) -> list:
        headers = {
            "Content-Type": "application/json"
        }

        # Append Authorization header if API key is provided
        if (self._key):
            headers["Authorization"] = f"Bearer {self._key}"

        return headers

    # Make request and return response over HTTP
    def http_call(self, endpoint: str, method: Method, payload: list = None) -> tuple:
        # Remove leading "/" if present, as it's already present in self._endpoint
        endpoint = endpoint if endpoint[-1] != "/" else endpoint[:-1]
        
        resp = requests.request(method.name, self._endpoint + endpoint, verify=self._https_peer_verify, headers=self.http_headers(), data=json.dumps(payload))
        # Return response as tuple of response code and response body as decoded JSON (mixed)
        return (resp.status_code, json.loads(resp.text))

    def socket_txn(self, endpoint: str, method: Union[Method, str] = None, payload: list = None) -> tuple:
        data = f'["{endpoint}","{method.name}","{json.dumps(payload)}"]'
        tx = self._socket.sendall(b'["order","GET",""]')
        rx = self._socket.recv(__class__.SOCKET_READ_BYTES)

        return tuple(json.loads(rx))

    def call(self, endpoint: str, method: Union[Method, str] = None, payload: list = None) -> tuple:
        # Get default method if not provided
        method = self.resolve_method(method)

        # Call endpoint via UNIX socket
        if (self._con == Connection.AF_UNIX):
            return self.socket_txn(endpoint, method, payload)

        # Call endpoint over HTTP
        return self.http_call(endpoint, method, payload)
