"""Example: Compute a researcher's S-Index from their datasets."""

from share import SHAREScorer

scorer = SHAREScorer()

# A researcher with 5 datasets of varying quality
researcher_datasets = [
    {  # Dataset 1: Excellent sharing practices
        "has_consent": True, "has_deidentification": True,
        "has_temporal_coverage": True, "has_contributors": True,
        "has_methods": True, "has_contributor_pids": True,
        "has_references": True, "has_description": True,
        "is_open_access": True, "has_license": True,
        "is_permissive_license": True, "has_download_url": True,
        "citation_count": 200,
        "has_related_publications": True, "has_funding": True,
        "has_version": True, "has_keywords": True,
    },
    {  # Dataset 2: Good but less reuse
        "has_consent": True, "has_deidentification": True,
        "has_temporal_coverage": True, "has_contributors": True,
        "has_methods": True, "has_description": True,
        "is_open_access": True, "has_license": True,
        "is_permissive_license": True, "has_download_url": True,
        "citation_count": 15,
        "has_related_publications": True, "has_funding": True,
        "has_keywords": True,
    },
    {  # Dataset 3: Minimal metadata
        "has_contributors": True,
        "is_open_access": True, "has_license": True,
        "has_download_url": True,
        "citation_count": 3,
        "has_keywords": True,
    },
    {  # Dataset 4: Well-documented but new (no reuse yet)
        "has_consent": True, "has_temporal_coverage": True,
        "has_contributors": True, "has_methods": True,
        "has_description": True, "has_references": True,
        "is_open_access": True, "has_license": True,
        "is_permissive_license": True, "has_download_url": True,
        "citation_count": 0,
        "has_related_publications": True, "has_funding": True,
        "has_version": True, "has_keywords": True,
    },
    {  # Dataset 5: Bare minimum deposit
        "has_contributors": True,
        "is_open_access": True,
        "citation_count": 0,
    },
]

# Score each dataset
results = scorer.score_batch(researcher_datasets)

print("Dataset Scores:")
for i, result in enumerate(results, 1):
    print(f"  Dataset {i}: {result.total}")

# Compute S-Index
s_index = scorer.compute_s_index(results)
print(f"\nS-Index: {s_index}")
print(f"(Researcher has {s_index} datasets with SHARE score >= {s_index})")
