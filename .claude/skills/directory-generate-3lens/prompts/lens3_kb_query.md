# Lens 3: Knowledge Base Cross-Referencing & Citation Extraction

You are cross-referencing **{{product_name}}** against the NGM Signaling Knowledge Base to:
1. Surface related interventions and mechanism alignment
2. **Extract peer-reviewed citations (PMIDs/DOIs) to enrich the final output**
3. Build actionability mapping from findings to interventions

## CRITICAL: Citation Policy

**The KB is a source aggregator, NOT a citable source.**

When you find relevant data in the KB:
- **EXTRACT** the PMIDs and DOIs from `peer_reviewed_citations[]` arrays
- **CITE** those papers directly in the final output
- **NEVER** cite "the KB" or "internal knowledge base"

```
✗ WRONG: "According to our knowledge base, butyrate supports colonocyte function"
✓ RIGHT: "Butyrate serves as the primary fuel for colonocyte mitochondrial respiration (Litvak et al., Science, 2018; DOI: 10.1126/science.aat9076)"
```

## Product Type Detection

Before querying, identify the product type:

| Product Type | Query Strategy | Examples |
|--------------|----------------|----------|
| **Intervention** | Direct lookup + target/pathway queries | Metformin, Rapamycin, Butyrate supplements |
| **Testing/Diagnostic** | Biomarker queries + "what it informs" queries | Microbiome tests, lab panels, breath tests |
| **Service** | Related intervention queries | Coaching, protocols, programs |

## Objective

The KB contains 664 intervention nodes with:
- Mechanism claims with peer-reviewed citations
- Dosing protocols with indications
- Contraindications and monitoring parameters
- Implicit clinical wisdom

## The Clinical Perspective Layer

Beyond mechanism claims and citations, the KB contains embedded wisdom:

- **What practitioners actually monitor** → reveals what matters in practice
- **How dosing protocols are structured** → reveals clinical priorities
- **What contraindications are emphasized** → reveals hard-won lessons
- **What combinations are used** → reveals clinical thinking patterns
- **What alternatives exist** → reveals the decision landscape

This implicit knowledge should inform the **voice and perspective** of the entire directory entry—not be siloed into a separate "KB Insights" box.

## Input

- **Product Name:** {{product_name}}
- **Slugified Name:** {{slug}}
- **Lens 1 Output (Mechanism):** {{lens1_output}}
- **KB Path:** `.signaling-kb/interventions/`

## Process

### Step 0: Product Type Detection

First, determine the product type:

```
{{product_name}} is a:
[ ] INTERVENTION - supplement, drug, therapy (has direct KB node)
[ ] TESTING/DIAGNOSTIC - lab test, microbiome test, device (measures biomarkers)
[ ] SERVICE - coaching, program (connects to interventions)
```

**For TESTING/DIAGNOSTIC products, skip Step 1 and go to Step 1B.**

### Step 1: Direct Intervention Lookup (for Intervention products)

Query the KB for an exact match:

```bash
python scripts/query_kb.py --lookup {{slug}}
```

If found, extract structured data AND implicit perspectives:

### Step 1B: Biomarker-Based Queries (for Testing/Diagnostic products)

For testing products like microbiome tests, query by what they MEASURE:

```bash
# Identify biomarkers this test measures
# For microbiome testing, these include:

# SCFA/Butyrate markers
python scripts/query_kb.py --biomarker butyrate --json
python scripts/query_kb.py --target "SCFA" --json
python scripts/query_kb.py --target "short-chain fatty acid" --json

# Specific organisms
python scripts/query_kb.py --biomarker akkermansia --json
python scripts/query_kb.py --indication "gut microbiome" --json

# Gut-related pathways
python scripts/query_kb.py --pathway "gut barrier" --json
python scripts/query_kb.py --target "colonocyte" --json
python scripts/query_kb.py --target "HDAC" --json  # butyrate target

# Prebiotics/probiotics that test results inform
python scripts/query_kb.py --indication "prebiotic" --json
python scripts/query_kb.py --indication "probiotic" --json
```

**For each matched intervention, extract:**
1. `peer_reviewed_citations[]` - PMIDs/DOIs to cite
2. `mechanism_claims[]` - explains WHY the biomarker matters
3. `dosing_protocols[]` - actionable interventions test results inform

