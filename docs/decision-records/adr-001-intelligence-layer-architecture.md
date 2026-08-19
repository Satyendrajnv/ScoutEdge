# ADR 001: Decoupled Intelligence Layer Architecture

- **Status**: Approved
- **Date**: 2026-08-19
- **Author**: Engineering Team

---

## Context

Sports performance software historically bundles data storage, statistical visualization, and recruitment evaluation into monolithic applications. This coupling creates several failure modes:
1. Fragmented data sources (video vs stat providers) cannot be easily unified.
2. Analytics dashboards report raw statistics without contextual intelligence or explainability.
3. Decision-makers lack confidence in "black-box" predictive algorithms.

---

## Decision

We decouple the ScoutEdge system into three distinct boundaries:
1. **System of Record**: Ingestion of raw signals without imposing domain logic.
2. **System of Intelligence**: Modular, domain-focused engines (SE-R™, PGI™, EdgeCare™, Live Resume™) calculating normalized metrics and growth models.
3. **System of Decision**: Explainable synthesis layer translating intelligence into actionable recruitment and talent evaluation recommendations.

---

## Consequences

### Positive
- **Modularity**: Individual engines (e.g., SE-R™ or EdgeCare™) can be updated or swapped without disrupting data ingestion or decision UI.
- **Explainability**: Every decision output is backed by traceable sub-system evidence.
- **Security & IP Protection**: Core engine algorithms and proprietary models remain isolated behind strict API abstractions.

### Negative / Trade-offs
- Increased initial architectural complexity due to strict contract definitions between layers.
