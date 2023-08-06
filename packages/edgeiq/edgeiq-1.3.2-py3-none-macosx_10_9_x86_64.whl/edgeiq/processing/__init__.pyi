from .image import *
from .object_detection import *
from .results import *
from .semantic_segmentation import *
from .image_classification import *
from .trt_plugin import *
from .libhuman_pose import *
from typing import Any, Optional

class Processor:
    funcs: Any = ...
    def __init__(self, funcs: Optional[Any] = ...) -> None: ...
    def __call__(self, data: Any, runtime_params: Optional[Any] = ...): ...
