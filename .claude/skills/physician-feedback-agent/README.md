# Physician Feedback Agent

Evaluate NGM products and services through the lens of synthesized longevity physician personas.

## Quick Start

```
Invoke: /physician-feedback-agent

Example: Evaluate the lab report generator output for clinical accuracy and actionability
```

## What It Does

This agent simulates feedback from a panel of 8 distinct longevity physician personas, synthesized from real-world clinician discussions. Each persona brings a unique perspective:

| Persona | Primary Focus |
|---------|---------------|
| **Mechanistic Skeptic** | Evidence, mechanisms, skepticism of marketing |
| **Protocol Collector** | Cutting-edge protocols, early adoption |
| **Quality Guardian** | Sourcing, documentation, safety |
| **Precision Pioneer** | Personalization, longitudinal data |
| **Immunology Deep-Diver** | Complex cases, immune nuance |
| **Telehealth Innovator** | Scale, accessibility, affordability |
| **Regenerative Pragmatist** | Practical implementation, ROI |
| **Women's Health Advocate** | Sex differences, HRT, women's needs |

## Products Evaluated

- **Report Generator**: Lab interpretations, biomarker reports
- **Biomarker Analysis Tools**: Test selection, reference ranges
- **Chatbot/AI Outputs**: Medical accuracy, safety, protocols
- **Vendor Directory**: Objectivity, completeness, clinical utility
- **Educational Content**: Accuracy, depth, applicability

## Output Format

Feedback is structured as actionable items for coding agents:

```markdown
### ITEM-001: Implement Optimal Glucose Ranges

**Priority**: P0
**Personas Raising**: Mechanistic Skeptic, Precision Pioneer (6/8)
**Problem**: Report shows glucose 98 as "normal" (lab range) not "suboptimal" (optimal range)
**Solution**: Implement dual-range display with optimal ranges for longevity context

**Implementation Guidance**:
File: src/services/labInterpretation.ts
Change: Add optimalRange alongside labReferenceRange
```

## Files

- `SKILL.md` - Full skill definition and instructions
- `personas.md` - Detailed persona profiles
- `evaluation-criteria.md` - Product-specific scoring frameworks
- `output-format.md` - Actionable output specification

## Origin

Personas synthesized from analysis of the Longevity Docs WhatsApp chat, representing 200+ longevity clinicians across multiple specialties and practice models.
