================================================================================
LECTURE ITERATOR CHANGELOG
================================================================================

Session ID:     [iter-YYYY-MM-DD-physician-slug]
Physician:      [Full Name (slug)]
Course:         [Course Title (slug)]
Started:        [ISO timestamp]
Completed:      [ISO timestamp or "In Progress"]

Feedback Source: [Path or description]

================================================================================
CHANGE SUMMARY
================================================================================

Total Changes:  [N]
  - Factual Corrections:  [N]
  - Content Edits:        [N]
  - Structure Changes:    [N]
  - Diagram Updates:      [N]
  - Callout Modifications:[N]
  - Reference Updates:    [N]

Lectures Modified: [lecture-1, lecture-3, lecture-5]

Clarifications Requested: [N]

================================================================================
CHANGE LOG
================================================================================

--- CHANGE 001 | T-001 | [Category] ---
Timestamp:    [ISO timestamp]
Lecture:      lecture-[N]
Slide:        [slide-id or "lecture-level"]
Target:       [content[2].text / callouts[0] / references / etc.]

Description:  [What was changed and why]

Before:
```
[Original content - exact text or structure]
```

After:
```
[New content - exact text or structure]
```

Rationale:    [Why this change was made, from feedback source]
Feedback Ref: [Line number or timestamp in original feedback]
Status:       APPLIED

---

--- CHANGE 002 | T-002 | [Category] ---
Timestamp:    [ISO timestamp]
Lecture:      lecture-[N]
Slide:        [slide-id]
Target:       [path]

Description:  [What was changed]

Before:
```
[Original]
```

After:
```
[New]
```

Rationale:    [From feedback]
Feedback Ref: [Reference]
Status:       APPLIED

---

[... additional changes ...]

================================================================================
CLARIFICATIONS
================================================================================

--- CLARIFICATION 001 ---
Timestamp:    [ISO timestamp]
Question:     [What was asked]
Options:      [A) Option 1, B) Option 2, ...]
Response:     [User's answer]
Applied To:   [T-003, T-004]

---

[... additional clarifications if any ...]

================================================================================
FILES MODIFIED
================================================================================

| File | Changes | Status |
|------|---------|--------|
| content/physician-courses/[physician]/[course]/lecture-1.json | 3 | Modified |
| content/physician-courses/[physician]/[course]/lecture-3.json | 5 | Modified |
| content/physician-courses/[physician]/[course]/lecture-5.json | 2 | Modified |

Total Files: [N]

================================================================================
EXECUTION NOTES
================================================================================

Patterns Discovered:
- [Any patterns learned during this session]
- [Useful for future iterations]

Issues Encountered:
- [Any problems and how they were resolved]
- [Or "None"]

Recommendations:
- [Suggestions for future feedback sessions]
- [Or "None"]

================================================================================
SESSION COMPLETE
================================================================================

All [N] changes applied successfully.

Review commands:
  git diff HEAD~1 content/physician-courses/[physician]/[course]/
  git log --oneline -5

Next steps:
  1. Review changes visually in preview system
  2. Run `npm run check` to verify TypeScript
  3. Commit changes when satisfied

================================================================================
