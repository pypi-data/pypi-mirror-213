# WignerSymbol-pybind11

Python bindings for [0382/WignerSymbol](https://github.com/0382/WignerSymbol).

## Example

```python
import WignerSymbol as ws
ws.init(20, "Jmax", 3)
ws.CG(1,1,2,-1,1,0) # 1/\sqrt(2)
```