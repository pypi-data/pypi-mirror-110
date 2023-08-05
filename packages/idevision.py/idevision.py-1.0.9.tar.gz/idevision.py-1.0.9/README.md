# idevision.py

## Installation

Installation is simple!

```python
# Stable version

pip install -U idevision.py

# Development version

pip install -U git+https://github.com/isaa-ctaylor/idevision.py
```

## Examples

```python
# Sync

from idevision import sync_client

TOKEN = "" # Optional token

client = sync_client(TOKEN)

print(client.sphinxrtfm("https://docs.aiohttp.org/en/stable/", "ClientSession"))
```

```python
# Async

from idevision import async_client

TOKEN = "" # Optional token

client = async_client(TOKEN)

print(await client.sphinxrtfm("https://docs.aiohttp.org/en/stable/", "ClientSession"))
```

