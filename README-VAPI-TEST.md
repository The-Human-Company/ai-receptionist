# Equity Insurance AI Receptionist - Web Test Dashboard

This is a professional, production-grade testing interface for the Equity Insurance AI Receptionist. It connects directly to VAPI.ai and your n8n backend workflows to simulate real-world calls.

## Features

-   **Real-time Call Simulation:** Connects to VAPI using the Web SDK.
-   **Dual Mode Testing:** Toggle between "Business Hours" and "After Hours" logic instantly.
-   **Live Data Extraction:** Watch as the AI extracts fields (Name, Policy Type, etc.) and see them populate the data table in real-time.
-   **Live Transcript:** View the conversation as it happens.
-   **System Logs:** Monitor function calls and system status events.
-   **Visual Feedback:** Audio visualizer and connection status indicators.

## How to Use

1.  **Open the File:**
    Simply open `vapi-web-test.html` in any modern web browser (Chrome, Edge, Safari). No server is required, but running it via a local server (like Live Server in VS Code) is recommended for microphone permissions.

2.  **Select Mode:**
    Use the toggle in the top-left of the main stage to switch between:
    -   **Business Hours:** Full reception logic, routing, and data collection.
    -   **After Hours:** Brief message taking logic.

3.  **Start Call:**
    Click the large white Phone button at the bottom center.
    -   *Note: You will need to allow microphone access.*

4.  **Interact:**
    Speak to the AI as a customer. Watch the **Transcript** and **Extracted Data** panels populate.

5.  **Controls:**
    -   **Mute:** Click the microphone icon to mute your audio.
    -   **End Call:** Click the red phone button to hang up.
    -   **Reset:** Click the refresh icon to clear all data and start fresh.

## Technical Details

-   **Framework:** Vanilla JS + Tailwind CSS (via CDN).
-   **Icons:** Lucide Icons.
-   **Fonts:** Outfit (Display), Plus Jakarta Sans (Body), JetBrains Mono (Code).
-   **API:** VAPI Web SDK (`@vapi-ai/web`).
-   **Backend:** Connects to `https://solarexpresss.app.n8n.cloud/webhook`.

## Troubleshooting

-   **Microphone Error:** Ensure your browser has permission to access the microphone.
-   **Connection Failed:** Check your internet connection and verify the VAPI Public Key in the source code.
-   **No Audio:** Check your system volume and ensure the correct output device is selected in your OS settings.
