# Reproducibility

The SHARE Framework is designed for complete reproducibility. All components are open.

## Components

| Component | Repository | What it contains |
|-----------|-----------|-----------------|
| **Algorithm** | [share-framework](https://github.com/ConductScience-Foundation/share-framework) (this repo) | Scoring logic, signal definitions, S-Index calculation |
| **Pledges** | [share-pledges](https://github.com/ConductScience-Foundation/share-pledges) | Signal mappings for 9 repositories (JSON) |
| **Implementation** | [share-implementation](https://github.com/ConductScience-Foundation/share-implementation) | Scoring scripts, validation code, pre-computed results |
| **Live Platform** | [sharescore.org](https://sharescore.org) | 76.4M scored datasets, public REST API (no auth required) |

## How to Reproduce

1. **Install the algorithm**: `pip install share-framework`
2. **Get the signal mappings**: Clone [share-pledges](https://github.com/ConductScience-Foundation/share-pledges)
3. **Run the scoring engine**: See [share-implementation](https://github.com/ConductScience-Foundation/share-implementation) for scripts and instructions
4. **Verify against live data**: Query [api.sharescore.org](https://api.sharescore.org/docs) to compare scores

Full step-by-step guide: [share-implementation/REPRODUCIBILITY.md](https://github.com/ConductScience-Foundation/share-implementation/blob/main/REPRODUCIBILITY.md)

## Data Access

All 9 upstream data repositories are publicly accessible. No special credentials required. See [share-implementation/data/README.md](https://github.com/ConductScience-Foundation/share-implementation/blob/main/data/README.md) for API endpoints.

## Validation

The SHARE score's predictive validity has been validated on two Zenodo cohorts:

- Citation prediction OR: 3.0x per 10-point increase (95% CI: 2.87-3.18; Zenodo 2016 cohort, n=48,771)
- Derivative prediction OR: 5.73x per 10-point increase (95% CI: 4.97-6.61; Zenodo 2017-2022 cohort, n=183,872)
- Known-groups validity confirmed across 9 repositories

Validation scripts and pre-computed results: [share-implementation/validation/](https://github.com/ConductScience-Foundation/share-implementation/tree/main/validation)
