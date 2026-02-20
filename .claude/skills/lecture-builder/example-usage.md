# Lecture Builder Skill - Example Usage

## How to Use This Skill

The `lecture-builder` skill is automatically invoked by Claude Code when you request to build or create a lecture file.

### Example Request

```
Hey Claude, I need to build a new lecture. Here are the details:

Title: "Transformers in Medical Imaging"
Descript iframe: <iframe src="https://share.descript.com/view/abc123" width="100%" height="500"></iframe>
Output location: /lectures/ai-radiology/transformers-imaging.html
Content file: /input/transformers-content.html

Please create the lecture following the standard format.
```

### What Claude Will Do

1. **Read** the content from `/input/transformers-content.html`
2. **Extract and structure** the content into the JSON format with:
   - Meta information (track, subtrack, tags, abstract)
   - Video section with the Descript iframe
   - 5-7 content sections covering key topics
   - Key Mechanisms table
   - Implementation Pathway
   - The Path Forward
   - References
3. **Generate** the lecture file at the output location
4. **Validate** that the structure matches existing lectures

### Automatic Invocation

The skill is triggered automatically when you:
- Ask to "build a lecture"
- Request to "create a new lecture file"
- Want to "convert HTML content to lecture format"
- Need to "format a lecture consistently"

### Manual Invocation

You can also explicitly invoke the skill using:
```
/skill lecture-builder
```

Then provide the required inputs (title, iframe, output location, content file).

## Example Output Structure

The skill will generate an HTML file structured like this:

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="track" content="AI in Medicine">
  <meta name="subtrack" content="Radiology">
  <title>Transformers in Medical Imaging</title>
  <!-- Additional meta tags -->
</head>
<body>
  <!-- Header with title and meta info -->

  <!-- Video Section -->
  <section class="video-lecture">
    <iframe src="https://share.descript.com/view/abc123"></iframe>
    <p>Watch the full lecture here.</p>
  </section>

  <!-- Content Sections (5-7) -->
  <section id="fundamental-shift">
    <h2>The Fundamental Shift</h2>
    <!-- Content paragraphs -->
  </section>

  <!-- Additional sections -->

  <!-- Key Mechanisms Table -->
  <section id="mechanisms-table">
    <h2>Key Mechanisms and Clinical Takeaways</h2>
    <table>
      <!-- Structured table content -->
    </table>
  </section>

  <!-- Implementation Pathway -->
  <section id="implementation">
    <h2>Implementation Pathway</h2>
    <!-- Structured implementation steps -->
  </section>

  <!-- The Path Forward -->
  <section id="path-forward">
    <h2>The Path Forward</h2>
    <!-- Conclusion content -->
  </section>

  <!-- References -->
  <section id="references">
    <h2>References</h2>
    <ol>
      <li>Reference 1</li>
      <li>Reference 2</li>
    </ol>
  </section>
</body>
</html>
```

## Tips for Best Results

1. **Prepare your HTML content file** with clear headings and well-structured text
2. **Provide complete meta information** (track, duration, tags) upfront if available
3. **Include all references** in the source content for proper citation
4. **Check existing lectures** in your project to ensure styling consistency
5. **Review the output** to verify the structure matches your expectations

## Maintaining Consistency

The skill ensures every lecture has:
- ✅ Identical structural format
- ✅ Same section ordering
- ✅ Consistent styling and CSS classes
- ✅ Uniform video embed placement
- ✅ Standardized table format
- ✅ Matching implementation pathway structure
- ✅ Identical reference formatting

This guarantees all lectures on your website have a professional, cohesive appearance.
