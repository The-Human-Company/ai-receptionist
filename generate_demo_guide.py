"""
Generate a professional PDF Demo Guide for the Equity Insurance AI Receptionist.
Includes full live demo scripts with dialogue.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

# ── Colors ──
DARK_BG = HexColor("#09090b")
SURFACE = HexColor("#18181b")
PRIMARY = HexColor("#3b82f6")
PRIMARY_DARK = HexColor("#1e3a5f")
ACCENT = HexColor("#f59e0b")
SUCCESS = HexColor("#10b981")
DANGER = HexColor("#ef4444")
ORANGE = HexColor("#f97316")
PURPLE = HexColor("#8b5cf6")
ZINC_200 = HexColor("#e4e4e7")
ZINC_300 = HexColor("#d4d4d8")
ZINC_400 = HexColor("#a1a1aa")
ZINC_500 = HexColor("#71717a")
ZINC_600 = HexColor("#52525b")
ZINC_700 = HexColor("#3f3f46")
ZINC_800 = HexColor("#27272a")
WHITE = HexColor("#ffffff")
LIGHT_BG = HexColor("#f4f4f5")
CARD_BG = HexColor("#fafafa")

# ── Styles ──
styles = {
    "title": ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=28, leading=34,
        textColor=PRIMARY_DARK, spaceAfter=4,
    ),
    "subtitle": ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=13, leading=18,
        textColor=ZINC_500, spaceAfter=20,
    ),
    "h1": ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=20, leading=26,
        textColor=DARK_BG, spaceBefore=20, spaceAfter=8,
    ),
    "h2": ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=14, leading=20,
        textColor=PRIMARY_DARK, spaceBefore=14, spaceAfter=6,
    ),
    "h3": ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=11, leading=16,
        textColor=ZINC_600, spaceBefore=10, spaceAfter=4,
    ),
    "body": ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10, leading=15,
        textColor=HexColor("#333333"), spaceAfter=6,
    ),
    "body_bold": ParagraphStyle(
        "body_bold", fontName="Helvetica-Bold", fontSize=10, leading=15,
        textColor=HexColor("#333333"), spaceAfter=6,
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=10, leading=15,
        textColor=HexColor("#333333"), leftIndent=20, spaceAfter=3,
        bulletIndent=8,
    ),
    "small": ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8.5, leading=13,
        textColor=ZINC_500, spaceAfter=4,
    ),
    "mono": ParagraphStyle(
        "mono", fontName="Courier", fontSize=9, leading=14,
        textColor=ZINC_600, leftIndent=16, spaceAfter=6,
    ),
    "footer": ParagraphStyle(
        "footer", fontName="Helvetica", fontSize=7, leading=10,
        textColor=ZINC_400, alignment=TA_CENTER,
    ),
    "step_num": ParagraphStyle(
        "step_num", fontName="Helvetica-Bold", fontSize=22, leading=26,
        textColor=PRIMARY, alignment=TA_CENTER,
    ),
    "step_title": ParagraphStyle(
        "step_title", fontName="Helvetica-Bold", fontSize=11, leading=16,
        textColor=DARK_BG, spaceAfter=2,
    ),
    "step_body": ParagraphStyle(
        "step_body", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=ZINC_600, spaceAfter=4,
    ),
    # Script dialogue styles
    "ai_label": ParagraphStyle(
        "ai_label", fontName="Helvetica-Bold", fontSize=9, leading=13,
        textColor=PRIMARY, spaceBefore=8, spaceAfter=1,
    ),
    "ai_text": ParagraphStyle(
        "ai_text", fontName="Helvetica-Oblique", fontSize=9.5, leading=14,
        textColor=ZINC_600, leftIndent=12, spaceAfter=4,
    ),
    "you_label": ParagraphStyle(
        "you_label", fontName="Helvetica-Bold", fontSize=9, leading=13,
        textColor=HexColor("#059669"), spaceBefore=6, spaceAfter=1,
    ),
    "you_text": ParagraphStyle(
        "you_text", fontName="Helvetica-Bold", fontSize=9.5, leading=14,
        textColor=HexColor("#333333"), leftIndent=12, spaceAfter=4,
    ),
    "watch": ParagraphStyle(
        "watch", fontName="Helvetica-Oblique", fontSize=8.5, leading=13,
        textColor=ACCENT, leftIndent=12, spaceAfter=6, spaceBefore=2,
    ),
}


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(PRIMARY)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, h - 0.6 * inch, w - 0.75 * inch, h - 0.6 * inch)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(PRIMARY)
    canvas.drawString(0.75 * inch, h - 0.55 * inch, "EQUITY INSURANCE")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(ZINC_400)
    canvas.drawRightString(w - 0.75 * inch, h - 0.55 * inch, "AI Receptionist Demo Guide")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(ZINC_400)
    canvas.drawCentredString(w / 2, 0.45 * inch, f"Equity Insurance Inc. \u2014 Honolulu, HI  |  equityinsurance.services  |  Page {doc.page}")
    canvas.setStrokeColor(HexColor("#e4e4e7"))
    canvas.setLineWidth(0.3)
    canvas.line(0.75 * inch, 0.6 * inch, w - 0.75 * inch, 0.6 * inch)
    canvas.restoreState()


def first_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setFillColor(PRIMARY)
    canvas.rect(0, h - 8, w, 8, fill=1, stroke=0)
    canvas.setFillColor(PRIMARY)
    canvas.roundRect(0.75 * inch, h - 2.1 * inch, 50, 50, 10, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawCentredString(0.75 * inch + 25, h - 2.05 * inch + 14, "EI")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(ZINC_400)
    canvas.drawCentredString(w / 2, 0.45 * inch, "Equity Insurance Inc. \u2014 Honolulu, HI  |  equityinsurance.services")
    canvas.setStrokeColor(HexColor("#e4e4e7"))
    canvas.setLineWidth(0.3)
    canvas.line(0.75 * inch, 0.6 * inch, w - 0.75 * inch, 0.6 * inch)
    canvas.restoreState()


def colored_box(text, bg_color, text_color=WHITE):
    style = ParagraphStyle("box", fontName="Helvetica", fontSize=9.5, leading=14, textColor=text_color)
    t = Table([[Paragraph(text, style)]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    return t


def step_row(num, title, body):
    num_p = Paragraph(str(num), styles["step_num"])
    title_p = Paragraph(title, styles["step_title"])
    body_p = Paragraph(body, styles["step_body"])
    content = Table([[title_p], [body_p]], colWidths=[5.8 * inch])
    content.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    t = Table([[num_p, content]], colWidths=[0.6 * inch, 5.9 * inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
    ]))
    return t


def demo_header(num, title, mode, color=PRIMARY):
    """Create a demo scenario header bar."""
    style = ParagraphStyle("dh", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=WHITE)
    mode_style = ParagraphStyle("dm", fontName="Helvetica", fontSize=9, leading=13, textColor=HexColor("#dbeafe"))
    t = Table([
        [Paragraph(f"DEMO {num}: {title}", style)],
        [Paragraph(f"Mode: {mode}", mode_style)],
    ], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('TOPPADDING', (0, 0), (0, 0), 10),
        ('BOTTOMPADDING', (0, -1), (0, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
    ]))
    return t


def ai_says(text):
    return Paragraph(f'<b>AI:</b> <i>"{text}"</i>', styles["ai_text"])


def you_say(text):
    return Paragraph(f'<b>YOU:</b> "{text}"', styles["you_text"])


def watch(text):
    return Paragraph(f'\u25b6 {text}', styles["watch"])


def divider():
    return HRFlowable(width="100%", thickness=0.3, color=HexColor("#e4e4e7"), spaceBefore=6, spaceAfter=6)


def build():
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "AI-Receptionist-Demo-Guide.pdf"
    )
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.75 * inch,
    )

    story = []

    # ════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════
    story.append(Spacer(1, 1.6 * inch))
    story.append(Paragraph("AI Receptionist", styles["title"]))
    story.append(Paragraph("Demo Guide", ParagraphStyle(
        "t2", fontName="Helvetica-Bold", fontSize=28, leading=34, textColor=PRIMARY, spaceAfter=8,
    )))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="30%", thickness=2, color=PRIMARY, spaceAfter=12))
    story.append(Paragraph(
        "A complete walkthrough with live demo scripts for demonstrating the AI-powered "
        "phone receptionist for Equity Insurance Inc. \u2014 Honolulu, Hawaii.",
        styles["subtitle"]
    ))
    story.append(Spacer(1, 20))

    info_data = [
        ["Client", "Equity Insurance Inc."],
        ["Location", "Honolulu, HI"],
        ["Main Line", "+1 (808) 593-7746"],
        ["Tech Stack", "VAPI.ai  +  n8n  +  ElevenLabs  +  Google Sheets"],
        ["Version", "Production Pilot"],
    ]
    info_table = Table(info_data, colWidths=[1.4 * inch, 4.6 * inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), ZINC_500),
        ('TEXTCOLOR', (1, 0), (1, -1), HexColor("#333333")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, HexColor("#e4e4e7")),
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════
    story.append(Paragraph("Contents", styles["h1"]))
    story.append(Spacer(1, 6))
    toc = [
        ("1.", "Getting Started"),
        ("2.", "Dashboard Layout"),
        ("3.", "Demo 1 \u2014 New Customer (Auto Insurance)"),
        ("4.", "Demo 2 \u2014 Existing Customer"),
        ("5.", "Demo 3 \u2014 Filing a Claim"),
        ("6.", "Demo 4 \u2014 Hot Lead (High-Value Property)"),
        ("7.", "Demo 5 \u2014 Disqualified Caller"),
        ("8.", "Demo 6 \u2014 After Hours Call"),
        ("9.", "What to Watch For During Demos"),
        ("10.", "Business Rules Reference"),
        ("11.", "Tips &amp; Troubleshooting"),
    ]
    for num, item in toc:
        story.append(Paragraph(
            f'<b>{num}</b>&nbsp;&nbsp;&nbsp;{item}',
            ParagraphStyle("toc", fontName="Helvetica", fontSize=11, leading=22, textColor=HexColor("#333333"))
        ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 1. GETTING STARTED
    # ════════════════════════════════════════
    story.append(Paragraph("1. Getting Started", styles["h1"]))
    story.append(Spacer(1, 6))
    story.append(step_row("1", "Open the Demo App",
        "Navigate to the AI Receptionist web app in <b>Google Chrome</b> (recommended). "
        "The app can also be opened locally by double-clicking <b>vapi-web-test.html</b>."))
    story.append(step_row("2", "Allow Microphone Access",
        "When prompted by the browser, click <b>Allow</b>. The AI cannot hear you without microphone permission."))
    story.append(step_row("3", "Wait for SDK to Load",
        'Look for <b>"VAPI SDK loaded successfully"</b> in the System Logs panel (bottom-right). This takes 1-2 seconds.'))
    story.append(step_row("4", "Choose Mode",
        "Select <b>Business Hours</b> or <b>After Hours</b> using the toggle in the top-left corner."))
    story.append(step_row("5", "Start the Call",
        "Click the large <b>white phone button</b> at the bottom of the left panel. Wait for the AI greeting."))
    story.append(step_row("6", "End the Call",
        "Click the <b>red phone button</b> to end the call. Press the <b>refresh icon</b> to reset everything."))

    story.append(Spacer(1, 10))
    story.append(colored_box(
        "<b>Requirements:</b> Chrome browser, microphone, speakers/headphones, stable internet connection.",
        PRIMARY_DARK,
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 2. DASHBOARD LAYOUT
    # ════════════════════════════════════════
    story.append(Paragraph("2. Dashboard Layout", styles["h1"]))
    story.append(Paragraph(
        "The dashboard has three panels plus a top navigation bar.",
        styles["body"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Top Navigation Bar", styles["h2"]))
    for item in [
        "<b>Logo &amp; Branding</b> \u2014 Equity Insurance shield with \"AI RECEPTIONIST\" label",
        "<b>Environment Badge</b> \u2014 Shows \"Production\" indicator",
        "<b>Connection Status</b> \u2014 Disconnected / Connecting / Connected / AI Speaking / Listening",
    ]:
        story.append(Paragraph(f"\u2022  {item}", styles["bullet"]))

    story.append(Paragraph("Left Panel \u2014 Call Controls", styles["h2"]))
    for item in [
        "<b>Mode Toggle</b> \u2014 Switch between Business Hours and After Hours",
        "<b>Avatar Circle</b> \u2014 Animated audio visualizer with pulsing rings",
        "<b>Timer</b> \u2014 Live call duration (MM:SS)",
        "<b>Controls</b> \u2014 Start/End Call, Mute/Unmute, Reset",
    ]:
        story.append(Paragraph(f"\u2022  {item}", styles["bullet"]))

    story.append(Paragraph("Center Panel \u2014 Live Transcript", styles["h2"]))
    for item in [
        "<b>AI Messages</b> \u2014 Left-aligned, dark background",
        "<b>Your Messages</b> \u2014 Right-aligned, blue background",
        "<b>Typing Indicator</b> \u2014 Animated dots when AI is speaking",
    ]:
        story.append(Paragraph(f"\u2022  {item}", styles["bullet"]))

    story.append(Paragraph("Right Panel \u2014 Data &amp; Intelligence", styles["h2"]))
    for item in [
        "<b>Call Flow</b> \u2014 5-stage progress (Idle \u2192 Collecting \u2192 Evaluating \u2192 Routing \u2192 Done)",
        "<b>Status Badges</b> \u2014 Call type, disqualifier result, hot lead result",
        "<b>Extracted Data</b> \u2014 Real-time table of collected fields (shows X / 8)",
        "<b>System Logs</b> \u2014 Timestamped technical events with color coding",
    ]:
        story.append(Paragraph(f"\u2022  {item}", styles["bullet"]))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # DEMO 1: NEW CUSTOMER (AUTO)
    # ════════════════════════════════════════
    story.append(Paragraph("3. Demo 1 \u2014 New Customer Wanting Auto Insurance", styles["h1"]))
    story.append(demo_header("1", "New Customer \u2014 Auto Insurance", "Business Hours"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This is the full intake flow. It demonstrates data collection, validation, "
        "disqualifier check, hot lead check, and closing.",
        styles["body"]
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("After clicking the phone button, wait for the AI greeting:", styles["body"]))
    story.append(divider())

    story.append(ai_says("Hello, thank you for calling Equity Insurance. I am your AI receptionist..."))
    story.append(you_say("Hi, I'm looking for auto insurance."))
    story.append(divider())

    story.append(ai_says("I would be happy to help you with that. Can I get your full name..."))
    story.append(you_say("My name is John Smith. J-O-H-N, S-M-I-T-H."))
    story.append(watch('Watch: "caller_name: John Smith" appears in the Extracted Data panel. Call Flow moves to "Collecting."'))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for phone number.</b>", styles["body"]))
    story.append(you_say("808-555-1234"))
    story.append(Paragraph("<b>AI reads it back for confirmation.</b>", styles["body"]))
    story.append(you_say("Yes, that's correct."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for email.</b>", styles["body"]))
    story.append(you_say("john.smith@gmail.com"))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for mailing address.</b>", styles["body"]))
    story.append(you_say("123 Ala Moana Blvd, Honolulu, Hawaii 96813"))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for date of birth.</b>", styles["body"]))
    story.append(you_say("January 15, 1990"))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for occupation.</b>", styles["body"]))
    story.append(you_say("I'm a teacher at Punahou School."))
    story.append(divider())

    story.append(Paragraph("<b>AI confirms auto insurance, asks how you heard about them.</b>", styles["body"]))
    story.append(you_say("My friend Val told me about you."))
    story.append(watch('Watch: All 8 fields now show in Extracted Data. Counter shows "8 / 8".'))
    story.append(divider())

    story.append(Paragraph("<b>AI asks about your vehicle.</b>", styles["body"]))
    story.append(you_say("I drive a 2023 Honda Civic. I don't have the VIN on me. "
                         "It's financed through Honda Financial. Clean driving record, "
                         "no tickets or accidents. I'm the only driver."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks about claims history.</b>", styles["body"]))
    story.append(you_say("No claims at all."))
    story.append(watch('Watch: Call Flow moves to "Evaluating." Disqualifier badge shows "Evaluating..." then turns green "Qualified."'))
    story.append(divider())

    story.append(Paragraph("<b>AI asks when you need coverage.</b>", styles["body"]))
    story.append(you_say("I need it by next month."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks what you're currently paying.</b>", styles["body"]))
    story.append(you_say("I'm paying about $150 a month with GEICO."))
    story.append(watch('Watch: Hot Lead badge shows "Evaluating..." then turns green "Standard Lead."'))
    story.append(divider())

    story.append(Paragraph("<b>AI offers cross-sell (renters/homeowners).</b>", styles["body"]))
    story.append(you_say("Actually yeah, I could use renters insurance too."))
    story.append(divider())

    story.append(Paragraph("<b>AI reads back all your info for confirmation.</b>", styles["body"]))
    story.append(you_say("Yes, that's all correct."))
    story.append(watch('Watch: AI delivers closing. Call Flow reaches "Done."'))
    story.append(Spacer(1, 6))
    story.append(colored_box(
        "<b>Click the red phone button to end the call.</b>",
        ZINC_700
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # DEMO 2: EXISTING CUSTOMER
    # ════════════════════════════════════════
    story.append(Paragraph("4. Demo 2 \u2014 Existing Customer", styles["h1"]))
    story.append(demo_header("2", "Existing Customer", "Business Hours", PURPLE))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Demonstrates the existing customer routing path \u2014 AI takes a message and notifies Val.",
        styles["body"]
    ))
    story.append(divider())

    story.append(Paragraph("<b>AI says the greeting.</b>", styles["body"]))
    story.append(you_say("Hi, I'm an existing customer. I need to make a change to my policy."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for your name.</b>", styles["body"]))
    story.append(you_say("Sarah Lee."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for phone number.</b>", styles["body"]))
    story.append(you_say("808-555-6789"))
    story.append(divider())

    story.append(Paragraph("<b>AI asks what type of policy.</b>", styles["body"]))
    story.append(you_say("Auto insurance."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks what you need specifically.</b>", styles["body"]))
    story.append(you_say("I just bought a new car and I need to add it to my policy. It's a 2025 Tesla Model 3."))
    story.append(watch('Watch: Call Type badge shows purple "Existing Customer." Call Flow jumps to "Routing." '
                       'System log: "ROUTE: Existing customer \u2192 Ticket + Val notification."'))
    story.append(divider())

    story.append(Paragraph("<b>AI confirms a ticket was created and Val will follow up.</b>", styles["body"]))
    story.append(you_say("Great, thank you."))
    story.append(Spacer(1, 6))
    story.append(colored_box("<b>End the call.</b>", ZINC_700))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # DEMO 3: FILING A CLAIM
    # ════════════════════════════════════════
    story.append(Paragraph("5. Demo 3 \u2014 Filing a Claim", styles["h1"]))
    story.append(demo_header("3", "Filing a Claim", "Business Hours", DANGER))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Demonstrates the claims routing path \u2014 AI collects claim details and routes to claims agent.",
        styles["body"]
    ))
    story.append(divider())

    story.append(Paragraph("<b>AI says the greeting.</b>", styles["body"]))
    story.append(you_say("I need to file a claim. I was in an accident."))
    story.append(divider())

    story.append(ai_says("I'm sorry to hear that..."))
    story.append(Paragraph("<b>AI asks for your name.</b>", styles["body"]))
    story.append(you_say("David Kim."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for phone.</b>", styles["body"]))
    story.append(you_say("808-555-3333"))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for policy number.</b>", styles["body"]))
    story.append(you_say("I think it's EQ-2024-5500."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks what type of claim.</b>", styles["body"]))
    story.append(you_say("Auto."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks what happened.</b>", styles["body"]))
    story.append(you_say("Someone ran a red light and hit the side of my car on Kapiolani Boulevard. "
                         "There's major damage to the driver's side door and fender."))
    story.append(watch('Watch: Call Type badge turns red "Claim Filed." System log: '
                       '"ROUTE: Claim filed \u2192 Priority notification sent." Call Flow jumps to "Routing."'))
    story.append(divider())

    story.append(Paragraph("<b>AI says it filed the claim and is transferring you to an agent.</b>", styles["body"]))
    story.append(Spacer(1, 6))
    story.append(colored_box(
        "<b>End the call</b> (the transfer will attempt to connect to Val's number).",
        ZINC_700
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # DEMO 4: HOT LEAD
    # ════════════════════════════════════════
    story.append(Paragraph("6. Demo 4 \u2014 Hot Lead (High-Value Property)", styles["h1"]))
    story.append(demo_header("4", "Hot Lead \u2014 $3M Property", "Business Hours", ORANGE))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Triggers the hot lead detection \u2014 property value over $2M triggers immediate transfer to Davin.",
        styles["body"]
    ))
    story.append(divider())

    story.append(Paragraph("<b>AI says the greeting.</b>", styles["body"]))
    story.append(you_say("I'm looking for homeowners insurance."))
    story.append(divider())

    story.append(Paragraph(
        "<b>Follow the standard data collection</b> (name, phone, email, address, DOB, occupation, referral). "
        "When the AI asks about the property:",
        styles["body"]
    ))
    story.append(divider())

    story.append(ai_says("What is the estimated value of the property?"))
    story.append(you_say("It's a house in Kahala. Worth about 3 million dollars."))
    story.append(watch('Watch: Hot Lead badge turns orange "HOT LEAD \u2014 Transfer." System log shows high-value '
                       'detection. Call Flow moves to "Routing." Email sent to Davin + Val.'))
    story.append(divider())

    story.append(ai_says("With a property of this value, I would like to connect you directly "
                         "with one of our experienced agents..."))
    story.append(Spacer(1, 6))
    story.append(colored_box("<b>End the call.</b>", ZINC_700))

    story.append(Spacer(1, 16))

    # ════════════════════════════════════════
    # DEMO 5: DISQUALIFIED
    # ════════════════════════════════════════
    story.append(Paragraph("7. Demo 5 \u2014 Disqualified Caller", styles["h1"]))
    story.append(demo_header("5", "Disqualified Caller \u2014 Too Many Claims", "Business Hours", DANGER))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Triggers the disqualifier rule \u2014 3+ claims in a single year results in a polite redirect.",
        styles["body"]
    ))
    story.append(divider())

    story.append(Paragraph(
        "<b>Go through standard data collection.</b> When claims history comes up:",
        styles["body"]
    ))
    story.append(divider())

    story.append(ai_says("Have you had any claims in the past 5 years?"))
    story.append(you_say("Yes, I've had quite a few. A water damage claim in 2022, "
                         "a fire claim in 2023, a mold claim also in 2023, "
                         "and another water damage claim this year."))
    story.append(watch('Watch: Disqualifier badge turns red "Disqualified." System log shows disqualifier triggered.'))
    story.append(divider())

    story.append(ai_says("I appreciate your time. Based on the information you have shared, "
                         "we may not be the best fit for your needs right now..."))
    story.append(Spacer(1, 6))
    story.append(colored_box("<b>End the call.</b>", ZINC_700))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # DEMO 6: AFTER HOURS
    # ════════════════════════════════════════
    story.append(Paragraph("8. Demo 6 \u2014 After Hours Call", styles["h1"]))
    story.append(demo_header("6", "After Hours Call", "After Hours", ZINC_600))
    story.append(Spacer(1, 6))
    story.append(colored_box(
        "<b>Important:</b> Switch to <b>After Hours</b> mode BEFORE starting the call.",
        ACCENT
    ))
    story.append(Spacer(1, 6))

    story.append(ai_says("You have reached Equity Insurance outside of our regular office hours..."))
    story.append(you_say("Hi, I'd like to leave a message about getting an insurance quote."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for name.</b>", styles["body"]))
    story.append(you_say("Mike Johnson."))
    story.append(divider())

    story.append(Paragraph("<b>AI asks for phone.</b>", styles["body"]))
    story.append(you_say("808-555-4444"))
    story.append(divider())

    story.append(Paragraph("<b>AI asks the reason for calling.</b>", styles["body"]))
    story.append(you_say("I need auto insurance for a new car I'm picking up next week."))
    story.append(divider())

    story.append(ai_says("Thank you for calling. A member of our team will follow up on the next business day."))
    story.append(Spacer(1, 6))
    story.append(colored_box("<b>End the call.</b>", ZINC_700))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 9. WHAT TO WATCH FOR
    # ════════════════════════════════════════
    story.append(Paragraph("9. What to Watch For During Demos", styles["h1"]))
    story.append(Spacer(1, 6))

    watch_data = [
        [Paragraph("<b>Panel</b>", styles["body_bold"]),
         Paragraph("<b>What You'll See</b>", styles["body_bold"])],
        ["Call Flow\n(top-right)", "Progress bar: Idle \u2192 Collecting \u2192 Evaluating \u2192 Routing \u2192 Done"],
        ["Status Badges\n(below flow)", "Color badges: Qualified/Disqualified, Standard/Hot Lead, Call Type"],
        ["Extracted Data\n(middle-right)", "Each field appears in real-time as the AI saves it"],
        ["Live Transcript\n(center)", "Blue bubbles = You speaking, Dark bubbles = AI speaking"],
        ["System Logs\n(bottom-right)", "Blue=SAVE, Amber=RULE CHECK, Purple=ROUTE, Green=PASS, Red=FAIL"],
        ["Timer\n(center-left)", "Live call duration counter (MM:SS)"],
        ["Connection Status\n(top-right header)", "Disconnected \u2192 Connecting \u2192 Connected \u2192 Speaking"],
    ]
    w_table = Table(watch_data, colWidths=[1.5 * inch, 4.5 * inch])
    w_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, CARD_BG]),
    ]))
    story.append(w_table)
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 10. BUSINESS RULES
    # ════════════════════════════════════════
    story.append(Paragraph("10. Business Rules Reference", styles["h1"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Data Collection Fields (in order)", styles["h2"]))
    fields_data = [
        [Paragraph("<b>#</b>", styles["body_bold"]),
         Paragraph("<b>Field</b>", styles["body_bold"]),
         Paragraph("<b>AI Behavior</b>", styles["body_bold"])],
        ["1", "Full Name", "Asks caller to spell it out"],
        ["2", "Phone Number", "Repeats back and asks for confirmation"],
        ["3", "Email Address", "For sending the quote"],
        ["4", "Mailing Address", "Double-checks spelling"],
        ["5", "Date of Birth", "Standard verification"],
        ["6", "Occupation", "Qualifies for P&C credits"],
        ["7", "Insurance Type", "Auto, Property, Renters, Business, etc."],
        ["8", "Referral Source", "How they heard about Equity Insurance"],
    ]
    f_table = Table(fields_data, colWidths=[0.4 * inch, 1.3 * inch, 4.3 * inch])
    f_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, CARD_BG]),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ]))
    story.append(f_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Disqualifier Rules", styles["h2"]))
    disq_data = [
        [Paragraph("<b>Rule</b>", styles["body_bold"]),
         Paragraph("<b>Threshold</b>", styles["body_bold"]),
         Paragraph("<b>Action</b>", styles["body_bold"])],
        ["Claims History", "3+ claims in a single year", "Polite redirect"],
        ["Urgency (Property)", "Coverage needed within 72 hours", "Polite redirect"],
    ]
    d_table = Table(disq_data, colWidths=[1.3 * inch, 2.2 * inch, 2.5 * inch])
    d_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DANGER),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, HexColor("#fef2f2")]),
    ]))
    story.append(d_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Hot Lead Detection", styles["h2"]))
    hot_data = [
        [Paragraph("<b>Policy Type</b>", styles["body_bold"]),
         Paragraph("<b>Value Threshold</b>", styles["body_bold"]),
         Paragraph("<b>Action</b>", styles["body_bold"])],
        ["Property", "$2,000,000+", "Immediate transfer to Davin"],
        ["Auto", "$180,000+", "Immediate transfer to Davin"],
    ]
    h_table = Table(hot_data, colWidths=[1.3 * inch, 2.2 * inch, 2.5 * inch])
    h_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, HexColor("#fff7ed")]),
    ]))
    story.append(h_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Safety Guardrails", styles["h2"]))
    story.append(colored_box(
        "<b>The AI will NEVER:</b><br/>"
        "\u2022  Give coverage advice or quote prices<br/>"
        "\u2022  Bind policies, sign documents, or underwrite<br/>"
        "\u2022  Guarantee coverage or make promises<br/>"
        "\u2022  Claim affiliation with Equity Insurance in Tulsa, Oklahoma<br/><br/>"
        "All AI-collected data is flagged with <b>VAPI_AI_COLLECTED</b> for audit trail.",
        HexColor("#7f1d1d"),
    ))

    story.append(PageBreak())

    # ════════════════════════════════════════
    # 11. TIPS & TROUBLESHOOTING
    # ════════════════════════════════════════
    story.append(Paragraph("11. Tips &amp; Troubleshooting", styles["h1"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Tips for Best Results", styles["h2"]))
    tips = [
        "<b>Speak clearly</b> \u2014 the AI uses speech-to-text, so enunciate names and numbers",
        "<b>Pause after speaking</b> \u2014 give the AI 1-2 seconds to process before speaking again",
        "<b>Spell names</b> when asked \u2014 this dramatically improves accuracy",
        "<b>Confirm phone numbers</b> when the AI reads them back \u2014 say \"Yes\" or \"Correct\"",
        "<b>Press #</b> on your phone keypad at any time to request a live agent transfer",
        "If the AI misunderstands, correct it naturally: <i>\"No, I said Smith, S-M-I-T-H\"</i>",
        "If the call doesn't connect, click the <b>refresh button</b> and try again",
    ]
    for tip in tips:
        story.append(Paragraph(f"\u2022  {tip}", styles["bullet"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Troubleshooting", styles["h2"]))

    trouble_data = [
        [Paragraph("<b>Issue</b>", styles["body_bold"]),
         Paragraph("<b>Solution</b>", styles["body_bold"])],
        ["AI can't hear me", "Check microphone permission. Click Reset and retry. Check OS mic settings."],
        ["No audio from AI", "Check speakers/headphones. Try Chrome (recommended browser)."],
        ['"Connection Failed"', "Check internet. Wait 30 seconds and retry."],
        ["Call ends immediately", "Refresh page and retry. Browser may have blocked audio context."],
        ["Transcript not updating", "End call and start a new one."],
        ["Mode toggle not working", "Mode can only be changed when no call is active."],
        ["Audio echo / feedback", "Use headphones. Echo cancellation is built in but headphones are best."],
    ]
    tr_table = Table(trouble_data, colWidths=[1.6 * inch, 4.4 * inch])
    tr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ZINC_700),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, CARD_BG]),
    ]))
    story.append(tr_table)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#e4e4e7"), spaceAfter=12))

    story.append(Paragraph("Support Contacts", styles["h2"]))
    c_data = [
        [Paragraph("<b>Name</b>", styles["body_bold"]),
         Paragraph("<b>Email</b>", styles["body_bold"]),
         Paragraph("<b>Notes</b>", styles["body_bold"])],
        ["Davin Char (CEO)", "davin@equityinsurance.services", "Life/Medicare + high-value leads"],
        ["Val Char (P&C Agent)", "val@equityinsurance.services", "+1 (808) 780-0473"],
    ]
    c_table = Table(c_data, colWidths=[1.8 * inch, 2.2 * inch, 2.0 * inch])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e4e4e7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, CARD_BG]),
    ]))
    story.append(c_table)

    # ── BUILD ──
    doc.build(story, onFirstPage=first_page, onLaterPages=header_footer)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    build()
