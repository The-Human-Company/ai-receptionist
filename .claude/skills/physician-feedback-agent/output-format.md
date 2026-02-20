# Actionable Feedback Output Format

This document defines the standard output format for physician feedback that can be directly consumed by coding agents.

## Output Structure

```markdown
# Physician Panel Feedback Report

**Product Evaluated**: [Product name/type]
**Evaluation Date**: [Date]
**Files Reviewed**: [List of files examined]
**Personas Consulted**: [List of personas used]

---

## Executive Summary

[2-3 sentence summary of key findings and overall assessment]

**Overall Verdict**: [Ready for Use | Needs Work | Critical Issues]

---

## Priority Matrix

### P0 - Critical (Must Fix Before Launch)
Issues that could cause patient harm, legal liability, or fundamental product failure.

### P1 - High Priority (Fix This Sprint)
Significant usability or accuracy issues that affect clinical utility.

### P2 - Medium Priority (Backlog)
Improvements that would enhance the product but aren't blocking.

### P3 - Nice to Have (Future Consideration)
Polish items and feature requests from the physician panel.

---

## Actionable Items

### [ITEM-001] [Short Title]

**Priority**: P0/P1/P2/P3
**Category**: [Accuracy | UX | Safety | Completeness | Performance]
**Personas Raising**: [List of personas who raised this concern]
**Consensus Level**: [Universal | Majority | Split | Minority]

**Problem Statement**:
[Clear description of the issue from the physician perspective]

**Clinical Impact**:
[Why this matters for patient care or clinician workflow]

**Suggested Solution**:
[Specific, actionable fix]

**Implementation Guidance**:
```
File: [path/to/file.tsx]
Location: [function/component name or line range]
Change: [Specific code change or approach]
```

**Acceptance Criteria**:
- [ ] [Specific testable outcome 1]
- [ ] [Specific testable outcome 2]

---

### [ITEM-002] [Short Title]
...

---

## Persona-Specific Feedback

### The Mechanistic Skeptic
**Overall Assessment**: [Satisfied | Concerns | Would Not Use]

**Key Feedback**:
- [Bullet point feedback]

**Suggested Improvements**:
1. [Specific improvement]

---

### The Protocol Collector
...

---

## Trade-off Decisions Required

Some feedback reveals fundamental tensions where the product team must make strategic choices:

### Trade-off 1: [Title]
**Tension**: [Persona A] wants X, but [Persona B] wants Y
**Options**:
1. Option A: [Description] - Favored by: [Personas]
2. Option B: [Description] - Favored by: [Personas]
3. Option C: [Hybrid approach]
**Recommendation**: [Your recommended approach with rationale]

---

## Quick Wins

Low-effort, high-impact improvements that can be implemented immediately:

| Item | Description | Effort | Impact |
|------|-------------|--------|--------|
| [ID] | [Description] | [Hours] | [High/Med/Low] |

---

## Implementation Roadmap

**Phase 1: Critical Fixes** (Immediate)
- [ ] ITEM-001: [Title]
- [ ] ITEM-002: [Title]

**Phase 2: Core Improvements** (Next Sprint)
- [ ] ITEM-003: [Title]
- [ ] ITEM-004: [Title]

**Phase 3: Polish & Enhancement** (Backlog)
- [ ] ITEM-005: [Title]

---

## Appendix: Raw Persona Evaluations

<details>
<summary>Click to expand full persona evaluations</summary>

### Mechanistic Skeptic - Full Evaluation
[Complete evaluation notes]

### Protocol Collector - Full Evaluation
[Complete evaluation notes]

...

</details>
```

---

## Formatting Rules

### Item IDs
- Use sequential numbering: ITEM-001, ITEM-002, etc.
- Prefix with category when helpful: ACC-001 (accuracy), UX-001 (user experience)

### Priority Definitions

| Priority | Definition | SLA |
|----------|------------|-----|
| **P0** | Patient safety, legal risk, or product-breaking issue | Fix before any release |
| **P1** | Significant clinical utility or accuracy problem | Fix this sprint |
| **P2** | Material improvement to physician experience | Backlog, prioritize quarterly |
| **P3** | Enhancement request, edge case, or polish | Future consideration |

### Consensus Levels

| Level | Definition |
|-------|------------|
| **Universal** | 6+ of 8 personas agree |
| **Majority** | 4-5 of 8 personas agree |
| **Split** | 3-4 personas on each side |
| **Minority** | 1-2 personas, but represents important edge case |

### Implementation Guidance Quality

Good implementation guidance should:
1. Specify the exact file path
2. Identify the function/component to modify
3. Describe the change conceptually
4. Provide code snippets when helpful
5. Note any dependencies or related changes

