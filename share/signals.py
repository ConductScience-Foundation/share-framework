"""Signal definitions for the SHARE Framework.

Each SHARE bucket has 5 boolean signals worth 4 points each (20 max per bucket),
except Access (value-weighted) and Reuse (log-scaled).
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


@dataclass
class SignalMapping:
    """Maps repository-specific metadata fields to SHARE signals.

    Each mapping is a dict of signal_name -> callable that takes a record dict
    and returns a boolean (or numeric for reuse/access).

    Example:
        SignalMapping(
            stewardship={
                "has_consent": lambda r: bool(r.get("affirmedConsent")),
                "has_deidentification": lambda r: bool(r.get("affirmedDefaced")),
            }
        )
    """

    stewardship: Dict[str, Callable[[Dict[str, Any]], bool]] = field(default_factory=dict)
    harmonization: Dict[str, Callable[[Dict[str, Any]], bool]] = field(default_factory=dict)
    access: Dict[str, Callable[[Dict[str, Any]], Any]] = field(default_factory=dict)
    reuse: Dict[str, Callable[[Dict[str, Any]], Any]] = field(default_factory=dict)
    engagement: Dict[str, Callable[[Dict[str, Any]], bool]] = field(default_factory=dict)


# Default signal keys for each bucket (used when scoring from a flat dict)
STEWARDSHIP_SIGNALS = [
    "has_consent",            # S1: Consent attestation
    "has_deidentification",   # S2: De-identification documented
    "has_geographic_coverage", # S3: Geographic coverage specified
    "has_temporal_coverage",  # S4: Temporal coverage (dates)
    "has_contributors",       # S5: Contributors listed
]

HARMONIZATION_SIGNALS = [
    "has_methods",            # H1: Methods/study design documented
    "has_contributor_pids",   # H2: Contributor persistent IDs (ORCID)
    "has_org_pids",           # H3: Organization PIDs (ROR)
    "has_references",         # H4: References and links
    "has_description",        # H5: Description quality
]

ACCESS_SIGNALS = [
    "is_open_access",         # 8 pts
    "has_license",            # 4 pts
    "is_permissive_license",  # 4 pts
    "has_download_url",       # 4 pts (no embargo)
]

ACCESS_WEIGHTS = {
    "is_open_access": 8,
    "has_license": 4,
    "is_permissive_license": 4,
    "has_download_url": 4,
}

ENGAGEMENT_SIGNALS = [
    "has_related_publications",  # E1: Related publications linked
    "has_related_data",          # E2: Related datasets linked
    "has_funding",               # E3: Funding source documented
    "has_version",               # E4: Version tracking / standard compliance
    "has_keywords",              # E5: Keywords/tags present
]
