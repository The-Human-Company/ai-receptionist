# Quality Gate Evaluation

You are evaluating the output of **{{phase_name}}** for **{{product_name}}** against its quality rubric.

## Objective

Determine if the output passes the quality gate. Provide specific, actionable feedback if it fails.

## Input

- **Phase:** {{phase_name}} (L1 | L2 | L3 | Synthesis)
- **Output to Evaluate:** {{output}}
- **Iteration:** {{iteration_number}}

## Evaluation Process

### Step 1: Load Rubric

Based on the phase, apply the corresponding rubric:

#### Lens 1 (Mechanistic) Rubric

| ID | Criterion | Question | Pass Condition |
|----|-----------|----------|----------------|
| L1.1 | `mechanism_depth` | Are specific targets named (genes, proteins, receptors)? | At least 2 specific targets with gene symbols |
| L1.2 | `pathway_accuracy` | Are pathways correctly mapped with direction? | Clear trigger → effect → outcome chain |
| L1.3 | `cascade_completeness` | Does it show trigger → primary → secondary → outcome? | All 4 stages present |
| L1.4 | `analogy_quality` | Is there at least one memorable analogy? | Analogy is accurate and illuminating |
| L1.5 | `diagram_validity` | Does SVG have proper viewBox, padding, readable text? | SVG renders without overflow |
| L1.6 | `first_principles_not_claims` | Does it explain HOW, not whether IF it works? | No efficacy claims, only mechanism |

**Pass threshold:** 5/6

#### Lens 2 (Literature) Rubric

| ID | Criterion | Question | Pass Condition |
|----|-----------|----------|----------------|
| L2.1 | `citation_validity` | Do all PMIDs/DOIs resolve to real papers? | 0 unverified citations in final output |
| L2.2 | `evidence_breadth` | Are 3+ distinct studies cited? | At least 3 unique PMIDs/DOIs |
| L2.3 | `study_details` | Are sample sizes and designs included? | Each study has N and design type |
| L2.4 | `conflict_documentation` | Are conflicting findings noted? | If conflicts exist, they're documented |
| L2.5 | `regulatory_accuracy` | Is regulatory status factually correct? | FDA status matches official records |
| L2.6 | `recency` | Are 2024+ studies included when available? | At least 1 study from 2024-2026 if exists |

**Pass threshold:** 5/6

#### Lens 3 (KB Cross-Reference) Rubric

| ID | Criterion | Question | Pass Condition |
|----|-----------|----------|----------------|
| L3.1 | `kb_search_exhaustive` | Were all 4 query types attempted? | Direct, target, pathway, indication queries run |
| L3.2 | `related_interventions_found` | Are related KB nodes surfaced? | If KB has related nodes, they're listed |
| L3.3 | `mechanism_alignment` | Do KB claims align with Lens 1? | Alignment status documented |
| L3.4 | `conflict_check` | Were contraindications cross-referenced? | KB contraindications included |
| L3.5 | `citation_enrichment` | Were PMIDs from KB incorporated? | KB citations extracted |
| L3.6 | `novel_product_handling` | If not in KB, is this explicitly noted? | NOT_IN_KB status with indirect enrichment |

**Pass threshold:** 5/6

#### Synthesis Rubric

| ID | Criterion | Question | Pass Condition |
|----|-----------|----------|----------------|
| S.1 | `lens_integration` | Are all three lenses represented? | Content from L1, L2, L3 visible |
| S.2 | `conflict_addressed` | Are discrepancies noted and resolved? | All conflicts have resolution notes |
| S.3 | `evidence_graded` | Is confidence communicated? | Claims labeled with confidence level |
| S.4 | `clinical_utility` | Is this actionable for practitioners? | Includes dosing/monitoring/context |
| S.5 | `vendor_neutrality` | No ranking or "best" declarations? | Zero promotional language |

**Pass threshold:** 5/5

### Step 2: Evaluate Each Criterion

For each criterion:
1. Check the output against the pass condition
2. Mark as PASS or FAIL
3. If FAIL, provide specific feedback

### Step 3: Calculate Result

- Count passes
- Compare to threshold
- Determine overall PASS or FAIL

### Step 4: Generate Feedback (if FAIL)

For each failed criterion, provide:
1. What specifically failed
2. Where in the output the issue is
3. How to fix it

## Output Format

```json
{
  "phase": "L1",
  "product": "{{product_name}}",
  "iteration": {{iteration_number}},
  "evaluation": {
    "L1.1": {
      "criterion": "mechanism_depth",
      "status": "PASS",
      "evidence": "Targets named: AMPK (PRKAA1/PRKAA2), Mitochondrial Complex I, MTOR"
    },
    "L1.2": {
      "criterion": "pathway_accuracy",
      "status": "PASS",
      "evidence": "Clear chain: Complex I inhibition → ↑AMP/ATP → AMPK activation → mTORC1 inhibition"
    },
    "L1.3": {
      "criterion": "cascade_completeness",
      "status": "FAIL",
      "evidence": "Missing downstream outcomes after mTORC1 inhibition",
      "feedback": "Add downstream outcomes: enhanced autophagy, reduced protein synthesis, improved insulin sensitivity"
    },
    "L1.4": {
      "criterion": "analogy_quality",
      "status": "PASS",
      "evidence": "Analogy: 'Metformin acts like an energy crisis alarm...'"
    },
    "L1.5": {
      "criterion": "diagram_validity",
      "status": "PASS",
      "evidence": "SVG viewBox 0 0 800 600, all text within bounds"
    },
    "L1.6": {
      "criterion": "first_principles_not_claims",
      "status": "PASS",
      "evidence": "No efficacy claims found; focuses on mechanism"
    }
  },
  "summary": {
    "passed": 5,
    "failed": 1,
    "threshold": 5,
    "result": "PASS"
  },
  "retry_feedback": null
}
```

If FAIL:

```json
{
  "summary": {
    "passed": 4,
    "failed": 2,
    "threshold": 5,
    "result": "FAIL"
  },
  "retry_feedback": {
    "failures": [
      {
        "criterion": "L1.3",
        "issue": "Cascade incomplete - missing downstream outcomes",
        "location": "pathway_map.downstream_outcomes",
        "fix": "Add: enhanced autophagy, reduced protein synthesis, improved insulin sensitivity after mTORC1 inhibition"
      },
      {
        "criterion": "L1.5",
        "issue": "SVG text overflow",
        "location": "pathway_diagram_svg, text at y=580 in 600-height viewBox",
        "fix": "Increase viewBox height to 700 or move text up by 40px"
      }
    ],
    "priority": "Fix L1.5 first (rendering), then L1.3 (content)"
  }
}
```

## Evaluation Guidelines

### Be Specific
- Bad: "Pathway is wrong"
- Good: "Pathway shows AMPK → mTOR activation, but should show inhibition (AMPK inhibits mTORC1)"

### Be Actionable
- Bad: "Add more detail"
- Good: "Add sample size (N=97) and study duration (12 months) for PMID:34391872"

### Be Fair
- Don't fail for optional elements
- Don't fail for stylistic preferences
- Only fail for rubric violations

### Trust the Threshold
- If 5/6 pass, the phase passes even with one failure
- Log the failure for future improvement, but don't block progress
