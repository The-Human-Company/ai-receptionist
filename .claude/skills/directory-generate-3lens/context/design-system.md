# NGM Design System for Directory Pages

## Design Tokens (MUST USE)

### Typography
```css
font-serif: "Newsreader", Georgia, serif;
font-sans: "Inter", system-ui, sans-serif;
```

### Editorial Color Palette
```css
/* Backgrounds */
--paper: #FFFFFF;           /* Pure white background */
--paper-alt: #FAFAF8;       /* Warm off-white for diagram backgrounds */

/* Text Colors */
--ink-900: #0A0B0C;         /* Primary text, headings */
--ink-700: #1F2124;         /* Secondary text */
--ink-500: #5C626B;         /* Tertiary text, labels */
--ink-400: #8B909A;         /* Subtle text, annotations */

/* Borders */
--line: #E5E3DE;            /* Borders, dividers */

/* Accent Colors */
--gold: #C5A572;            /* Brand accent, highlights */
--vermillion: #E03E2F;      /* Warnings, negative states */
--green: #5C8A6B;           /* Positive states, success */
--blue: #5C7A8A;            /* Informational, neutral */
--purple: #7A6C8A;          /* Special, advanced */
--orange: #D4845C;          /* Warm accent, caution */
--yellow: #D4A84C;          /* Highlights, attention */
```

---

## SVG Diagram Requirements

### 1. Base Structure
Every diagram MUST be self-contained with:
- `viewBox` attribute for responsiveness
- Embedded `<style>` block with design tokens
- Maximum suggested height: 400px
- Background: `#FAFAF8` with `#E5E3DE` border

### 2. Required Style Block
```xml
<style>
  .diagram-title { font-family: "Newsreader", Georgia, serif; font-size: 18px; fill: #0A0B0C; font-weight: 500; }
  .diagram-label { font-family: "Inter", system-ui, sans-serif; font-size: 13px; fill: #1F2124; }
  .diagram-sublabel { font-family: "Inter", system-ui, sans-serif; font-size: 11px; fill: #5C626B; }
  .diagram-annotation { font-family: "Inter", system-ui, sans-serif; font-size: 10px; fill: #8B909A; font-style: italic; }
</style>
```

### 3. Standard Defs Block
```xml
<defs>
  <!-- Gradients -->
  <linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#6B8A9A"/>
    <stop offset="100%" stop-color="#5C7A8A"/>
  </linearGradient>
  <linearGradient id="goldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#D5B582"/>
    <stop offset="100%" stop-color="#C5A572"/>
  </linearGradient>
  <linearGradient id="greenGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#6C9A7B"/>
    <stop offset="100%" stop-color="#5C8A6B"/>
  </linearGradient>
  <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#8A7C9A"/>
    <stop offset="100%" stop-color="#7A6C8A"/>
  </linearGradient>
  <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#E4946C"/>
    <stop offset="100%" stop-color="#D4845C"/>
  </linearGradient>

  <!-- Drop Shadow -->
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0A0B0C" flood-opacity="0.1"/>
  </filter>

  <!-- Glow Effects -->
  <radialGradient id="glowGold" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#C5A572" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#C5A572" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowGreen" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#5C8A6B" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#5C8A6B" stop-opacity="0"/>
  </radialGradient>

  <!-- Arrow Marker -->
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
    <path d="M 0,0 L 10,5 L 0,10 Z" fill="#C5A572"/>
  </marker>
</defs>
```

---

## SVG Techniques for Visual Variety

### 1. Curved Paths (Organic Flow)
```xml
<path d="M 50,100 Q 150,50 250,100 T 450,100" stroke="#C5A572" fill="none" stroke-width="2"/>
```

### 2. Rounded Corners
```xml
<rect x="10" y="10" width="100" height="60" rx="12" ry="12" fill="#5C8A6B"/>
```

