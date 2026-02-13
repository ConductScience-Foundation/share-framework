# SHARE Framework

A universal, open metric for evaluating scientific data sharing quality.

**SHARE** scores datasets on a 0–100 scale across five dimensions:

| Bucket | Name | What it measures | Max |
|--------|------|-----------------|-----|
| **S** | Stewardship | Consent, de-identification, provenance, contributors | 20 |
| **H** | Harmonization | Standards compliance, PIDs, documentation quality | 20 |
| **A** | Access | Openness, licensing, download availability | 20 |
| **R** | Reuse | Citations, downloads, derived works (outcome signal) | 20 |
| **E** | Engagement | Related publications, funding, keywords, versioning | 20 |

## S-Index

The **S-Index** is derived from SHARE scores, analogous to the H-Index for publications:

> A researcher has an S-Index of *k* if they have *k* datasets each with a SHARE score ≥ *k*.

## Key Design Principle

SHARE separates **deposit-time signals** (S + H + A + E) from **outcome signals** (R). This means:
- New datasets get a meaningful score immediately (up to 80 points)
- Reuse metrics accumulate over time without penalizing recent deposits
- Researchers are rewarded for good data sharing *practices*, not just popularity

## Installation

```bash
pip install share-framework
```

## Quick Start

```python
from share import SHAREScorer

scorer = SHAREScorer()

# Score a dataset from its metadata
result = scorer.score({
    "has_consent": True,
    "has_deidentification": True,
    "has_temporal_coverage": True,
    "has_contributors": True,
    "has_methods": True,
    "has_contributor_pids": True,
    "has_references": True,
    "has_description": True,
    "is_open_access": True,
    "has_license": True,
    "is_permissive_license": True,
    "has_download_url": True,
    "citation_count": 42,
    "has_related_publications": True,
    "has_funding": True,
    "has_version": True,
    "has_keywords": True,
})

print(result)
# SHAREResult(S=16, H=16, A=20, R=8.1, E=16, total=76.1)
```

## Adapting to Your Repository

Each repository has different metadata fields. Create a mapping from your metadata to SHARE signals:

```python
from share import SHAREScorer, SignalMapping

# Example: mapping OpenNeuro BIDS metadata
openneuro_mapping = SignalMapping(
    stewardship={
        "has_consent": lambda r: bool(r.get("affirmedConsent")),
        "has_deidentification": lambda r: bool(r.get("affirmedDefaced")),
        "has_temporal_coverage": lambda r: r.get("publicationDate") is not None,
        "has_contributors": lambda r: bool(r.get("Authors")),
    },
    # ... define harmonization, access, engagement mappings
)

scorer = SHAREScorer(mapping=openneuro_mapping)
results = [scorer.score_record(record) for record in my_records]
```

## Scoring Details

### S — Stewardship (5 signals x 4 pts = 20 max)
| Signal | Description |
|--------|-------------|
| S1 | Consent attestation present |
| S2 | De-identification documented |
| S3 | Geographic coverage specified |
| S4 | Temporal coverage (dates) |
| S5 | Contributors listed |

### H — Harmonization (5 signals x 4 pts = 20 max)
| Signal | Description |
|--------|-------------|
| H1 | Methods / study design documented |
| H2 | Contributor persistent IDs (ORCID) |
| H3 | Organization PIDs (ROR) |
| H4 | References and links |
| H5 | Description quality / acknowledgements |

### A — Access (value-weighted, 20 max)
| Signal | Points | Description |
|--------|--------|-------------|
| Open access | 8 | Dataset is publicly accessible |
| License present | 4 | Any license specified |
| Permissive license | 4 | CC0, CC-BY, PDDL, MIT, etc. |
| No embargo / downloadable | 4 | Direct download available |

### R — Reuse (log-scaled, 20 max)
```
R = min(20, 20 * log10(reuse_count + 1) / log10(10000))
```
Where `reuse_count` combines citations, downloads, and derived works.

### E — Engagement (5 signals x 4 pts = 20 max)
| Signal | Description |
|--------|-------------|
| E1 | Related publications linked |
| E2 | Related datasets linked |
| E3 | Funding source documented |
| E4 | Version tracking / standard compliance |
| E5 | Keywords / tags present |

## Validated Repositories

The SHARE Framework has been applied to **76.4M+ datasets** across 9 repositories:

| Repository | Records | Avg SHARE | Domain |
|------------|---------|-----------|--------|
| OpenAIRE | 73.4M | 53.8 | Multi-disciplinary |
| Zenodo | 1.3M | 44.1 | General-purpose |
| SRA | 644K | 84.7 | Genomics |
| ClinicalTrials.gov | 571K | 50.3 | Clinical trials |
| GEO | 274K | 73.5 | Gene expression |
| Dryad | 109K | 45.2 | Biology |
| EDI | 47K | 56.2 | Environmental science |
| NASA | 27K | 28.6 | Earth science |
| OpenNeuro | 1,873 | 49.5 | Neuroimaging |

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for how to reproduce these results.

## Contributing

We welcome contributions! To add support for a new repository:

1. Fork this repo
2. Create a signal mapping for your repository's metadata schema
3. Add tests with sample records
4. Submit a pull request

## Citation

If you use the SHARE Framework in your research, please cite:

```
He S, He YH, Corscadden L. SHARE Framework: A Universal Metric for
Scientific Data Sharing Quality. ConductScience Foundation, 2026.
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

## Team

- **Shuhan He, MD** — Scientific Steward
- **Yijian Henry He, PhD** — Technical Steward
- **Louise Corscadden, PhD** — Community Steward

Built by [ConductScience Foundation](https://conductscience.com), a 501(c)(3) nonprofit.
