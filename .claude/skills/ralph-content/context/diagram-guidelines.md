# Diagram Generation Guidelines

Guidelines for creating SVG diagrams that look like they belong in Cell, Nature, or NEJM publications.

---

## Design Philosophy

Create diagrams that Andrew Huberman or Peter Attia would share on Instagram:
- Insightful perspectives that make hard concepts easy to grasp
- Balance between detailed and simple enough for social media
- Focus on ONE core insight per diagram
- Make the central thesis visually obvious
- Labels should be concise (1-4 words max)

---

## Diagram Types

Choose the most appropriate type for the concept being visualized.

### Mechanism Pathway
**For:** Biological processes, cause-effect chains, signaling cascades

**Structure:**
- Linear or branching flow
- Arrows indicating direction and causation
- Labeled nodes for each state/step
- Use gradients for depth

**Example elements:**
- Substrate → Enzyme → Product arrows
- Receptor → Signal cascade → Cellular response
- Gene → mRNA → Protein pathway

### Process Flow
**For:** Step-by-step sequences, workflows, timelines

**Structure:**
- Clear START and END points
- Numbered steps (3-6 ideal)
- Directional arrows between steps
- Horizontal or vertical layout

### Comparison (Side-by-Side)
**For:** Before/after, traditional vs. new, contrasting approaches

**Structure:**
- Two columns or panels clearly labeled
- Visual parallel between sides
- Contrasting colors to highlight differences
- Summary labels at bottom

**Critical sizing:**
- Each panel minimum 160px wide × 200px tall
- ALL labels must be INSIDE their colored box
- Calculate: (number of text lines × 25px) + 100px padding = minimum height

### Network/Hub
**For:** Interconnected concepts, ecosystems, multi-factor relationships

**Structure:**
- Central node with radiating connections
- Glowing nodes for emphasis
- Connection lines with labels
- Size indicates importance

### Timeline
**For:** Chronological events, treatment phases, historical progression

**Structure:**
- Horizontal progression line with gradient
- Circular markers at key points
- Labels above and below
- Color progression (can indicate change)

### Concept/Hierarchy
**For:** Abstract ideas, organizational structures, layered concepts

**Structure:**
- Pyramid, stacked layers, or tree structure
- Clear visual groupings
- Size/position shows importance
- Isometric view for depth

### Quadrant/Positioning Chart
**For:** Competitive landscapes, 2x2 matrices, strategic positioning

**Structure:**
- Two axes dividing space into 4 quadrants
- Items positioned by their coordinates on both dimensions
- Clear quadrant labels describing each zone
- "Best" items in visually superior position

**⚠️ CRITICAL: Axis Orientation Rules**

In SVG, y=0 is at the TOP of the canvas. This creates counterintuitive positioning:

| Desired Position | SVG Y Value |
|------------------|-------------|
| HIGH (visually at top) | LOW cy value (e.g., cy="120") |
| LOW (visually at bottom) | HIGH cy value (e.g., cy="380") |

**Standard axis conventions:**
- **Y-axis (vertical):** Values INCREASE going UP (higher = better should be at TOP = low cy)
- **X-axis (horizontal):** Values INCREASE going RIGHT (higher = right = high cx)

**Mandatory for quadrant diagrams:**
1. Add explicit "HIGH" and "LOW" labels on each axis
2. Position "best" items at the TOP (low cy values) if Y represents something desirable
3. Quadrant labels should match the positioning (top quadrants = high Y-value outcomes)

**Example - Outcome Focus axis:**
```svg
<!-- HIGH outcome focus = TOP of chart = low cy value -->
<text x="68" y="80">HIGH</text>
<circle cx="200" cy="130" .../>  <!-- High outcome focus item at TOP -->

<!-- LOW outcome focus = BOTTOM of chart = high cy value -->
<text x="68" y="430">LOW</text>
<circle cx="200" cy="350" .../>  <!-- Low outcome focus item at BOTTOM -->
```

**Self-check:** Before finalizing, ask: "If I drew this on paper with a pencil, would HIGH values be at the top?" If yes, those items need LOW cy values in SVG.

---

## DO NOT Create

- Bar charts, line graphs, pie charts, scatter plots
- Data visualizations with axes
- Generic stock-image style graphics
- Diagrams that require reading the full article to understand
- Overly complex diagrams with >7 main elements

---

## SVG Technical Requirements

### Required Structure

```svg
<svg viewBox="0 0 600 450" overflow="visible" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="100%" height="100%" fill="#FAFAF8" stroke="none"/>
  
  <!-- Content with 40px padding from all edges -->
  <!-- Bottom content should not exceed y=410 to maintain padding -->
</svg>
```

### Critical Rules

1. **viewBox:** Always use `viewBox="0 0 600 450"` for generous breathing room
2. **overflow:** Always set `overflow="visible"` to prevent clipping
3. **stroke:** Use `stroke="none"` attribute (NOT "stroke-none" which is INVALID)
4. **padding:** Maintain 40px padding from all viewBox edges
5. **contrast:** 4.5:1 minimum ratio (dark text on light backgrounds)

