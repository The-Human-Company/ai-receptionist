# Lecture Builder Skill

## Overview
This skill creates lecture files with **strict, consistent formatting** for the NextGenMed website. All lectures follow the same structure to ensure uniformity across the educational platform.

## Skill Files
- `SKILL.md` - Main skill definition and instructions
- `templates/lecture-structure.json` - JSON structure template
- `templates/lecture-template.tsx` - TSX component template
- `example-usage.md` - Usage guide and examples
- `README.md` - This file

## Lecture Structure
Every lecture **must** follow this exact sequence:

1. **Meta** (track, subtrack, title, duration, tags, abstract)
2. **Header** (generated from meta)
3. **Video Lecture** (Descript iframe embed)
4. **5-7 Content Sections** (text-based educational content):
   - The Fundamental Shift
   - How [Core Concept] Works
   - Clinical Performance Evidence
   - [Domain] Applications
   - Additional sections as needed
5. **Key Mechanisms Table** (structured clinical takeaways)
6. **Implementation Pathway** (practical application steps)
7. **The Path Forward** (conclusion and next steps)
8. **References** (numbered citations)

## Usage

### Automatic Invocation
Simply ask Claude Code to:
- "Build a new lecture about [topic]"
- "Create a lecture file for [title]"
- "Convert this HTML content to a lecture"

### Provide These Inputs
When building a lecture, provide:

1. **Title**: The lecture title
2. **Descript iframe**: Video embed code
   ```html
   <iframe src="https://share.descript.com/embed/..." width="100%" height="500"></iframe>
   ```
3. **Output location**: File path where the lecture should be saved
   ```
   /client/src/pages/mentorship/lectures/YourLectureTitle.tsx
   ```
4. **HTML content file**: Path to the HTML file containing the lecture content
   ```
   /input/your-lecture-content.html
   ```

### Example Request
```
Hey Claude, I need to build a new lecture:

Title: "Transformers in Medical Imaging"
Descript iframe: <iframe src="https://share.descript.com/embed/abc123"></iframe>
Output location: client/src/pages/mentorship/lectures/TransformersImaging.tsx
Content file: input/transformers-content.html

Please create the lecture following the standard format.
```

## Consistency Guarantees
The skill ensures:
- ✅ Identical structural format across all lectures
- ✅ Same section ordering
- ✅ Consistent styling (TailwindCSS classes)
- ✅ Uniform video embed placement
- ✅ Standardized table format
- ✅ Matching implementation pathway structure
- ✅ Identical reference formatting

## Technical Details

### Component Structure
- React TypeScript component
- Uses `MentorshipAccessGate` for access control
- Imports from:
  - `wouter` for routing
  - `lucide-react` for icons
  - `@/components/layout` for Navbar/Footer

### Styling
- TailwindCSS utility classes
- Consistent color scheme:
  - Headers: gradient from indigo-50 via purple-50 to blue-50
  - Section headings: border-b-2 border-blue-500
  - Table headers: bg-blue-600 text-white
  - Even rows: even:bg-gray-50

### Required Sections
All lectures must include these exact H2 headings in order:
1. Video Lecture
2. The Fundamental Shift
3. How [Concept] Works
4. Clinical Performance Evidence
5. [Domain] Applications
6. Key Mechanisms and Clinical Takeaways (table)
7. Implementation Pathway
8. The Path Forward

## Validation
Before marking a lecture as complete, verify:
- [ ] All required sections are present
- [ ] Sections are in the correct order
- [ ] Video iframe is properly embedded
- [ ] Table has three columns
- [ ] Implementation steps use bold labels
- [ ] References are numbered
- [ ] Component name matches file name
- [ ] All imports are correct

## Tips
1. **Prepare content files** with clear headings matching the required structure
2. **Provide complete meta information** upfront if available
3. **Include all references** in the source content
4. **Check existing lectures** for styling consistency (e.g., IntroClaude45HealthcareAI.tsx)
5. **Review the output** to ensure it matches the template

## Maintenance
When updating this skill:
1. Check recent lectures for any new patterns
2. Update the template if structure changes
3. Test with a sample lecture to verify output
4. Update this README with any new requirements
