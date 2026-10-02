"""
Animation layer. SCENES is the registry: concept name -> Manim scene class.
To add a new concept later: write the scene file, then add one line here.
"""
from .mean_scene import MeanScene
from .median_scene import MedianScene
from .mode_scene import ModeScene
from .variance_scene import VarianceScene
from .std_scene import StdScene

SCENES = {
    "Mean": MeanScene,
    "Median": MedianScene,
    "Mode": ModeScene,
    "Variance": VarianceScene,
    "Standard Deviation": StdScene,
}