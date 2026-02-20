# NGM Brand Design System

Complete style guide for NextGeneration Medicine content and HTML rendering.

---

## Brand Identity

NextGeneration Medicine is a longevity medicine education platform targeting:
- Physicians entering the longevity space
- Health-conscious professionals
- Evidence-based practitioners

**Voice:** Authoritative yet accessible, evidence-based, clinically actionable.

---

## Color Palette

### Primary Colors
```css
--paper: #FFFFFF           /* Primary background */
--paper-alt: #FAFAF8       /* Secondary background, alternating sections */
--ink-900: #0A0B0C         /* Primary text, headings */
--ink-700: #1F2124         /* Strong emphasis, body text */
--ink-500: #5C626B         /* Secondary text */
--ink-400: #8B909A         /* Tertiary text, captions */
--line: #E5E3DE            /* Borders, dividers */
```

### Accent Colors
```css
--gold: #C5A572            /* Primary accent - use SPARINGLY */
--vermillion: #E03E2F      /* Active states, rare emphasis */
--green: #5C8A6B           /* Positive states, success */
--blue: #5C7A8A            /* Informational, neutral */
--purple: #7A6C8A          /* Special, advanced */
--orange: #D4845C          /* Warm accent, caution */
```

### Usage Guidelines
- Gold accent maximum 5-10% of visual area
- Vermillion only for critical emphasis
- Prefer ink colors for most elements
- Use paper-alt (#FAFAF8) for alternating sections

---

## Typography

### Headlines
```css
font-family: 'Newsreader', 'Noto Serif JP', serif;
font-weight: 500;
color: #0A0B0C;
```

**Sizes:**
- H1: clamp(40px, 5vw, 56px), line-height: 1.05
- H2: clamp(32px, 4vw, 42px), line-height: 1.2
- H3: clamp(24px, 3vw, 32px), line-height: 1.2

### Body Text
```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;
font-size: 15px;
line-height: 1.6;
color: #0A0B0C;
```

### Category Labels
```css
font-family: 'Inter', system-ui, sans-serif;
font-size: 11px;
font-weight: 600;
letter-spacing: 0.08em;
text-transform: uppercase;
color: #C5A572;
```

### Captions & Metadata
```css
font-family: 'Inter', system-ui, sans-serif;
font-size: 13px;
color: #5C626B;
font-style: italic;
```

---

## HTML Templates

### Lead Magnet Structure
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600&family=Noto+Serif+JP:wght@500&display=swap" rel="stylesheet">
  <title>{title}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #FFFFFF;">
  <div style="max-width: 900px; margin: 0 auto; padding: clamp(20px, 5vw, 48px);">
    <!-- Title -->
    <h1 style="font-family: 'Newsreader', serif; font-size: clamp(40px, 5vw, 56px); line-height: 1.05; font-weight: 500; color: #0A0B0C; margin-bottom: 32px;">
      {title}
    </h1>
    
    <!-- Subtitle -->
    <p style="font-family: 'Inter', sans-serif; font-size: 17px; line-height: 1.6; color: #5C626B; font-style: italic; margin-bottom: 48px;">
      {summary}
    </p>
    
    <!-- Content sections -->
    {content}
    
    <!-- Footer -->
    <footer style="margin-top: 72px; padding-top: 32px; border-top: 1px solid #E5E3DE; text-align: center;">
      <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #8B909A;">
        NextGeneration Medicine | Evidence-Based Longevity Education
      </p>
    </footer>
  </div>
</body>
</html>
```

### Section Template
```html
<section style="margin-top: 72px;">
  <h2 style="font-family: 'Newsreader', serif; font-size: clamp(32px, 4vw, 42px); line-height: 1.2; font-weight: 500; color: #1F2124; margin-bottom: 20px;">
    {heading}
  </h2>
  {content}
</section>
```

### Paragraph Template
```html
<p style="font-family: 'Inter', sans-serif; font-size: 15px; line-height: 1.6; color: #0A0B0C; margin-bottom: 20px;">
  {text}
</p>
```

### Alternating Background Section
```html
<div style="background-color: #FAFAF8; padding: 32px; border-radius: 4px; margin: 32px 0;">
  {content}
</div>
```

### SVG Container
```html
<figure style="margin: 32px 0; text-align: center;">
  {svg}
  <figcaption style="font-family: 'Inter', sans-serif; font-size: 13px; color: #5C626B; margin-top: 12px; font-style: italic;">
    {caption}
  </figcaption>
</figure>
```

### Mechanism Table
```html
<table style="width: 100%; border-collapse: collapse; margin: 32px 0; font-family: 'Inter', sans-serif;">
  <thead>
    <tr style="background-color: #0A0B0C;">
      <th style="padding: 14px 20px; text-align: left; color: #FFFFFF; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em;">Mechanism</th>
      <th style="padding: 14px 20px; text-align: left; color: #FFFFFF; font-weight: 600; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em;">Clinical Takeaway</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #E5E3DE;">
      <td style="padding: 16px 20px; color: #0A0B0C; font-size: 15px;">{mechanism}</td>
      <td style="padding: 16px 20px; color: #5C626B; font-size: 15px;">{takeaway}</td>
    </tr>
  </tbody>
</table>
```

### References Section
```html
<section style="margin-top: 72px; padding-top: 32px; border-top: 1px solid #E5E3DE;">
  <h3 style="font-family: 'Newsreader', serif; font-size: 24px; font-weight: 500; color: #1F2124; margin-bottom: 20px;">
    References
  </h3>
  <ol style="font-family: 'Inter', sans-serif; font-size: 13px; color: #5C626B; line-height: 1.8; padding-left: 20px;">
    <li>{reference}</li>
  </ol>
</section>
```

---

## Newsletter HTML (Email-Ready)

For newsletters, use table-based layout for email client compatibility.

### Email Container
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    @media only screen and (max-width: 620px) {
      .email-container { width: 100% !important; padding: 20px !important; }
      h1 { font-size: 26px !important; }
      h2 { font-size: 20px !important; }
      p, li { font-size: 16px !important; }
    }
  </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Georgia, serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 40px 20px;">
        <table role="presentation" class="email-container" cellspacing="0" cellpadding="0" style="background-color: #ffffff; width: 100%; max-width: 600px;">
          <tr>
            <td style="padding: 40px;">
              {content}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

### Email Typography (Inline Styles)

**Title:**
```html
<h1 style="font-family: Georgia, serif; font-size: 32px; line-height: 1.2; font-weight: 400; color: #1a1a1a; margin: 0 0 12px 0;">
```

**Subtitle:**
```html
<p style="font-family: Georgia, serif; font-size: 18px; line-height: 1.4; font-style: italic; color: #4a4a4a; margin: 0 0 24px 0;">
```

**Section Header:**
```html
<h2 style="font-family: Georgia, serif; font-size: 24px; line-height: 1.3; font-weight: 400; color: #1a1a1a; margin: 40px 0 16px 0;">
```

**Body Paragraph:**
```html
<p style="font-family: Georgia, serif; font-size: 18px; line-height: 1.7; color: #1a1a1a; margin: 0 0 20px 0;">
```

**Emphasis Paragraph (One-Sentence):**
```html
<p style="font-family: Georgia, serif; font-size: 18px; line-height: 1.7; color: #1a1a1a; margin: 24px 0; font-weight: 500;">
```

**Blockquote:**
```html
<blockquote style="margin: 24px 0; padding: 16px 24px; border-left: 3px solid #C5A572; background-color: #fafafa; font-style: italic;">
```

### SVG in Email
```html
<div style="margin: 32px 0; text-align: center; background-color: #fafafa; padding: 24px; border-radius: 4px;">
  <svg width="100%" style="max-width: 100%; height: auto;" viewBox="0 0 600 450" overflow="visible">
    ...
  </svg>
</div>
```

---

## Visual Style Principles

### Editorial Aesthetic
- Magazine-quality, not corporate
- Think: The Economist, NEJM, Nature, The Atlantic
- Sophisticated, intellectual, premium
- Clean hierarchy, generous whitespace

### Spacing
- Section margins: 72px top
- Paragraph margins: 20px bottom
- Container padding: clamp(20px, 5vw, 48px)
- Figure margins: 32px vertical

### Borders
- Use #E5E3DE for subtle dividers
- 1px solid for section breaks
- 4px border-radius for containers

### Key Terms
Highlight important terms with gold:
```html
<span style="color: #C5A572; font-weight: 600;">{term}</span>
```
