"""SHARE Score Engine — computes 5-bucket SHARE scores for any dataset.

Scoring formula:
  S (Stewardship):   5 signals x 4 pts = 20 max
  H (Harmonization): 5 signals x 4 pts = 20 max
  A (Access):        value-weighted     = 20 max
  R (Reuse):         log-scaled         = 20 max
  E (Engagement):    5 signals x 4 pts  = 20 max
  Total SHARE = S + H + A + R + E (0-100)
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .signals import (
    ACCESS_SIGNALS,
    ACCESS_WEIGHTS,
    ENGAGEMENT_SIGNALS,
    HARMONIZATION_SIGNALS,
    STEWARDSHIP_SIGNALS,
    SignalMapping,
)


@dataclass
class SHAREResult:
    """Result of scoring a single dataset."""

    S: float  # Stewardship (0-20)
    H: float  # Harmonization (0-20)
    A: float  # Access (0-20)
    R: float  # Reuse (0-20)
    E: float  # Engagement (0-20)
    total: float  # Sum (0-100)

    def __repr__(self) -> str:
        return (
            f"SHAREResult(S={self.S}, H={self.H}, A={self.A}, "
            f"R={self.R}, E={self.E}, total={self.total})"
        )

    def as_dict(self) -> Dict[str, float]:
        return {
            "S": self.S, "H": self.H, "A": self.A,
            "R": self.R, "E": self.E, "total": self.total,
        }

    @property
    def non_reuse_score(self) -> float:
        """Deposit-time score (excludes outcome-based Reuse bucket)."""
        return self.S + self.H + self.A + self.E


class SHAREScorer:
    """Scores datasets using the SHARE Framework.

    Can operate in two modes:
    1. Flat dict mode (default): Pass a dict with standard signal keys
       (e.g., {"has_consent": True, "citation_count": 42})
    2. Mapping mode: Provide a SignalMapping to translate repository-specific
       metadata into SHARE signals.
    """

    # Log base for reuse scaling: 10,000 reuse events = 20 points
    REUSE_LOG_BASE = 10_000

    def __init__(self, mapping: Optional[SignalMapping] = None):
        self.mapping = mapping

    def score(self, record: Dict[str, Any]) -> SHAREResult:
        """Score a dataset record.

        Args:
            record: Dict of metadata. If no SignalMapping was provided,
                    expects standard SHARE signal keys (has_consent, etc.)
                    plus optional numeric fields (citation_count, download_count).

        Returns:
            SHAREResult with per-bucket and total scores.
        """
        if self.mapping:
            return self._score_with_mapping(record)
        return self._score_flat(record)

    def score_record(self, record: Dict[str, Any]) -> SHAREResult:
        """Alias for score()."""
        return self.score(record)

    def score_batch(self, records: List[Dict[str, Any]]) -> List[SHAREResult]:
        """Score multiple records."""
        return [self.score(r) for r in records]

    def compute_s_index(self, results: List[SHAREResult]) -> int:
        """Compute the S-Index from a list of SHARE results.

        S-Index = max(k) where the researcher has k datasets
        with SHARE score >= k.
        """
        scores = sorted([r.total for r in results], reverse=True)
        s_index = 0
        for i, score in enumerate(scores):
            if score >= (i + 1):
                s_index = i + 1
            else:
                break
        return s_index

    # --- Internal scoring methods ---

    def _score_flat(self, record: Dict[str, Any]) -> SHAREResult:
        """Score from a flat dict with standard signal keys."""
        S = self._score_boolean_bucket(record, STEWARDSHIP_SIGNALS)
        H = self._score_boolean_bucket(record, HARMONIZATION_SIGNALS)
        A = self._score_access(record)
        R = self._score_reuse(record)
        E = self._score_boolean_bucket(record, ENGAGEMENT_SIGNALS)
        total = round(S + H + A + R + E, 1)
        return SHAREResult(S=S, H=H, A=A, R=R, E=E, total=total)

    def _score_with_mapping(self, record: Dict[str, Any]) -> SHAREResult:
        """Score using a SignalMapping to extract signals from raw metadata."""
        m = self.mapping

        # Stewardship
        s_signals = [fn(record) for fn in m.stewardship.values()] if m.stewardship else []
        S = 4 * sum(bool(s) for s in s_signals)

        # Harmonization
        h_signals = [fn(record) for fn in m.harmonization.values()] if m.harmonization else []
        H = 4 * sum(bool(s) for s in h_signals)

        # Access — mapping functions should return booleans for standard access signals
        if m.access:
            a_total = 0
            for key, fn in m.access.items():
                weight = ACCESS_WEIGHTS.get(key, 4)
                if fn(record):
                    a_total += weight
            A = min(20, a_total)
        else:
            A = 0

        # Reuse — mapping should have a "reuse_count" function returning a number
        if m.reuse and "reuse_count" in m.reuse:
            count = m.reuse["reuse_count"](record) or 0
            R = self._log_scale_reuse(count)
        else:
            R = 0.0

        # Engagement
        e_signals = [fn(record) for fn in m.engagement.values()] if m.engagement else []
        E = 4 * sum(bool(s) for s in e_signals)

        total = round(S + H + A + R + E, 1)
        return SHAREResult(S=S, H=H, A=A, R=R, E=E, total=total)

    @staticmethod
    def _score_boolean_bucket(record: Dict[str, Any], signals: List[str]) -> int:
        """Score a bucket with 5 boolean signals x 4 pts each."""
        return 4 * sum(1 for sig in signals if record.get(sig))

    @staticmethod
    def _score_access(record: Dict[str, Any]) -> int:
        """Score the Access bucket (value-weighted, 20 max)."""
        total = 0
        for sig in ACCESS_SIGNALS:
            if record.get(sig):
                total += ACCESS_WEIGHTS[sig]
        return min(20, total)

    def _score_reuse(self, record: Dict[str, Any]) -> float:
        """Score the Reuse bucket (log-scaled, 20 max)."""
        count = (
            (record.get("citation_count") or 0)
            + (record.get("download_count") or 0)
            + (record.get("derived_count") or 0)
        )
        return self._log_scale_reuse(count)

    @classmethod
    def _log_scale_reuse(cls, count: int) -> float:
        """Log-scale reuse count to 0-20 range."""
        if count <= 0:
            return 0.0
        return min(20.0, round(
            20.0 * math.log10(count + 1) / math.log10(cls.REUSE_LOG_BASE), 1
        ))
