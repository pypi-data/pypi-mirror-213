import cv2
import numpy as np

def raw2opencv(raw):
    """raw to opencv

    Args:
        raw (_type_): _description_

    Returns:
        _type_: _description_
    """
    return cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)

