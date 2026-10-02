"""
Renderer: scene class + data  ->  MP4 file in the generated/ folder.

Same scene + same data + same quality = same file name, so a video
that was already made is reused instead of rendered again.
"""

import hashlib
import shutil
import tempfile
import threading
from pathlib import Path

from manim import tempconfig

GENERATED_DIR = Path(__file__).resolve().parent.parent / "generated"
_lock = threading.Lock()        # Manim settings are global -> render one video at a time

QUALITIES = {"Low (fast)": "low_quality", "Medium": "medium_quality", "High (slow)": "high_quality"}


def video_path(scene_cls, data, quality):
    """Build a unique file name, e.g. generated/MeanScene_low_quality_3f9a1c2b.mp4"""
    key = ",".join(str(float(v)) for v in data)
    short_hash = hashlib.md5(key.encode()).hexdigest()[:8]
    return GENERATED_DIR / f"{scene_cls.__name__}_{quality}_{short_hash}.mp4"


def render_scene(scene_cls, data, quality="low_quality"):
    """Return the path of the MP4 for this scene + data (renders it only if missing)."""
    target = video_path(scene_cls, data, quality)
    if target.exists():
        return target                                # already made earlier -> reuse

    GENERATED_DIR.mkdir(exist_ok=True)
    with _lock, tempfile.TemporaryDirectory() as tmp:
        settings = {
            "quality": quality,
            "media_dir": tmp,                        # Manim's working files go to a temp folder
            "disable_caching": True,
            "verbosity": "WARNING",
            "progress_bar": "none",
        }
        with tempconfig(settings):
            scene = scene_cls(data=data)
            scene.render()
            shutil.copy(scene.renderer.file_writer.movie_file_path, target)
    return target
