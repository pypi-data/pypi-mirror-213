import logging

from torch_tensorrt.fx.converter_registry import (  # noqa
    CONVERTERS,
    NO_EXPLICIT_BATCH_DIM_SUPPORT,
    NO_IMPLICIT_BATCH_DIM_SUPPORT,
    tensorrt_converter,
)
from .fx2trt import TRTInterpreter, TRTInterpreterResult  # noqa
from .input_tensor_spec import InputTensorSpec  # noqa
from .lower_setting import LowerSetting  # noqa
from .lower import compile  # usort: skip  #noqa

logging.basicConfig(level=logging.INFO)
