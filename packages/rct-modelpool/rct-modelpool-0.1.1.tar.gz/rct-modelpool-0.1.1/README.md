# rct-modelpool

## Installation
You can git install `rct_modelpool` via `pip`:

```bash
pip install git+https://github.com/rct-ai/rct-modelpool
```

## Usage
You can import the *sync_model* from the package like so:

### `sync_model`
```python
from rct_modelpool.modelpool import sync_model

path = sync_model("rcthub://CPM.csv")
print(path)

```
