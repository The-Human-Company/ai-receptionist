# KB Query Strategies

This document details strategies for querying the NGM Signaling Knowledge Base in Lens 3.

## KB Overview

**Location:** `.signaling-kb/interventions/`
**Node Count:** 664 intervention nodes
**Format:** JSON files, one per intervention
**Naming:** Slugified intervention name (e.g., `metformin.json`, `low-intensity-aerobic-exercise.json`)

## Query Types

### 1. Direct Intervention Lookup

**Purpose:** Find exact match for the product being analyzed.

**Method:**
```bash
# Slugify product name and check if file exists
SLUG=$(echo "{{product_name}}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
cat .signaling-kb/interventions/${SLUG}.json
```

**Variations to try:**
1. Exact slugified name: `metformin`
2. Brand name: `glucophage`
3. Common alias: Check `aliases` field in other nodes

**Output:** Full intervention node or "not found"

### 2. Mechanism Target Query

**Purpose:** Find interventions that affect the same molecular targets.

**Method:**
```bash
# Search for target in mechanism_claims
grep -l "\"target\".*AMPK" .signaling-kb/interventions/*.json
grep -l "\"target\".*PRKAA1\|PRKAA2" .signaling-kb/interventions/*.json
grep -l "\"target\".*mTOR\|MTOR" .signaling-kb/interventions/*.json
```

**Target Normalization:**
| Common Name | HGNC Symbol | Aliases to Search |
|-------------|-------------|-------------------|
| AMPK | PRKAA1, PRKAA2 | "AMPK", "PRKAA1", "PRKAA2", "AMP-activated" |
| mTOR | MTOR | "mTOR", "MTOR", "mTORC1", "mTORC2", "mammalian target" |
| SIRT1 | SIRT1 | "SIRT1", "sirtuin", "silent information" |
| NRF2 | NFE2L2 | "NRF2", "Nrf2", "NFE2L2" |

**Output:** List of intervention IDs with matching targets

### 3. Pathway Query

**Purpose:** Find interventions in the same signaling cascade.

**Method:**
```bash
# Search primary_pathways field
grep -l "nutrient.sensing\|mTOR.signaling" .signaling-kb/interventions/*.json

# Search mechanism_claims for pathway-related effects
grep -l "autophagy\|glycolysis\|oxidative.phosphorylation" .signaling-kb/interventions/*.json
```

**Pathway Categories:**
| Axis | Pathways | Search Terms |
|------|----------|--------------|
| Nutrient Sensing | mTOR, AMPK, insulin signaling | "mTOR", "AMPK", "insulin", "nutrient" |
| Proteostasis | Autophagy, UPR, proteasome | "autophagy", "UPR", "proteasome", "protein quality" |
| Mitochondrial | ETC, biogenesis, dynamics | "mitochondri", "ETC", "Complex I", "PGC1" |
| Inflammation | NF-kB, inflammasome, cytokines | "NF-kB", "inflammasome", "IL-6", "TNF" |
| Epigenetic | Sirtuins, methylation, acetylation | "sirtuin", "HDAC", "methylation", "epigenetic" |

**Output:** List of intervention IDs in same pathway

### 4. Indication Query

**Purpose:** Find interventions used for similar clinical purposes.

**Method:**
```bash
# Search dosing_protocols for indication
grep -l "\"indication\".*glycemic\|glucose\|insulin.sensitivity" .signaling-kb/interventions/*.json
grep -l "\"indication\".*longevity\|healthspan\|lifespan" .signaling-kb/interventions/*.json
```

**Common Indications:**
| Category | Search Terms |
|----------|--------------|
| Metabolic | "glycemic", "glucose", "insulin", "diabetes", "metabolic" |
| Longevity | "longevity", "healthspan", "lifespan", "aging" |
| Cognitive | "cognitive", "neuroprotect", "brain", "memory" |
| Cardiovascular | "cardiovascular", "heart", "vascular", "blood pressure" |
| Immune | "immune", "inflammation", "autoimmune" |
| Exercise | "exercise", "performance", "endurance", "strength" |

**Output:** List of intervention IDs with similar indications

---

## Query Helper Script

Use `scripts/query_kb.py` for structured queries:

```bash
# Direct lookup
python scripts/query_kb.py --lookup metformin

# Target search (returns all interventions targeting AMPK)
python scripts/query_kb.py --target AMPK

# Pathway search (returns all interventions in mTOR pathway)
python scripts/query_kb.py --pathway "mTOR signaling"

# Indication search (returns all with glycemic indication)
python scripts/query_kb.py --indication "glycemic control"

# Combined report (all query types)
python scripts/query_kb.py --full-report metformin
```

---

## Extracting Data from KB Nodes

Once you have matching nodes, extract relevant fields:

