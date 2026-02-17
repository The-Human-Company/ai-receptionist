# HOW TO USE THE AI RECEPTIONIST — DEMO GUIDE

## Getting Started

1. Open `vapi-web-test.html` in Chrome (double-click the file)
2. Allow microphone access when prompted
3. Wait for "VAPI SDK loaded successfully" in the System Logs panel (bottom-right)
4. Choose **Business Hours** or **After Hours** mode (top-left toggle)
5. Click the white **phone button** to start the call

---

## DEMO 1: New Customer Wanting Auto Insurance

**Mode:** Business Hours

After clicking the phone button, wait for the AI greeting. Then follow this script:

---

**AI says:** *"Hello, thank you for calling Equity Insurance. I am your AI receptionist..."*

**YOU say:**
> "Hi, I'm looking for auto insurance."

**AI says:** *"I would be happy to help you with that. Can I get your full name..."*

**YOU say:**
> "My name is John Smith. J-O-H-N, S-M-I-T-H."

*Watch: "caller_name: John Smith" appears in the Extracted Data panel. Call Flow moves to "Collecting."*

**AI asks for phone number.**

**YOU say:**
> "808-555-1234"

**AI reads it back for confirmation.**

**YOU say:**
> "Yes, that's correct."

**AI asks for email.**

**YOU say:**
> "john.smith@gmail.com"

**AI asks for mailing address.**

**YOU say:**
> "123 Ala Moana Blvd, Honolulu, Hawaii 96813"

**AI asks for date of birth.**

**YOU say:**
> "January 15, 1990"

**AI asks for occupation.**

**YOU say:**
> "I'm a teacher at Punahou School."

**AI confirms auto insurance, asks how you heard about them.**

**YOU say:**
> "My friend Val told me about you."

*Watch: All 8 fields now show in Extracted Data. Field counter shows "8 / 8".*

**AI asks about your vehicle.**

**YOU say:**
> "I drive a 2023 Honda Civic. I don't have the VIN on me. It's financed through Honda Financial. Clean driving record, no tickets or accidents. I'm the only driver."

**AI asks about claims history.**

**YOU say:**
> "No claims at all."

*Watch: Call Flow moves to "Evaluating." Disqualifier badge shows "Evaluating..." then turns green "Qualified."*

**AI asks when you need coverage.**

**YOU say:**
> "I need it by next month."

**AI asks what you're currently paying.**

**YOU say:**
> "I'm paying about $150 a month with GEICO."

*Watch: Hot Lead badge shows "Evaluating..." then turns green "Standard Lead."*

**AI offers cross-sell (renters/homeowners).**

**YOU say:**
> "Actually yeah, I could use renters insurance too."

**AI reads back all your info for confirmation.**

**YOU say:**
> "Yes, that's all correct."

**AI delivers closing.** Call Flow reaches "Done."

**Click the red phone button to end the call.**

---

## DEMO 2: Existing Customer

**Mode:** Business Hours

**AI says the greeting.**

**YOU say:**
> "Hi, I'm an existing customer. I need to make a change to my policy."

**AI asks for your name.**

**YOU say:**
> "Sarah Lee."

**AI asks for phone number.**

**YOU say:**
> "808-555-6789"

**AI asks what type of policy.**

**YOU say:**
> "Auto insurance."

**AI asks what you need specifically.**

**YOU say:**
> "I just bought a new car and I need to add it to my policy. It's a 2025 Tesla Model 3."

*Watch: Call Type badge shows purple "Existing Customer." Call Flow jumps to "Routing." System log shows "ROUTE: Existing customer → Ticket + Val notification."*

**AI confirms a ticket was created and Val will follow up.**

**YOU say:**
> "Great, thank you."

**End the call.**

---

## DEMO 3: Filing a Claim

**Mode:** Business Hours

**AI says the greeting.**

**YOU say:**
> "I need to file a claim. I was in an accident."

**AI says:** *"I'm sorry to hear that..."* and asks for your name.