**Example of Good Guidance:**
```
File: src/components/reports/LabInterpretation.tsx
Location: renderBiomarkerAnalysis() function, lines 45-67
Change: Add mechanism explanation section after each abnormal finding

Code pattern:
{finding.isAbnormal && (
  <div className="mechanism-explanation">
    <h4>Why This Matters</h4>
    <p>{finding.mechanismExplanation}</p>
    <p className="evidence-note">Based on: {finding.citations.join(', ')}</p>
  </div>
)}

Related changes needed:
- Update BiomarkerFinding type in src/types/biomarkers.ts to include mechanismExplanation
- Add mechanism data to the AI prompt in src/services/reportGeneration.ts
```

**Example of Poor Guidance:**
```
Make the reports explain mechanisms better.
```

---

## Downstream Agent Integration

This output format is designed to be parsed by coding agents. Key integration points:

### For Code Implementation Agents
- Parse `Implementation Guidance` blocks for file paths and code changes
- Use `Acceptance Criteria` as test cases
- Follow `Priority` ordering for work sequence

### For Testing Agents
- Convert `Acceptance Criteria` to test cases
- Validate against `Clinical Impact` statements
- Check for regression on previously-passed items

### For Documentation Agents
- Use `Problem Statement` and `Suggested Solution` for changelog entries
- Reference `Personas Raising` for user story attribution
- Include `Clinical Impact` in release notes

---

## Example Output

```markdown
# Physician Panel Feedback Report

**Product Evaluated**: Lab Report Generator - Metabolic Panel Output
**Evaluation Date**: 2025-01-07
**Files Reviewed**: src/components/reports/MetabolicReport.tsx, src/services/labInterpretation.ts
**Personas Consulted**: All 8 core personas

---

## Executive Summary

The metabolic report generator provides accurate basic interpretations but lacks mechanism explanations that longevity physicians require. The Mechanistic Skeptic and Precision Medicine Pioneer both flagged that recommendations feel generic. The report also uses standard lab ranges instead of optimal ranges, which 6/8 personas identified as a critical gap.

**Overall Verdict**: Needs Work

---

## Priority Matrix

### P0 - Critical
- ACC-001: Fasting glucose interpretation uses lab range (70-100) instead of optimal range (75-85)

### P1 - High Priority
- ACC-002: Missing mechanism explanations for abnormal findings
- UX-001: No visual prioritization of which findings need attention first

### P2 - Medium Priority
- UX-002: Add sex-specific reference range option
- COMP-001: Include HbA1c trending over time if historical data exists

### P3 - Nice to Have
- ENH-001: Add protocol suggestions for borderline findings

---

## Actionable Items

### ACC-001: Implement Optimal Ranges for Glucose

**Priority**: P0
**Category**: Accuracy
**Personas Raising**: Mechanistic Skeptic, Precision Medicine Pioneer, Protocol Collector, Quality Guardian, Telehealth Innovator, Women's Health Advocate
**Consensus Level**: Universal

**Problem Statement**:
The report flags glucose as "normal" at 98 mg/dL because it falls within the standard lab range (70-100). However, longevity physicians consider optimal glucose to be 75-85 mg/dL, with 90-99 being "suboptimal" warranting intervention.

**Clinical Impact**:
Patients with metabolic dysfunction are being told their glucose is "normal" when longevity practitioners would recommend intervention. This undermines the entire value proposition of a longevity-focused report.

**Suggested Solution**:
Implement a dual-range system showing both lab reference and optimal ranges, with interpretations based on optimal ranges for longevity context.

**Implementation Guidance**:
```typescript
// File: src/services/labInterpretation.ts
// Location: interpretGlucose() function

// Current:
const isNormal = glucose >= 70 && glucose <= 100;

// Change to:
const labReferenceRange = { min: 70, max: 100 };
const optimalRange = { min: 75, max: 85 };
const suboptimalRange = { min: 86, max: 99 };

const interpretation = {
  labStatus: glucose >= labReferenceRange.min && glucose <= labReferenceRange.max ? 'normal' : 'abnormal',
  optimalStatus: glucose >= optimalRange.min && glucose <= optimalRange.max
    ? 'optimal'
    : glucose >= suboptimalRange.min && glucose <= suboptimalRange.max
      ? 'suboptimal'
      : 'requires-attention',
  clinicalNote: getGlucoseClinicalNote(glucose)
};
```

**Acceptance Criteria**:
- [ ] Glucose of 98 mg/dL displays as "suboptimal" not "normal"
- [ ] Report shows both lab reference range and optimal range
- [ ] Color coding reflects optimal status (green for optimal, yellow for suboptimal, red for abnormal)
- [ ] Clinical note explains why optimal range differs from lab range
```

---

This format ensures every piece of feedback is actionable and can be directly implemented by development teams or coding agents.
