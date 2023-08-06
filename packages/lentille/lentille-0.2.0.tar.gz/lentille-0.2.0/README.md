# Lentille
Library that wraps various embedders. For now it only wraps a Resnet50 model.

## Installation
``` bash
pip install lentille
```

## Example usage
``` python
from lentille import Resnet50Embedder

embedder = Resnet50Embedder.from_file(
    "resnet50-v1-12-int8.onnx" # ONNX model from: https://github.com/onnx/models/tree/main/vision/classification/resnet
)

print(embedder.classify("cat.jpg"))
```