### 3. Icon Paths
```xml
<!-- Checkmark -->
<path d="M 5,12 L 10,17 L 20,7" stroke="#5C8A6B" stroke-width="2" fill="none" stroke-linecap="round"/>

<!-- Arrow -->
<path d="M 0,10 L 15,10 M 10,5 L 15,10 L 10,15" stroke="#C5A572" stroke-width="2" fill="none"/>

<!-- Warning triangle -->
<path d="M 10,2 L 18,16 L 2,16 Z" fill="none" stroke="#E03E2F" stroke-width="1.5"/>
```

### 4. Dashed/Dotted Lines
```xml
<line stroke-dasharray="5,5" ... />  <!-- dashed -->
<line stroke-dasharray="2,4" ... />  <!-- dotted -->
```

---

## Diagram Types & When to Use

| Concept Type | Diagram Style | Key Elements |
|--------------|---------------|--------------|
| Processes | Flowing curves with nodes | Bezier paths, rounded boxes, arrows |
| Comparisons | Radial/circular or split | Two circles, connecting arrows |
| Hierarchies | Isometric stacks/pyramids | Layered shapes with gradients |
| Networks | Connected nodes with glows | Radial gradients, dashed connections |
| Timelines | Horizontal with markers | Gradient line, milestone circles |
| Data/Metrics | Gauges, spectrums | Arc paths, color gradients |

---

## Diagram Design Principles

1. **Every diagram must be unique** - Never create generic box-and-arrow layouts
2. **Match concept to form**:
   - Comparisons → side-by-side, radial, or split layouts
   - Hierarchies → stacks, pyramids, trees
   - Networks → connected nodes with glows
   - Data → gauges, timelines, spectrums
3. **Use depth and dimension**:
   - Apply shadows to create elevation
   - Use gradients instead of flat colors
   - Layer elements for visual interest
4. **Maintain editorial restraint**:
   - Maximum 4-5 colors per diagram
   - Keep backgrounds subtle (paper-alt)
   - Use gold sparingly as accent
   - Ensure strong readability
5. **Responsive sizing**:
   - Always use viewBox for scaling
   - Keep text readable at smaller sizes
   - Test that labels don't overlap

---

## HTML Page Structure

### CSS Variables
```css
:root {
  /* Typography */
  --font-serif: "Newsreader", Georgia, serif;
  --font-sans: "Inter", system-ui, sans-serif;

  /* Colors */
  --paper: #FFFFFF;
  --paper-alt: #FAFAF8;
  --ink-900: #0A0B0C;
  --ink-700: #1F2124;
  --ink-500: #5C626B;
  --ink-400: #8B909A;
  --line: #E5E3DE;
  --gold: #C5A572;
  --vermillion: #E03E2F;
  --green: #5C8A6B;
  --blue: #5C7A8A;
  --purple: #7A6C8A;
  --orange: #D4845C;
  --yellow: #D4A84C;

  /* Spacing */
  --space-1: 8px;
  --space-2: 12px;
  --space-3: 20px;
  --space-4: 32px;
  --space-5: 48px;
  --space-6: 72px;
}
```

### Typography Scale
```css
h1 { font-family: var(--font-serif); font-size: 2.25rem; color: var(--ink-900); font-weight: 500; }
h2 { font-family: var(--font-serif); font-size: 1.5rem; color: var(--ink-900); font-weight: 500; }
h3 { font-family: var(--font-serif); font-size: 1.25rem; color: var(--ink-700); font-weight: 500; }
body { font-family: var(--font-sans); font-size: 16px; color: var(--ink-700); line-height: 1.6; }
.label { font-size: 13px; color: var(--ink-500); }
.annotation { font-size: 11px; color: var(--ink-400); font-style: italic; }
```

### Component Patterns

**Summary Box:**
```css
.summary-box {
  background: var(--paper-alt);
  border-left: 3px solid var(--gold);
  padding: var(--space-3);
  border-radius: 0 8px 8px 0;
}
```

**Cards:**
```css
.card {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: var(--space-3);
}
```

**Badges:**
```css
.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.badge-gold { background: var(--gold); color: white; }
.badge-green { background: var(--green); color: white; }
.badge-blue { background: var(--blue); color: white; }
```

**Diagram Container:**
```css
.diagram-container {
  background: var(--paper-alt);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: var(--space-3);
  margin: var(--space-4) 0;
}
```