### Text Containment Rules (CRITICAL)

**ALL text that belongs to a container MUST be FULLY INSIDE that container:**

1. **No text straddling boundaries** - Text labels must be entirely within their colored box
2. **Minimum container padding** - All text inside a box must have at least 15px padding from ALL edges
3. **Size containers to fit text** - Make rectangles large enough to contain all text with padding
4. **Vertical stacking** - Multiple text lines stack vertically INSIDE the container
5. **External labels go OUTSIDE** - Labels describing a container from outside need 10px+ gap

**Container sizing formula:**
- Minimum height = (number of text lines × 25px) + 40px top padding + 40px bottom padding
- Minimum width = longest text line width + 30px left padding + 30px right padding

### Invalid SVG Attributes (DO NOT USE)
- ❌ `stroke-none` (use `stroke="none"`)
- ❌ `fill-none` (use `fill="none"`)
- ❌ Attributes without equals sign and quotes

---

## Color Palette (MUST USE)

```
/* BACKGROUNDS */
--paper: #FFFFFF           /* Pure white */
--paper-alt: #FAFAF8       /* Warm off-white - USE FOR SVG BACKGROUNDS */

/* TEXT & SHAPES */
--ink-900: #0A0B0C         /* Primary text, headings, key shapes */
--ink-700: #1F2124         /* Secondary text, body copy */
--ink-500: #5C626B         /* Tertiary text, labels */
--ink-400: #8B909A         /* Subtle text, annotations */

/* LINES & BORDERS */
--line: #E5E3DE            /* Borders, dividers, connecting lines */

/* ACCENTS (use sparingly - max 5-10% of visual area) */
--gold: #C5A572            /* Primary accent, highlights */
--vermillion: #E03E2F      /* Warnings, negative states, emphasis */
--green: #5C8A6B           /* Positive states, success, growth */
--blue: #5C7A8A            /* Informational, neutral, trust */
--purple: #7A6C8A          /* Special, advanced, premium */
--orange: #D4845C          /* Warm accent, caution, attention */
```

---

## Typography

### Title Text
```svg
<text
  font-family="'Newsreader', Georgia, serif"
  font-size="18"
  font-weight="500"
  fill="#1F2124"
  stroke="none">
  Diagram Title
</text>
```

### Label Text
```svg
<text
  font-family="'Inter', system-ui, sans-serif"
  font-size="13"
  fill="#0A0B0C"
  stroke="none"
  dominant-baseline="middle"
  text-anchor="middle">
  Label Text
</text>
```

### Category Labels (Uppercase)
```svg
<text
  font-family="'Inter', sans-serif"
  font-size="11"
  font-weight="600"
  letter-spacing="0.08em"
  fill="#C5A572"
  stroke="none">
  CATEGORY
</text>
```

---

## Visual Techniques

### Gradient Fills (for depth)
```svg
<defs>
  <linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#6B8A9A"/>
    <stop offset="100%" stop-color="#5C7A8A"/>
  </linearGradient>
</defs>
<rect fill="url(#blueGrad)" rx="8" .../>
```

### Drop Shadows (for elevation)
```svg
<defs>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0A0B0C" flood-opacity="0.1"/>
  </filter>
</defs>
<rect filter="url(#shadow)" .../>
```

### Rounded Corners
```svg
<rect x="10" y="10" width="100" height="60" rx="8" ry="8" fill="#5C8A6B" stroke="none"/>
```

### Dashed Lines (for relationships)
```svg
<line stroke-dasharray="5,5" stroke="#E5E3DE" stroke-width="1.5" .../>
```

---

## Horizontal Layout & Element Spacing (CRITICAL)

**The #1 cause of broken diagrams: overlapping elements in sequential layouts.**

When placing elements horizontally (e.g., Step 1 → Step 2 → Step 3), you MUST calculate positions mathematically to prevent overlap.

### The Overlap Problem

```
❌ WRONG - Elements overlap:
Box A: x=100, width=200 → ends at x=300
Box B: x=250, width=200 → starts at x=250 (OVERLAPS Box A by 50px!)

✅ CORRECT - Elements have gaps:
Box A: x=100, width=200 → ends at x=300
Arrow: x=300 to x=330
Box B: x=335, width=200 → starts at x=335 (35px gap for arrow)
```

### Mandatory Spacing Rules

1. **Calculate end position:** `element_end = x + width`
2. **Arrow gaps:** Leave 30-50px between element end and next element start for arrows
3. **Minimum gap without arrow:** 20px between adjacent elements
4. **Validate before rendering:** Ensure `element[n].x + element[n].width + gap < element[n+1].x`

### Sequential Layout Template

For 3-element horizontal flows in a 700px viewBox:

