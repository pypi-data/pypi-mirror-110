"""init.py for processing module."""

__author__ = "Jonas Van Der Donckt, Emiel Deprost, Jeroen Van Der Donckt"

from .logger import get_processor_logs
from .series_pipeline import SeriesPipeline
from .series_pipeline_sk import SKSeriesPipeline
from .series_processor import SeriesProcessor, dataframe_func
from .. import __pdoc__

__pdoc__['SeriesProcessor.__call__'] = True

__all__ = [
    "dataframe_func",
    "SeriesProcessor",
    "SeriesPipeline",
    "SKSeriesPipeline",
    "get_processor_logs",
]
