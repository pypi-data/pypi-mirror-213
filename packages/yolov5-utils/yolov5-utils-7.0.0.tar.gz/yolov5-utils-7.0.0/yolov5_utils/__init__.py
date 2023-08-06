import os
import sys
sys.path.append(os.path.dirname(__file__)+'/yolov5')

from .helpers import YOLOv5
from .helpers import load_model as load

__version__ = "7.0.0"
