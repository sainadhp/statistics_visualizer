from .mean_scene import MeanScene
from .median_scene import MedianScene
from .mode_scene import ModeScene

SCENES = {
    "Mean": MeanScene,
    "Median": MedianScene,
    "Mode": ModeScene
}