### From Direct Match

```python
node = load_intervention(slug)

# Key fields to extract
dosing_protocols = node.get("dosing_protocols", [])
mechanism_claims = node.get("mechanism_claims", [])
contraindications = node.get("contraindications", [])
monitoring = node.get("monitoring", [])
conflicts = node.get("conflicts", [])
regulatory_status = node.get("regulatory_status", {})
```

### From Related Interventions

```python
related = query_by_target("AMPK")

for intervention_id in related:
    node = load_intervention(intervention_id)

    # Extract for comparison
    shared_targets = [c["target"] for c in node["mechanism_claims"]
                      if "AMPK" in c["target"]]

    # Classify relationship
    relationship = classify_relationship(
        product_targets=["AMPK"],
        related_targets=shared_targets,
        related_indications=[p["indication"] for p in node["dosing_protocols"]]
    )
```

---

## Relationship Classification

When you find related interventions, classify the relationship:

| Relationship | Criteria | Example |
|--------------|----------|---------|
| `synergistic` | Different targets, complementary effects | Rapamycin (mTOR) + Metformin (AMPK) |
| `complementary` | Same goal, different mechanism | Metformin + Exercise (both improve insulin sensitivity) |
| `overlapping` | Same target, consider redundancy | Metformin + Berberine (both AMPK activators) |
| `potentially_antagonistic` | May interfere with each other | Metformin + Intensive exercise training |
| `neutral` | Same target but no known interaction | Most combinations |

---

## Citation Extraction

Extract peer-reviewed citations from KB nodes:

```python
citations = []

# From dosing_protocols
for protocol in node.get("dosing_protocols", []):
    for cite in protocol.get("peer_reviewed_citations", []):
        citations.append({
            "pmid": cite.get("pmid"),
            "doi": cite.get("doi"),
            "title": cite.get("title"),
            "source": f"{node['intervention_id']}.dosing_protocols"
        })

# From mechanism_claims
for claim in node.get("mechanism_claims", []):
    for cite in claim.get("peer_reviewed_citations", []):
        citations.append({
            "pmid": cite.get("pmid"),
            "doi": cite.get("doi"),
            "title": cite.get("title"),
            "source": f"{node['intervention_id']}.mechanism_claims"
        })

# Deduplicate by PMID/DOI
unique_citations = deduplicate_citations(citations)
```

---

## Handling NOT_IN_KB Products

If direct lookup fails:

1. **Try variations:**
   - Different slugification
   - Brand names
   - Component names (for multi-ingredient products)

2. **Indirect enrichment:**
   - Identify the product's mechanism from Lens 1
   - Query by those targets
   - Query by indication
   - Return related interventions even without direct match

3. **Flag for KB inclusion:**
   - Extract mechanism data in KB-compatible format
   - Save to `.signaling-kb/pending-ingestion/`
   - Note in output that this could be added to KB

---

## Performance Considerations

- **Local queries only:** No API calls in Lens 3
- **File I/O:** Reading 664 JSON files is fast (<1 second for full grep)
- **Caching:** Consider caching intervention index for repeated queries
- **Parallel grep:** Can run multiple greps in parallel for speed

---

## Example Full Query Report

For product "Metformin":

```
=== KB QUERY REPORT: Metformin ===

DIRECT LOOKUP: FOUND
  Node: .signaling-kb/interventions/metformin.json
  Aliases: ["Glucophage"]
  Category: small_molecule
  Dosing Protocols: 9
  Mechanism Claims: 14
  Contraindications: 13

TARGET MATCHES (AMPK):
  - berberine (AMPK activator)
  - exercise (AMPK activator)
  - aicar (AMPK activator)
  - resveratrol (indirect AMPK)

TARGET MATCHES (mTOR):
  - rapamycin (mTORC1 inhibitor)
  - protein-restriction (mTORC1 modulator)

PATHWAY MATCHES (nutrient sensing):
  - fasting (nutrient sensing axis)
  - ketogenic-diet (nutrient sensing)
  - nad-precursors (energy sensing)

INDICATION MATCHES (glycemic):
  - berberine
  - chromium
  - cinnamon-extract
  - alpha-lipoic-acid

CITATIONS EXTRACTED: 8 PMIDs
  - PMID:34391872 (dosing_protocols)
  - DOI:10.1007/s00125-017-4342-z (mechanism_claims)
  - DOI:10.1111/acel.12880 (mechanism_claims)
  - DOI:10.1111/acel.13039 (mechanism_claims)
  - DOI:10.1056/NEJMoa012512 (dosing_protocols)
  ...

CONTRAINDICATIONS:
  - Lactic acidosis risk in renal impairment
  - B12 deficiency with long-term use
  - May blunt exercise adaptations
  ...
```
