# rct-modelpool

## Installation
You can git install `rctmodelpool` via `pip`:

```bash
pip install git+https://github.com/rct-ai/rct-modelpool
```

## Usage
You can import the *rctmodelpool.modelpool* from the package like so:

### `sync_model`
```python
import rctmodelpool.modelpool

path = rctmodelpool.modelpool.sync_model("rcthub://CPM.csv")
print(path)

```
