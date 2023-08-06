# Implementation of napari hooks according to
# https://napari.org/docs/dev/plugins/for_plugin_developers.html#plugins-hook-spec
from functools import partial
from pathlib import Path

from napari_plugin_engine import napari_hook_implementation

from ._categories import CATEGORIES
from ._gui import Assistant
from ._gui._category_widget import make_gui_for_category
from ._statistics_of_labeled_pixels import statistics_of_labeled_pixels

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [Assistant] + [
        (partial(make_gui_for_category, category), {"name": name})
        for name, category in CATEGORIES.items()
    ]


@napari_hook_implementation
def napari_provide_sample_data():
    data = Path(__file__).parent / "data"
    return {
        "Lund": data / "Lund_000500_resampled-cropped.tif",
        "CalibZAPW": data / "CalibZAPWfixed_000154_max-16.tif",
        "Sonneberg": data / "Sonneberg100_Resampled_RotY-40_MaxZ.tif",
    }


@napari_hook_implementation
def napari_experimental_provide_function():
    return [statistics_of_labeled_pixels]
