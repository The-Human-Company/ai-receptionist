# NGM Graphic Design Studio

Create professional graphic assets (banners, LinkedIn graphics, webinar promotions) with consistent NGM branding.

## What It Does

Graphic Design Studio generates visual marketing assets for Next Generation Medicine:
- **LinkedIn Banners** — Profile headers for personal/company pages
- **LinkedIn Posts** — Feed graphics, announcements, quote cards
- **Webinar Promos** — Event promotion graphics
- **Email Banners** — Newsletter headers
- **Social Stories** — Instagram/LinkedIn story graphics

All graphics follow the NGM editorial design system—gold accents, Newsreader/Inter fonts, clean visual hierarchy.

## Quick Start

### Create a LinkedIn Banner

```
Create a LinkedIn banner with the headline "Turning Science Into Strategy" and subtext "Founder, Next Generation Medicine"
```

The agent will:
1. Apply NGM branding and typography
2. Create an HTML file with exact dimensions (1584 × 396px)
3. Save to `content/graphics/linkedin-banner-[name].html`

### Create a Webinar Promo

```
Create a webinar promo for "GLP-1s in Longevity Medicine" on January 15, 2026 at 12pm EST
```

### Create a Quote Card

```
Create a quote card with: "The future of medicine isn't just about living longer—it's about living better." - Dr. Anant Vinjamoori
```

### Update an Existing Graphic

```
Update the LinkedIn banner to change the headline to "Building the Future of Longevity Medicine"
```

## What's Included

### Reference Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Core instructions, templates, workflows |
| Uses `document-studio/design-system.md` | Colors, typography, spacing |

### Templates

| Template | Dimensions | Use Case |
|----------|------------|----------|
| `linkedin-banner.html` | 1584 × 396px | Profile headers |
| `linkedin-post.html` | 1200 × 1200px | Feed posts |
| `webinar-promo.html` | 1920 × 1080px | Event promotion |
| `email-banner.html` | 600 × 200px | Newsletter headers |
| `quote-card.html` | 1080 × 1080px | Quote graphics |

## Design System

### Colors
- **Paper**: #FFFFFF (main background)
- **Ink-900**: #0A0B0C (headings, dark elements)
- **Gold**: #C5A572 (accent color, use sparingly)
- **Vermillion**: #E03E2F (CTA accent, rare)

### Typography
- **Headings**: Newsreader (serif)
- **Body**: Inter (sans-serif)
- **Labels**: Inter uppercase, tracked

## Output Format

Graphics are generated as HTML files that can be:
1. Opened in a browser for screenshot capture
2. Converted to PNG/JPG using Puppeteer
3. Used as web graphics directly

## Including Photos

When providing photos:
1. Place photo files in an accessible location
2. Reference the path in your request
3. The agent will incorporate with appropriate treatment (circles for portraits, overlays for backgrounds)

## MCP Integrations (Optional)

For enhanced capabilities, these MCPs can be integrated:

| MCP | Capability |
|-----|------------|
| **Replicate** | AI image generation for backgrounds/elements |
| **Canva API** | Template-based design automation |
| **Figma** | Design token extraction |
| **DALL-E** | AI image generation via OpenAI |

See `mcp-integrations.md` for setup instructions.

## Tips

1. **Keep it simple** — NGM design is editorial, not flashy
2. **Use gold sparingly** — Accent only, never large areas
3. **Embrace whitespace** — Generous margins improve readability
4. **Real photos** — Use actual photos of Dr. Vinjamoori, not AI-generated
5. **Test at size** — Ensure text is readable at target platform size