| KB Field | Factual Extraction | Implicit Perspective |
|----------|-------------------|---------------------|
| `dosing_protocols[]` | Specific doses, timing | What clinicians prioritize for different use cases |
| `mechanism_claims[]` | Molecular targets | Which mechanisms clinicians find most clinically relevant |
| `contraindications[]` | Safety warnings | Hard-won clinical experience, what to watch for |
| `monitoring[]` | Tests to run | What actually matters in practice |
| `conflicts[]` | Drug interactions | Where extra caution is warranted |

### Step 2: Related Intervention Discovery

Using targets from Lens 1, find the clinical neighborhood:

```bash
# Find interventions targeting same pathways
python scripts/query_kb.py --target {{primary_target}}
python scripts/query_kb.py --pathway "{{primary_pathway}}"
python scripts/query_kb.py --indication "{{primary_indication}}"
```

For each related intervention, extract:
- How it relates mechanistically
- What clinical context it serves
- What this reveals about the decision landscape

### Step 3: Clinical Perspective Synthesis

For this product category, synthesize:

#### A. The Practitioner's Mental Model
How do clinicians think about this category? What questions do they ask? What tradeoffs do they weigh?

Example for testing products:
- "What does this test actually tell me that changes my clinical decision?"
- "How does this fit into my testing sequence?"
- "What actionable interventions does this enable?"

#### B. The Intervention Landscape
What KB interventions does this product/category connect to? This reveals its clinical value.

Example for microbiome testing:
- If related to fiber/prebiotic interventions → primary value is guiding dietary optimization
- If related to antimicrobials → may inform dysbiosis treatment
- If related to probiotics → may guide strain selection

#### C. The Practical Wisdom
What do experienced practitioners know that isn't in the literature?

- Monitoring that matters most
- Timing considerations
- Patient populations where this shines
- Realistic expectations

### Step 4: "Notable For" Framing

For vendor/product comparisons, extract what makes each option **distinctive** rather than ranking them:

**DO:**
- "Notable for its metatranscriptomic approach, which captures functional activity"
- "Distinctive in offering personalized supplement recommendations"
- "Emphasizes practitioner education and protocol integration"

**DON'T:**
- "Best for..." or "Better than..."
- "Weakness is..." or "Lacks..."
- Critical comparisons or rankings

The goal: A clinician reading should understand what makes each option interesting, not which is "best."

### Step 5: Actionability Mapping

Map this product/category to **actionable next steps** from the KB:

```
[Product/Test] → reveals → [Insight] → informs → [KB Intervention]
```

Example:
```
Microbiome test → reveals → low Akkermansia → informs → fiber-and-prebiotics intervention
Microbiome test → reveals → elevated LPS markers → informs → gut-barrier-support protocols
```

This creates the clinical utility story—not just what the test shows, but what you *do* about it.

## Output Format

Return a JSON object:

