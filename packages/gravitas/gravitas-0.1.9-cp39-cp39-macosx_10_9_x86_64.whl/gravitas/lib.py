import numpy as np
from ._grav import _grav

_SUPPORTED_MODELS = {'EGM96': 360, 'GRGM360': 360, "MRO120F": 120}
_MAX_PTS = int(1e5)

def acceleration(position_ecef: np.ndarray, max_order: int, use_model: str = "EGM96") -> np.ndarray:
    if use_model not in _SUPPORTED_MODELS:
        raise NotImplementedError(f"Model {use_model} is not supported, it must be in: {', '._SUPPORTED_MODELS.keys()}")
    if _SUPPORTED_MODELS[use_model] < max_order:
        raise ValueError(f"The {use_model} model has coefficients to a maximum order of {_SUPPORTED_MODELS[use_model]}, {max_order} input")
    if position_ecef.shape[0] > _MAX_PTS:
        raise ValueError(f"Currently, gravitas is limited to 1e5 points per acceleration() call ({position_ecef.shape[0]} provided)")

    res = np.array(_grav(position_ecef, max_order, use_model)).reshape((-1,3))
    return res