**YOU say:**
> "David Kim."

**AI asks for phone.**

**YOU say:**
> "808-555-3333"

**AI asks for policy number.**

**YOU say:**
> "I think it's EQ-2024-5500."

**AI asks what type of claim.**

**YOU say:**
> "Auto."

**AI asks what happened.**

**YOU say:**
> "Someone ran a red light and hit the side of my car on Kapiolani Boulevard. There's major damage to the driver's side door and fender."

*Watch: Call Type badge turns red "Claim Filed." System log shows "ROUTE: Claim filed → Priority notification sent." Call Flow jumps to "Routing."*

**AI says it filed the claim and is transferring you to an agent.**

**End the call** (the transfer will attempt to connect to Val's number).

---

## DEMO 4: Hot Lead (High-Value Property)

**Mode:** Business Hours

**AI says the greeting.**

**YOU say:**
> "I'm looking for homeowners insurance."

Follow the data collection (name, phone, email, address, etc.) and when the AI asks about property:

**AI asks:** *"What is the property value?"*

**YOU say:**
> "It's a house in Kahala. Worth about 3 million dollars."

*Watch: Hot Lead badge turns orange "HOT LEAD — Transfer." System log shows the high-value detection. Call Flow moves to "Routing."*

**AI says:** *"With a property of this value, I would like to connect you directly with one of our experienced agents..."*

**End the call.**

---

## DEMO 5: Disqualified Caller

**Mode:** Business Hours

Go through data collection and when claims history comes up:

**AI asks:** *"Have you had any claims in the past 5 years?"*

**YOU say:**
> "Yes, I've had quite a few. A water damage claim in 2022, a fire claim in 2023, a mold claim also in 2023, and another water damage claim this year."

*Watch: Disqualifier badge turns red "Disqualified."*

**AI says:** *"I appreciate your time. Based on the information you have shared, we may not be the best fit for your needs right now..."*

**End the call.**

---

## DEMO 6: After Hours Call

**Mode:** Switch to **After Hours** before starting the call.

**AI says:** *"You have reached Equity Insurance outside of our regular office hours..."*

**YOU say:**
> "Hi, I'd like to leave a message about getting an insurance quote."

**AI asks for name.**

**YOU say:**
> "Mike Johnson."

**AI asks for phone.**

**YOU say:**
> "808-555-4444"

**AI asks the reason for calling.**

**YOU say:**
> "I need auto insurance for a new car I'm picking up next week."

**AI says:** *"Thank you for calling. A member of our team will follow up on the next business day."*

**End the call.**

---

## What to Watch For During Demos

| Panel | What You'll See |
|-------|----------------|
| **Call Flow** (top-right) | Progress bar: Idle → Collecting → Evaluating → Routing → Done |
| **Status Badges** (below flow) | Color badges: Qualified/Disqualified, Standard/Hot Lead, Call Type |
| **Extracted Data** (middle-right) | Each field appears in real-time as the AI saves it |
| **Live Transcript** (center) | Blue bubbles = AI speaking, White bubbles = You speaking |
| **System Logs** (bottom-right) | Color-coded: Blue=SAVE, Amber=RULE CHECK, Purple=ROUTE, Green=PASS, Red=FAIL |
| **Timer** (center-left) | Live call duration counter |
| **Connection Status** (top-right header) | Disconnected → Connecting → Connected → Speaking |

## Tips

- **Speak clearly** — the AI uses speech-to-text so enunciate names and numbers
- **Pause after speaking** — give the AI 1-2 seconds to process before speaking again
- **Spell names** when asked — this helps accuracy
- **Repeat phone numbers** when the AI reads them back — say "Yes" or "Correct"
- **Press #** on your phone keypad at any time to request a live agent transfer
- If the AI misunderstands something, just correct it naturally: *"No, I said Smith, S-M-I-T-H"*
- If the call doesn't connect, click the **refresh button** (circular arrow) and try again
