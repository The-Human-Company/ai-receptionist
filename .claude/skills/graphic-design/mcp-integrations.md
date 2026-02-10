# MCP Integrations for Graphic Design

This document covers Model Context Protocol (MCP) servers and API integrations that can enhance the Graphic Design Studio's capabilities for AI-generated elements and template-based automation.

---

## Overview

The hybrid approach combines:
1. **AI Image Generation** — Create backgrounds, abstract elements, decorative graphics
2. **Template Automation** — Fill pre-designed templates with data programmatically
3. **Design System Access** — Read design tokens and components from existing tools

```
┌─────────────────────────────────────────────────────────────────┐
│                     Graphic Design Agent                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│   │   Replicate  │    │  Canva API   │    │  Figma MCP   │    │
│   │     MCP      │    │              │    │              │    │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    │
│          │                   │                   │              │
│          ▼                   ▼                   ▼              │
│   AI-Generated         Template-Based       Design Token       │
│   Elements             Composition          Extraction         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Replicate MCP (Recommended)

**Purpose:** AI image generation using Flux, Stable Diffusion XL, and other models

**Status:** Community MCP available

**Best For:**
- Abstract backgrounds and textures
- Decorative elements and patterns
- Conceptual imagery for health/longevity themes
- Icon-style illustrations

### Installation

```json
{
  "mcpServers": {
    "replicate": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-replicate"],
      "env": {
        "REPLICATE_API_TOKEN": "your-replicate-api-token"
      }
    }
  }
}
```

### Getting an API Token

1. Create account at [replicate.com](https://replicate.com)
2. Go to Account Settings → API Tokens
3. Create a new token and add to your MCP config

### Recommended Models

| Model | Best For | Example Prompt |
|-------|----------|----------------|
| **flux-schnell** | Fast, high-quality images | General purpose |
| **flux-pro** | Premium quality | Important assets |
| **stable-diffusion-xl** | Versatile generation | Backgrounds |
| **ideogram** | Text in images | Logos, badges |

### NGM-Specific Prompts

**Abstract Background:**
```
Minimal abstract background for professional medical brand, 
soft gradient from cream (#FAFAF8) to warm white (#FFFFFF), 
subtle geometric lines in light gray, editorial design aesthetic, 
clean professional look, high resolution
```

**Medical/Longevity Theme:**
```
Abstract representation of cellular health and longevity, 
minimal elegant line art style, gold (#C5A572) and charcoal (#0A0B0C) 
accents on cream background, editorial medical illustration, 
sophisticated and clean
```

**Decorative Pattern:**
```
Elegant minimal decorative line pattern, thin gold lines, 
geometric shapes, isolated on transparent background, 
editorial design element, sophisticated and understated
```

---

## 2. DALL-E MCP (Alternative)

**Purpose:** AI image generation via OpenAI's DALL-E 3

**Status:** Community MCP available

**Best For:**
- Photorealistic conceptual imagery
- Complex scene compositions
- When Replicate quota is exhausted

### Installation

```json
{
  "mcpServers": {
    "openai-image": {
      "command": "npx",
      "args": ["-y", "mcp-server-openai-image"],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

### Considerations

- **Pros:** High quality, good at following complex prompts
- **Cons:** More expensive per image, slower than Flux
- **Note:** Text in images often has errors; render text as HTML instead

---

## 3. Canva Connect APIs

**Purpose:** Template-based design automation with professional output

**Status:** Official API (no native MCP yet, but can be integrated via custom tooling)

**Best For:**
- Professional template-based designs
- Brand kit integration
- Team collaboration on designs
- Print-ready outputs

### API Endpoints

| API | Purpose |
|-----|---------|
| **Design API** | Create and edit designs programmatically |
| **Autofill API** | Populate templates with dynamic data |
| **Export API** | Export to PNG, PDF, JPG |
| **Asset API** | Manage brand assets and images |
| **Brand Template API** | Access brand kit templates |

### Setup

1. Create a Canva Developer account at [canva.dev](https://canva.dev)
2. Create an application
3. Set up OAuth flow for user authorization
4. Use REST API endpoints directly

### Integration Pattern

Since Canva doesn't have a native MCP, you can:

1. **Use n8n/Zapier:** Create automation workflows that trigger Canva design generation
2. **Custom MCP Server:** Build a Node.js MCP server that wraps Canva APIs
3. **Direct API Calls:** Make HTTP requests to Canva APIs from your workflow

### Example: Custom MCP Server Structure

```typescript
// canva-mcp-server/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({
  name: "canva",
  version: "1.0.0",
});

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case "create_design":
      // Call Canva API to create design
      return await createCanvaDesign(args);
    case "autofill_template":
      // Call Canva Autofill API
      return await autofillTemplate(args);
    case "export_design":
      // Export design to image
      return await exportDesign(args);
  }
});
```

### Canva Brand Kit for NGM

When setting up Canva, create a Brand Kit with:

**Colors:**
- Paper: #FFFFFF
- Paper Alt: #FAFAF8
- Ink 900: #0A0B0C
- Ink 700: #1F2124
- Ink 500: #5C626B
- Gold: #C5A572
- Vermillion: #E03E2F

**Fonts:**
- Heading: Newsreader
- Body: Inter

**Logos:**
- NGM logo mark (N in square)
- Full wordmark

---

## 4. Figma MCP

**Purpose:** Extract design tokens, read existing designs, sync with design system

**Status:** Community MCP available

**Best For:**
- Extracting design tokens from existing Figma files
- Reading component specifications
- Syncing design system updates
- Getting exact color values, spacing, typography

### Installation

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-figma"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your-figma-personal-access-token"
      }
    }
  }
}
```

### Getting a Figma Token

1. Go to Figma → Settings → Account
2. Scroll to Personal Access Tokens
3. Generate a new token with appropriate permissions

### Use Cases

1. **Read Design Tokens:**
   - Extract exact color values from Figma styles
   - Get typography settings (font, size, weight, line-height)
   - Pull spacing values from components

2. **Component Specifications:**
   - Read component dimensions
   - Extract padding/margin values
   - Get border radius, shadows, etc.

3. **Asset Export:**
   - Export icons and graphics from Figma
   - Get SVG representations

---

## 5. Pixelixe API (Alternative)

**Purpose:** Template-based banner generation at scale

**Status:** REST API (no native MCP)

**Best For:**
- Bulk banner generation
- Social media graphics at scale
- Dynamic text/image replacement

### Features

- Template-based design system
- REST API for image generation
- Batch processing
- White-label editor embedding

### API Example

```bash
POST https://studio.pixelixe.com/api/1/generator

{
  "template_id": "your-template-id",
  "modifications": [
    {
      "name": "headline",
      "text": "Your Headline Here"
    },
    {
      "name": "image",
      "src": "https://example.com/photo.jpg"
    }
  ],
  "format": "png"
}
```

---

## 6. APITemplate.io (Alternative)

**Purpose:** REST API for banner and image generation

**Status:** REST API (no native MCP)

**Best For:**
- Simple banner generation
- E-commerce product images
- Social media images at scale

### Setup

1. Create account at [apitemplate.io](https://apitemplate.io)
2. Design templates in their editor
3. Use REST API to generate images

---

## Recommended Setup

For NGM Graphic Design Studio, we recommend this priority:

### Tier 1: Essential
1. **Replicate MCP** — For AI-generated backgrounds and elements
2. **HTML/CSS Templates** — Local templates (already created)

### Tier 2: Enhanced
3. **Canva API** — For complex template-based designs (requires setup)
4. **Figma MCP** — For design token synchronization

### Tier 3: Optional
5. **DALL-E MCP** — Alternative to Replicate
6. **Pixelixe/APITemplate** — For bulk generation needs

---

## Environment Setup

Create a `.env` file or configure your MCP settings:

```bash
# Replicate (required for AI generation)
REPLICATE_API_TOKEN=your-replicate-token

# OpenAI (optional, for DALL-E)
OPENAI_API_KEY=your-openai-key

# Figma (optional, for design sync)
FIGMA_ACCESS_TOKEN=your-figma-token

# Canva (optional, for template automation)
CANVA_CLIENT_ID=your-canva-client-id
CANVA_CLIENT_SECRET=your-canva-client-secret
```

---

## Workflow Examples

### Example 1: Create LinkedIn Banner with AI Background

1. **Generate background** using Replicate MCP with NGM prompt
2. **Compose layout** using HTML template
3. **Export** by opening in browser and taking screenshot

### Example 2: Create Webinar Promo with Canva

1. **Start from template** in Canva Brand Kit
2. **Autofill** with event details using API
3. **Export** to PNG using Canva Export API

### Example 3: Batch Generate Quote Cards

1. **Load quotes** from data source
2. **For each quote:**
   - Generate HTML from template
   - Export to PNG using Puppeteer
3. **Output** batch of images

---

## Converting HTML to Images

For the HTML templates, use one of these methods:

### Method 1: Browser Screenshot
```bash
# Open HTML file in browser, take screenshot at exact dimensions
# Works for quick one-off exports
```

### Method 2: Puppeteer Script
```javascript
const puppeteer = require('puppeteer');

async function htmlToImage(htmlPath, outputPath, width, height) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setViewport({ width, height });
  await page.goto(`file://${htmlPath}`);
  
  await page.screenshot({
    path: outputPath,
    clip: { x: 0, y: 0, width, height }
  });
  
  await browser.close();
}

// Usage
htmlToImage('templates/linkedin-banner.html', 'output/banner.png', 1584, 396);
```

### Method 3: html2canvas (Browser-based)
```javascript
import html2canvas from 'html2canvas';

html2canvas(document.querySelector('.canvas')).then(canvas => {
  const link = document.createElement('a');
  link.download = 'graphic.png';
  link.href = canvas.toDataURL();
  link.click();
});
```

---

## Resources

- [Replicate Documentation](https://replicate.com/docs)
- [Canva Connect APIs](https://www.canva.dev/docs/connect/)
- [Figma API Reference](https://www.figma.com/developers/api)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

