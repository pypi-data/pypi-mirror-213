# YOLOv5 Installable Package

Packaged [ultralytics/yolov5](https://github.com/ultralytics/yolov5)

Inspired from https://github.com/fcakyon/yolov5-pip.

## Build Package
Build wheel file:
```bash
python setup.py bdist_wheel
```

### General imports
Insert `yolov5_utils.yolov5.` prefix when importing modules `models` and `utils`.
For example: 
```python
from yolov5_utils.yolov5.models.common import DetectMultiBackend
```


## Authors
**Msclock** - msclock@qq.com  - [Github account](https://github.com/msclock)