```json
{
  "kb_lookup": {
    "direct_match_found": true,
    "intervention_id": "...",
    "node_path": "..."
  },

  "kb_factual_summary": {
    "mechanism_claims_count": 14,
    "dosing_protocols_count": 9,
    "contraindications_count": 13,
    "monitoring_items": ["..."],
    "related_interventions": ["..."]
  },

  "clinical_perspective_extraction": {
    "practitioner_mental_model": {
      "key_questions_clinicians_ask": [
        "What does this test tell me that changes my treatment plan?",
        "How do I sequence this with other diagnostics?",
        "What specific interventions does this inform?"
      ],
      "tradeoffs_practitioners_weigh": [
        "Depth of analysis vs. actionability",
        "Cost vs. clinical utility",
        "Snapshot vs. longitudinal tracking"
      ]
    },

    "intervention_landscape": {
      "connected_kb_interventions": [
        {
          "intervention_id": "fiber-and-prebiotics",
          "connection_type": "informs",
          "clinical_narrative": "Microbiome testing's primary clinical value is guiding personalized fiber and prebiotic interventions—the KB shows 9 distinct fiber protocols that can be optimized based on test results"
        }
      ],
      "clinical_value_story": "The primary clinical utility of microbiome testing lies in its ability to inform targeted interventions—particularly around fiber, prebiotics, and SCFA optimization—rather than as standalone diagnostics."
    },

    "practical_wisdom": {
      "what_practitioners_monitor": "...",
      "timing_considerations": "...",
      "patient_populations_where_valuable": "...",
      "realistic_expectations": "..."
    }
  },

  "notable_for_framing": {
    "entities_analyzed": [
      {
        "entity_name": "Viome",
        "notable_for": [
          "Metatranscriptomic approach capturing functional gene expression",
          "Personalized supplement recommendations based on AI analysis",
          "Longitudinal tracking with repeated testing protocols"
        ],
        "distinctive_approach": "Emphasizes functional activity over taxonomic abundance"
      }
    ]
  },

  "actionability_mapping": [
    {
      "finding": "Low Akkermansia muciniphila",
      "kb_interventions_informed": ["fiber-and-prebiotics", "polyphenols"],
      "clinical_action": "Consider prebiotic fiber (especially inulin, FOS) and polyphenol-rich foods to support Akkermansia abundance"
    }
  ],

  "integration_guidance": {
    "how_to_weave_throughout": {
      "mechanism_section": "Inform the 'why it matters' with clinical value story",
      "evidence_section": "Ground research findings in practical implications",
      "guidance_section": "Lead with KB-informed actionability",
      "faq_section": "Answer the questions practitioners actually ask"
    }
  },

  "citations_extracted_from_kb": {
    "total_pmids": 12,
    "total_dois": 8,
    "citations": [
      {
        "pmid": "23223453",
        "doi": "10.1126/science.1227166",
        "title": "Suppression of oxidative stress by β-hydroxybutyrate",
        "source_node": "butyrate.json",
        "relevance": "Explains HDAC inhibition mechanism measurable via SCFA testing"
      },
      {
        "pmid": null,
        "doi": "10.1126/science.aat9076",
        "title": "Colonocyte metabolism shapes the gut microbiota",
        "source_node": "butyrate.json",
        "relevance": "Core reference for butyrate as colonocyte fuel"
      }
    ],
    "citation_integration_guidance": {
      "mechanism_section": "Use DOI:10.1126/science.aat9076 when explaining colonocyte metabolism",
      "evidence_section": "Cite PMID:23223453 for HDAC inhibition evidence",
      "decision_support": "Reference KB mechanism claims when explaining why findings matter"
    }
  }
}
```

## Handling Products NOT in KB

If direct lookup fails, the related intervention discovery becomes even more important:

```json
{
  "kb_lookup": {
    "direct_match_found": false,
    "search_attempted": ["...", "..."]
  },
  "novel_product_handling": {
    "status": "NOT_IN_KB",
    "indirect_enrichment_strategy": "Connect to related interventions this product enables or informs",
    "related_by_mechanism": ["..."],
    "related_by_clinical_use": ["..."],
    "clinical_value_story": "Even without a direct KB entry, this product connects to [X] KB interventions..."
  }
}
```

## Quality Criteria

Before returning, verify:

- [ ] **L3.1 kb_search_exhaustive**: All query types attempted (direct, target, pathway, biomarker)
- [ ] **L3.2 pmid_extraction**: Minimum 5 PMIDs/DOIs extracted from KB nodes
- [ ] **L3.3 citations_actionable**: Each citation has clear integration guidance (which section to use it in)
- [ ] **L3.4 actionability_mapped**: Clear connection to KB interventions (Finding → Intervention)
- [ ] **L3.5 notable_for_framing**: Entities positioned positively without ranking
- [ ] **L3.6 no_kb_citation**: Output never references "the KB" as a source; only peer-reviewed papers

You must pass 5/6 criteria.

## Citation Extraction Checklist

For each KB node queried, extract:

```python
for node in matched_kb_nodes:
    for claim in node['mechanism_claims']:
        for cite in claim.get('peer_reviewed_citations', []):
            if cite.get('pmid') or cite.get('doi'):
                # ADD TO OUTPUT
                extracted_citations.append({
                    'pmid': cite.get('pmid'),
                    'doi': cite.get('doi'),
                    'title': cite.get('title'),
                    'from_claim': claim.get('claim_id'),
                    'relevance': f"Supports: {claim.get('effect')}"
                })
```

## Critical Principles

1. **Extract perspective, not just facts** - The KB's value is the clinical wisdom encoded in it
2. **"Notable for" over "better than"** - Position positively, never compare negatively
3. **Actionability is the story** - Connect everything to what clinicians *do*
4. **Weave, don't silo** - This output should inform the entire narrative, not live in a box
5. **Clinician-useful, vendor-friendly** - Both can be true simultaneously
