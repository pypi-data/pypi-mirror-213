# TurboREST

TurboREST is a REST API framework for Python 3.7+.

## Installation

```bash
pip install turborest
```

## Usage

```python
from turborest import Client

def main():
    auth = ("Bearer", "xyz")
    client = Client(format="json", auth=auth)
    client.get("https://api.bytesentinel.io/test")
```

## License

### MIT License

```text
MIT License

TurboREST - A REST API framework for Python 3.7+.


...
    
```
