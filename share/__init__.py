"""SHARE Framework — A universal metric for scientific data sharing quality."""

from .scorer import SHAREScorer, SHAREResult
from .signals import SignalMapping

__version__ = "0.1.0"
__all__ = ["SHAREScorer", "SHAREResult", "SignalMapping"]
