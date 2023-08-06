# wtoolzexceptions

![](https://github.com/e-k-m/wtoolzexceptions/workflows/main/badge.svg)

> wtoolzexceptions contains core exception logic for web applications

[Installation](#installation) | [Getting Up And Running](#getting-up-and-running) | [Examples](#examples) | [API](#api) | [See Also](#see-also)

wtoolzexceptions contains core exception logic for web applications. The main feature are:

- Contains error and exception classes and

- abort function.

## Installation

```bash
pip install wtoolzexceptions
```

## Getting Up and Running

```bash
nox -l
```

## Examples

```python
import flask

from wtoolzexceptions import exceptions

app = flask.Flask(__name__)

@app.errorhandler(exceptions.HTTPException)
def handle_it(e):
    res = flask.jsonify(self.to_dict())
    res.status_code = self.http_status_code
    return res

@app.route("/me")
def boom_me():
    raise exceptions.Forbidden()

# When calling /me you will now get 404 status code and JSON response
# as {"error": {"code": "XY", "message": "xy"}}.
```

## API

FIXME

## See Also

FIXME