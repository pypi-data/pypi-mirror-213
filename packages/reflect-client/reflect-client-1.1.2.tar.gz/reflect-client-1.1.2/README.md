# Reflect API client for Python

![Maintenance](https://img.shields.io/maintenance/yes/2023)
![github](https://img.shields.io/github/v/release/victorwesterlund/reflect-client-python)
![pypi](https://img.shields.io/pypi/v/reflect-client)

Make requests to an API built using the [Reflect API](https://github.com/VictorWesterlund/reflect) framework over HTTP or UNIX sockets.

---

Make a request with `Client.call()`. It will always return the response as a tuple of length 2.
- The first value is the HTTP-equivalent response code.
- The second value is the response body

```python
client = Client("<API URL or path to UNIX socket>", "<Optional API key>");

client.call("foo", Method.GET) # (tuple) (200, "bar")
client.call("foo", Method.POST, {
  "hello": "world
}) # (tuple) (201, "Created")

# etc..
```

## How to use

Requires Python 3 or newer, and of course a Reflect API endpoint.

1. **Install with pip**

   ```
   pip3 install reflect-client
   ```
   
2. **Initialize the module**

   ```python
   from reflect_client import Client 
   
   client = Client("<API URL or path to UNIX socket>", "<Optional API key>");
   ```
   
3. **Make API request**

   Use the `call()` method to perform a request
   
   ```python
   client.call("foo?bar=baz", Method.GET);
   ```
   
   Argument index|Type|Required|Description
   --|--|--|--
   0|String|Yes|Fully qualified pathname and query params of the endpoint to call
   1|Method|Yes|A supported [Reflect HTTP method](https://github.com/VictorWesterlund/reflect/wiki/Supported-technologies#http-request-methods) (eg. `Method::GET`)
   2|List|No|An optional List of key and values to be sent as `Content-Type: application/json` to the endpoint
   
   The `call()` function will return an array of length 2 wil the following information
   
   Index|Type|Description
   --|--|--
   0|Int|HTTP-equivalent response code (eg. `200` or `404`)
   1|String/Array|Contains the response body as either a string, or array if the response `Content-Type` header is `application/json`
