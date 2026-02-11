"""Example: Score a single dataset using the SHARE Framework."""

from share import SHAREScorer

scorer = SHAREScorer()

# A well-documented open-access neuroscience dataset
dataset = {
    # Stewardship signals
    "has_consent": True,
    "has_deidentification": True,
    "has_geographic_coverage": False,
    "has_temporal_coverage": True,
    "has_contributors": True,
    # Harmonization signals
    "has_methods": True,
    "has_contributor_pids": True,   # Has ORCID
    "has_org_pids": False,          # No ROR
    "has_references": True,
    "has_description": True,
    # Access signals
    "is_open_access": True,
    "has_license": True,
    "is_permissive_license": True,  # CC-BY-4.0
    "has_download_url": True,
    # Reuse signals (numeric)
    "citation_count": 42,
    "download_count": 1500,
    # Engagement signals
    "has_related_publications": True,
    "has_related_data": False,
    "has_funding": True,
    "has_version": True,
    "has_keywords": True,
}

result = scorer.score(dataset)
print(f"SHARE Score: {result.total}/100")
print(f"  S (Stewardship):   {result.S}/20")
print(f"  H (Harmonization): {result.H}/20")
print(f"  A (Access):        {result.A}/20")
print(f"  R (Reuse):         {result.R}/20")
print(f"  E (Engagement):    {result.E}/20")
print(f"  Non-reuse score:   {result.non_reuse_score}/80")
