# Lecture Iteration Changelog

================================================================================
SESSION METADATA
================================================================================

Session ID:     iter-2026-01-17-dr-robin-rose-gut-microbiome
Physician:      Dr. Robin Rose (dr-robin-rose)
Course:         gut-microbiome
Lecture:        lecture-1.json
Started:        2026-01-17T00:00:00.000Z
Completed:      2026-01-17T00:30:00.000Z

Feedback Source: Inline text feedback with image references
Feedback Summary: 14 changes across slides 1, 5, 7, 11, 12, 13, 15, 16 + new references slide

================================================================================
SUMMARY STATISTICS
================================================================================

Total Changes:  14
- Content Edits:       11
- Image Additions:     2
- New Slide:           1

Files Modified:
| File | Changes | Status |
|------|---------|--------|
| lecture-1.json | 14 | Complete |

Quality Gates:
✓ All JSON files valid (18 slides verified)
✓ All changes logged
✓ No errors encountered

================================================================================
CHANGE LOG
================================================================================

--- CHANGE 001 | Slide 1 | content_edit ---
Target: learning-objectives slide, numbered items[0]
Description: Updated learning objective #1 text
Before: "Understand the gut-lung axis and how SARS-CoV-2 directly affects the gastrointestinal tract through ACE2 receptors"
After: "Understand the mechanistic pathways driving dysbiosis, intestinal permeability, and persistent symptoms"
Status: APPLIED

--- CHANGE 002 | Slide 5 | image_addition ---
Target: gut-ground-zero slide
Description: Added electron micrograph image reference
Added: imageUrl: "/assets/ElectronMicrograph.jpeg"
Added: imageCaption: "Electron micrograph showing SARS-CoV-2 virions inside gut bacteria (Brogna et al.)"
Status: APPLIED

--- CHANGE 003 | Slide 7 | image_addition ---
Target: three-spike-origins slide
Description: Added spike protein origins graphic
Added: imageUrl: "/assets/SpikePhoto.jpeg"
Added: imageCaption: "Three origins of spike protein: from the virus (wild type), from the vaccine (mRNA), and from bacteria (bacteriophage activity)"
Status: APPLIED

--- CHANGE 004 | Slide 7 | content_edit ---
Target: three-spike-origins slide, highlight block
Description: Updated mass spectrometry detection text
Before: "Our Wellness Journey testing can detect actual spike protein (not just antibodies), differentiate between bacterial and human origin, and identify toxin-like peptides."
After: "Through mass spectrometry the following can be detected: actual spike protein (not the antibody) and differentiate between spike protein from virus vs. vaccine, differentiate between spike protein from bacterial and human origin, and identify toxin-like peptides."
Status: APPLIED

--- CHANGE 005 | Slide 7 | content_addition ---
Target: three-spike-origins slide, before bullets block
Description: Added study publication sentence
Added: Paragraph block with text about Journal of Mass Spectrometry pending publication
Status: APPLIED

--- CHANGE 006 | Slide 11 | content_edit ---
Target: diagnostic-biomarkers slide, bullets item
Description: Changed sequencing method from 16S rRNA to Shotgun Metagenomics
Before: "16S rRNA sequencing for bacterial composition"
After: "Shotgun Metagenomics sequencing for bacterial composition"
Status: APPLIED

--- CHANGE 007 | Slide 12 | content_edit ---
Target: therapeutic-overview slide, comparisonText Phase 1
Description: Updated Phase 1 detox description
Before: "Gentle detox pathways, eliminate bacteriophages, seal gut barrier"
After: "Administer oral gentle detox, eliminate bacteriophages, seal gut barrier"
Status: APPLIED

--- CHANGE 008 | Slide 13 | content_edit ---
Target: phase-1-detox slide, numbered item 3
Description: Expanded Vedicinals 9 mechanisms
Added: ", block the receptor binding domain, and inhibit the furin cleavage site"
Status: APPLIED

--- CHANGE 009 | Slide 13 | content_edit ---
Target: phase-1-detox slide, numbered item 4
Description: Updated Ozonated Glycerin virus coverage
Before: "active against lipid-enveloped viruses"
After: "active against lipid-enveloped and non lipid-enveloped viruses"
Status: APPLIED

--- CHANGE 010 | Slide 15 | content_edit ---
Target: phase-2-restoration slide, bullets item
Description: Updated Omega-3 description for gut focus
Before: "Plant-based omega-3/6/9 for inflammatory balance"
After: "Plant-based omega-3/6/9 influence the gut microbiome, reduce inflammation, strengthen the gut barrier, and promote the growth of beneficial bacteria"
Status: APPLIED

--- CHANGE 011 | Slide 15 | content_edit ---
Target: phase-2-restoration slide, bullets item
Description: Updated Magnesium description for gut focus
Before: "Magnesium Glycinate: Supports muscles, energy production, nervous system"
After: "Magnesium: Activates digestive enzymes, reduces gut inflammation, and supports a balanced gut microbiome"
Status: APPLIED

--- CHANGE 012 | Slide 16 | content_edit ---
Target: phase-3-probiotics slide, bullets item
Description: Updated B-Complex description for gut microbiome
Before: "B-Complex #12: Metabolic support, energy, mental health"
After: "B-Complex: Act as essential cofactors for gut bacteria metabolism, influence microbial diversity and function, help maintain the gut barrier, and promote beneficial bacteria like Faecalibacterium prausnitzii"
Status: APPLIED

--- CHANGE 013 | New Slide | structure_change ---
Target: End of slides array
Description: Added new references slide
Added: Slide "references-slide" with title "References and Further Reading"
Content: Intro paragraph, 8 numbered references, highlight block, clinical note callout
Status: APPLIED

================================================================================
SESSION 2 - Additional Iterations (2026-01-17)
================================================================================

--- CHANGE 014 | Slide 12 | diagram_update ---
Target: therapeutic-overview slide, diagramHtml SVG
Description: Removed "5-7 days" duration text from Phase 1 box
Before: `<text x=\"140\" y=\"230\" ...>5-7 days</text>`
After: (removed)
Status: APPLIED

--- CHANGE 015 | Slide 12 | diagram_update ---
Target: therapeutic-overview slide, diagramHtml SVG
Description: Removed "7 days+" duration text from Phase 2 box
Before: `<text x=\"350\" y=\"230\" ...>7 days+</text>`
After: (removed)
Status: APPLIED

--- CHANGE 016 | Slide 12 | diagram_update ---
Target: therapeutic-overview slide, diagramHtml SVG
Description: Removed "Ongoing" duration text from Phase 3 box
Before: `<text x=\"560\" y=\"230\" ...>Ongoing</text>`
After: (removed)
Status: APPLIED

--- CHANGE 017 | New Slide | structure_change ---
Target: slides[0] (new first slide)
Description: Added instructor bio slide with Dr. Rose photo and biography
Slide ID: instructor-bio
Title: "Meet Your Instructor: Dr. Robin Rose"
Image: /assets/physician-headshots/dr-robin-rose.jpg
Content: 5 paragraph/highlight blocks with full biography
Callout: Clinical note with credentials
Status: APPLIED

Additional Actions:
- Created directory: public/assets/physician-headshots/
- Copied headshot: src/assets/JGP_9995 (2).jpg → public/assets/physician-headshots/dr-robin-rose.jpg

================================================================================
END OF CHANGELOG
================================================================================