```svg
<!-- Element 1: x=30, width=150 → ends at 180 -->
<rect x="30" y="70" width="150" height="70"/>

<!-- Arrow 1: 180 → 215 (35px gap) -->
<line x1="180" y1="105" x2="210" y2="105"/>
<polygon points="215,105 205,100 205,110"/>

<!-- Element 2: x=220, width=220 → ends at 440 -->
<rect x="220" y="70" width="220" height="70"/>

<!-- Arrow 2: 440 → 475 (35px gap) -->
<line x1="440" y1="105" x2="470" y2="105"/>
<polygon points="475,105 465,100 465,110"/>

<!-- Element 3: x=480, width=180 → ends at 660 -->
<rect x="480" y="70" width="180" height="70"/>
```

### ViewBox Sizing for Horizontal Layouts

| # of Elements | Recommended viewBox Width |
|---------------|---------------------------|
| 2 elements    | 500-550px                 |
| 3 elements    | 650-700px                 |
| 4 elements    | 800-850px                 |

**Never assume 600px is enough for 3+ horizontal elements with arrows.**

### Text Centering in Boxes

When using `text-anchor="middle"`, the text centers on the x coordinate. Calculate the center of each box:

```
Box center x = box_x + (box_width / 2)

Example:
Box: x=220, width=220
Text should be at: x = 220 + (220/2) = 330
```

### Pre-Flight Checklist for Horizontal Layouts

Before writing SVG code, write out the math:

```
Element 1: x=___, width=___, ends at ___
Gap 1: ___ px
Element 2: x=___, width=___, ends at ___
Gap 2: ___ px
Element 3: x=___, width=___, ends at ___
Total width needed: ___
ViewBox width: ___ (must be > total + 40px padding)
```

If any element's start x is less than the previous element's end x, you have an overlap.

---

## Self-Validation Checklist

Before finalizing any diagram, verify:

1. [ ] viewBox is appropriately sized (600×450 for simple, 700+ width for 3+ horizontal elements)
2. [ ] Background rect fills with #FAFAF8
3. [ ] All text has 40px+ padding from viewBox edges
4. [ ] All text inside containers is FULLY contained with 15px+ padding
5. [ ] No text straddles container boundaries
6. [ ] All shapes have explicit `stroke="none"` unless borders intentional
7. [ ] Gold accent (#C5A572) is ≤10% of visual area
8. [ ] All text has adequate contrast (4.5:1 minimum)
9. [ ] Diagram makes sense without reading the article
10. [ ] Uses only NGM palette colors
11. [ ] **AXIS ORIENTATION (for quadrant/positioning diagrams):** Items with HIGH values on Y-axis are positioned at TOP of chart (LOW cy values). Ask: "On paper, would 'better' be higher up?" If yes, those items need lower cy values.
12. [ ] **HORIZONTAL OVERLAP CHECK:** For sequential layouts, verify math: `element[n].x + element[n].width + 30 < element[n+1].x`. No element should start before the previous one ends + gap.

If any check fails, regenerate with specific corrections.

---

## Common Mistakes to Avoid

**❌ Text spilling below container:**
```svg
<rect x="100" y="100" width="150" height="120" fill="#5C8A6B"/>
<text y="210">Subtitle</text>  <!-- y=210 is OUTSIDE the box (100+120=220) -->
```

**✅ Text fully contained:**
```svg
<rect x="100" y="100" width="150" height="180" fill="#5C8A6B"/>
<text y="130">Label</text>      <!-- 30px inside top -->
<text y="160">Subtitle</text>   <!-- Still inside -->
<text y="190">Description</text> <!-- 90px from bottom = safe -->
```

**❌ External label on the edge:**
```svg
<text y="100">Consumer</text>  <!-- ON the top edge - ambiguous -->
<rect x="100" y="100" width="150" height="150" fill="#5C8A6B"/>
```

**✅ External label clearly above with gap:**
```svg
<text y="80">Consumer</text>  <!-- 20px gap before box -->
<rect x="100" y="100" width="150" height="150" fill="#5C8A6B"/>
```

**❌ Horizontal elements overlapping (THE MOST COMMON BUG):**
```svg
<!-- Box A ends at x=460 but Box B starts at x=400 - OVERLAP! -->
<rect x="260" y="70" width="200" height="70"/>  <!-- ends at 460 -->
<rect x="400" y="70" width="160" height="70"/>  <!-- starts at 400, overlaps by 60px -->
```

**✅ Horizontal elements properly spaced:**
```svg
<!-- Box A ends at x=440, gap of 40px, Box B starts at x=480 -->
<rect x="220" y="70" width="220" height="70"/>  <!-- ends at 440 -->
<!-- Arrow fills gap: 440 to 475 -->
<rect x="480" y="70" width="180" height="70"/>  <!-- starts at 480, no overlap -->
```

**The fix:** Always calculate: `next_element.x > prev_element.x + prev_element.width + arrow_gap`
