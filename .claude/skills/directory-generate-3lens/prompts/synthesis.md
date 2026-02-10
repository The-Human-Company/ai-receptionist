# Synthesis Phase: Elevated Scientific Listicle with Clinical Voice

You are synthesizing outputs from all three analytical lenses into an **elevated, highly scientific, research-driven listicle** for **{{product_name}}** that speaks with clinical authority and practical wisdom.

## The Format: Elevated Scientific Listicle

This is not a superficial "top 5" list. It's a comprehensive clinical evaluation guide that:
1. **Satisfies LLM extraction patterns** — structured for citation by AI answer engines
2. **Provides genuine clinical value** — substantive enough that practitioners learn from it
3. **Positions vendors positively** — "notable for" framing, no rankings or criticism
4. **Goes deep** — each entity section is substantially developed

### Why This Format Works for AEO

- **80%** of articles cited by ChatGPT include list sections
- Content with **sequential H1>H2>H3 structure** is cited **3x more often**
- **Q&A format** content is **40% more likely** to be extracted by AI
- LLMs cite answers, not articles — structure each paragraph to answer one question

## Inputs

- **Product Name:** {{product_name}}
- **Lens 1 Output (Mechanistic):** {{lens1_output}}
- **Lens 2 Output (Literature):** {{lens2_output}}
- **Lens 3 Output (KB + Citations):** {{lens3_output}}

## CRITICAL: KB Citation Integration

Lens 3 provides `citations_extracted_from_kb` with PMIDs and DOIs. These MUST be woven throughout the output:

**Citation Policy:**
- The KB is a source aggregator, NOT a citable source
- Extract PMIDs/DOIs from L3 output and cite them directly
- Never write "according to our knowledge base" or similar

**Where to integrate KB citations:**

| Section | How to Use KB Citations |
|---------|------------------------|
| Technology | "Butyrate serves as primary colonocyte fuel (Litvak et al., 2018)" |
| Evidence | Add KB PMIDs to evidence table alongside L2 literature |
| Decision Support | "Low butyrate-producers correlate with barrier dysfunction (PMID: 28798127)" |
| FAQ | Back answers with KB-sourced citations where relevant |

**Integration Pattern:**
```
L3 provides: doi: "10.1126/science.aat9076", title: "Colonocyte metabolism shapes..."

✓ DO: "Tests measuring butyrate-producing bacteria assess a key metabolic
       pathway—these organisms provide the primary fuel source for colonocytes
       (Litvak et al., Science, 2018)."

✗ DON'T: "According to our internal knowledge base, butyrate matters for gut health."
```

## Content Structure (In Order)

### 1. Title & Meta (AEO-Optimized)
```
Title: "[Category]: A Clinical Evaluation Guide for [Year]"
Subtitle: "Understanding methodologies, evaluating evidence, and connecting findings to interventions"
```

### 2. Quick Reference Summary Table
**Place at top for LLM extraction.** A scannable comparison table with:
- Entity name
- Methodology
- Notable for (1-line)
- Price range
- Ordering model

