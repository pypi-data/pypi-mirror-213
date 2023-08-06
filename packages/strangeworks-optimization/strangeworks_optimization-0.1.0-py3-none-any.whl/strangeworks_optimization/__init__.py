import importlib.metadata

from .optimization import OptimizationJob, StrangeworksOptimization  # noqa

__version__ = importlib.metadata.version("strangeworks-optimization")