### 3. Executive Summary (300-400 words)
Lead with the **clinical value proposition**:
- Why this category matters to practitioners (from L3's clinical perspective)
- What the evidence shows (from L2)
- What interventions this connects to (from L3's actionability mapping)

**Structure:** 3-4 paragraphs, each focused on one key point.

### 4. Understanding the Technology (800-1000 words)
Lead with clinical questions, then explain mechanisms:

**For each methodology:**
- H3 subheading with methodology name
- What clinical question it answers (from L3's practitioner mental model)
- How it works mechanistically (from L1)
- When a practitioner would choose this approach
- Specific capabilities and outputs

**Include:**
- Comparison table of methodologies
- SVG diagram (from L1)
- At least one inline Q&A block

### 5. The Evidence Landscape (600-800 words)
Ground research in clinical implications:

- Key studies with grades and specific findings (from L2)
- Evidence table with Grade/Study/Finding structure
- What evidence gaps exist (stated explicitly)
- How practitioners should interpret uncertainty

**Include:**
- Evidence grading table
- "Nuance" callout for conflicting findings
- Inline Q&A: "How should I interpret these results given the evidence?"

### 6. Entity Sections — The Elevated Listicle (400-600 words each)
**This is the core of the listicle format.** Each entity gets a substantial section:

```
## [Number]. [Entity Name]: [Distinguishing Tagline]

### Quick Facts
- **Methodology:** [Specific approach]
- **Price:** $X-X
- **Ordering:** [Direct-to-consumer / Practitioner-only]
- **Turnaround:** X weeks

### What Makes It Notable
[3-4 bullet points with the "notable for" highlights]

### The Approach in Depth
[2-3 paragraphs explaining the methodology, technology choices, and what distinguishes this approach. Include specific technical details that practitioners care about. Reference L1 mechanism data.]

### Clinical Fit
[1-2 paragraphs on which practitioners/workflows this supports, patient populations, specific use cases. Draw from L3's clinical perspective.]

### Evidence & Validation
[1-2 paragraphs on any validation studies, regulatory status, what the literature shows about this specific product/methodology. Reference L2 evidence where available.]
```

**Number entities** (1, 2, 3, 4, 5) for listicle format, but **never rank them**.

### 7. Clinical Decision Support (500-700 words)
This is where KB actionability mapping shines:

**From Finding to Action table:**
```
| Finding | Intervention | Rationale |
|---------|--------------|-----------|
| Low diversity | Fiber diversity + prebiotics | KB shows 14+ interventions... |
```

**Include:**
- Action pathway visual/table
- "Realistic Expectations" section (what testing does well / doesn't do)
- Inline Q&A: "What's the most evidence-supported action from microbiome test results?"

### 8. Frequently Asked Questions (6-10 Q&A)
**Structure for AI extraction:**
- Question as H3 or strong formatted text
- Direct answer front-loaded (first sentence answers the question)
- Supporting detail follows
- 80-120 words per answer
- Source citations inline

**Question sources:**
- L3's "key questions clinicians ask"
- Common clinical decision points
- Methodology comparisons
- Interpretation guidance

### 9. Sources
Formatted for both human readers and AI extraction:
```
[1] Author et al. (Year). Title. Journal. PMID:XXXXXXXX
```

## Content Depth Requirements

| Section | Word Count | Key Elements |
|---------|------------|--------------|
| Quick Reference Table | N/A | 5-6 rows, 4-5 columns |
| Executive Summary | 300-400 | Clinical value proposition |
| Technology | 800-1000 | Comparison table, diagram, Q&A |
| Evidence | 600-800 | Graded table, nuance callouts |
| Each Entity | 400-600 | Quick facts, depth, clinical fit, evidence |
| Decision Support | 500-700 | Action pathways, expectations |
| FAQ | 500-800 | 6-10 Q&A pairs |
| **Total** | **5,000-7,000** | Comprehensive guide |

## Inline Q&A Blocks

Weave Q&A throughout—not just at the end:

**In Technology Section:**
> **Q: How does metatranscriptomics differ from shotgun metagenomics?**
> A: While shotgun metagenomics sequences all DNA to show what organisms are present and what they could potentially do, metatranscriptomics sequences RNA to reveal what genes are actively being expressed at the moment of sampling. Think of it as the difference between reading someone's resume (what they're capable of) versus watching them work (what they're actually doing).

**In Evidence Section:**
> **Q: Given the interlaboratory variability, can I trust these test results?**
> A: The variability reflects methodology differences rather than error. For reliable interpretation: use the same laboratory for longitudinal tracking, focus on directional changes rather than absolute values, and interpret results within clinical context rather than as standalone diagnostics.

**In Decision Support:**
> **Q: What's the single most evidence-supported action from microbiome test results?**
> A: Adjusting dietary fiber intake. Our knowledge base shows that fiber and prebiotic interventions have the strongest evidence for modifying the microbiome beneficially. More complex supplement protocols lack the same level of clinical validation.

## Output Format

```json
{
  "synthesis_meta": {
    "product_name": "{{product_name}}",
    "format": "elevated_scientific_listicle",
    "estimated_word_count": 6000,
    "entity_count": 5,
    "faq_count": 8
  },

  "quick_reference_table": {
    "columns": ["Entity", "Methodology", "Notable For", "Price", "Ordering"],
    "rows": [...]
  },

  "sections": {
    "executive_summary": "...",
    "technology": {
      "intro": "...",
      "methodologies": [
        {"name": "16S rRNA", "content": "...", "clinical_question": "..."}
      ],
      "comparison_table": {...},
      "inline_qa": [...]
    },
    "evidence": {
      "narrative": "...",
      "studies_table": [...],
      "nuance_notes": [...],
      "inline_qa": [...]
    },
    "entities": [
      {
        "number": 1,
        "name": "Viome",
        "tagline": "Functional Activity Through Metatranscriptomics",
        "quick_facts": {...},
        "notable_for": [...],
        "approach_depth": "...",
        "clinical_fit": "...",
        "evidence_validation": "..."
      }
    ],
    "decision_support": {
      "intro": "...",
      "action_pathways": [...],
      "realistic_expectations": "...",
      "inline_qa": [...]
    },
    "faq": [
      {"question": "...", "answer": "...", "sources": [...]}
    ]
  },

  "diagrams": {
    "methodology_diagram": "<svg>...</svg>",
    "methodology_comparison_table": "<table>...</table>"
  },

  "compiled_citations": [...]
}
```

## Quality Criteria (Self-Check)

Before returning, verify:

- [ ] **S.1 listicle_structure**: Numbered entities, quick reference table at top
- [ ] **S.2 content_depth**: 5,000+ words total, 400+ per entity section
- [ ] **S.3 clinical_voice_throughout**: Every section has clinical context
- [ ] **S.4 vendor_positive_framing**: All entities with "notable for," no criticism
- [ ] **S.5 inline_qa_distributed**: Q&A woven throughout, not just FAQ section
- [ ] **S.6 actionability_clear**: Decision support connects findings to interventions
- [ ] **S.7 evidence_graded**: Confidence levels visible throughout
- [ ] **S.8 kb_citations_integrated**: L3 PMIDs/DOIs appear in output (minimum 5)
- [ ] **S.9 no_kb_as_source**: Output never cites "the KB" or "internal knowledge"

You must pass 7/9 criteria.

## Citation Merge Strategy

The final output merges citations from L2 (Sonar Deep Research) and L3 (KB extraction):

```
L2 citations: Fresh literature from Perplexity deep research
L3 citations: Curated PMIDs from KB mechanism_claims and dosing_protocols

Final sources = deduplicate(L2_citations + L3_citations)
```

**Deduplication:** If same PMID appears in both, keep one instance with combined context.

**KB Citation Quality Filter:** Only include L3 citations where:
- `confidence` is "high" or "moderate"
- `pmid` or `doi` is not null
- `title` is present

## The Litmus Tests

Before finalizing, verify:

1. **Vendor test:** Would every vendor featured be happy to share this page?
2. **Clinician test:** Would a practitioner learn something and find this actionable?
3. **LLM test:** Could an AI easily extract structured answers from this content?
4. **Depth test:** Is this substantially more developed than typical listicle content?

All four must pass.
