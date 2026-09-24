# 🛡️ Technical Specification: Advanced Anti-Bot Evasion & Scraping Logic

This document outlines the hierarchy of bot detection and the specific implementation strategies required to bypass modern protection layers (Cloudflare, Akamai, Datadome, etc.).

---

## 🛠️ Detection & Mitigation Matrix

| Layer | Detection Method | Mitigation Strategy |
| :--- | :--- | :--- |
| **Layer 1: Hard Gates** | Mandatory CAPTCHA | Solve via 3rd party API (2Captcha, Anti-Captcha). |
| **Layer 2: Fingerprint** | Browser Traits (WebGL, Canvas, UA) | Use `playwright-stealth` or `puppeteer-extra-plugin-stealth`. |
| **Layer 3: Behavioral** | Mouse/Scroll patterns | Implement `Ghost Cursor` for human-like interaction. |
| **Layer 4: Framework** | `Runtime.enable` leaks / CDP events | Use `Rebrowser`, `Camaufox`, or `XDriver` (patched Playwright). |
| **Layer 5: Network** | TLS/JA3 Fingerprinting | Implement `curl_cffi` (Python) or `curl-impersonate`. |

---

## 1. CAPTCHA Strategy
### A. Mandatory CAPTCHAs
* **Trigger:** Checkout pages, login screens, or high-risk IP flags.
* **Logic:** Do not attempt to bypass via headers. 
* **Implementation:** Route the CAPTCHA payload to a solving service and inject the token into the response field.

### B. Invisible CAPTCHAs (V3 / Turnstile)
* **Mechanism:** Runs in the background to score the "humanity" of the session.
* **Action:** If blocked despite a clean browser, proceed to **Section 2 & 3**.

---

## 2. Browser Fingerprinting & Behavior
To prevent detection during the "Invisible" phase, the automation must mask low-level browser traits.

* **Fingerprint Variables:** Analyze `User-Agent`, `WebGL`, `Canvas`, `Audio Context`, `Navigator values`, and `Screen Resolution`.
* **Tooling:** * Use `FPMON` to audit which parameters are being leaked.
    * Apply `playwright-stealth` to patch common leaks.
* **Behavioral Simulation:** Avoid instant clicks or linear mouse movements.
    * **Implementation:** Integrate `Ghost Cursor` (Node.js/Python) to generate stochastic (randomized) paths for mouse movement and scrolling.

---

## 3. Automation Framework Detection (The "Silent Kill")
Even with perfect fingerprints, the **CDP (Chrome DevTools Protocol)** can leak the presence of automation.

### The `Runtime.enable` Leak
* **Problem:** Frameworks like Playwright send `Runtime.enable` to execute JS. This triggers `consoleAPICalled` events that don't occur in standard browsing.
* **The "Rebrowser" Fix:** Conventional stealth plugins do not fix this. 
* **Preferred Implementation:** 1.  **Camaufox:** A Firefox-based build patched at the binary level.
    2.  **Rebrowser:** A modified Playwright version that removes automation-specific signals.
    3.  **XDriver:** A custom-patched Playwright implementation designed to fix 4 specific detection bugs including `Runtime.enable`.

---

## 4. Network Layer: TLS/JA3 Fingerprinting
Detection can happen before a single line of JavaScript runs.

* **Mechanism:** The server analyzes the `ClientHello` packet (Cipher suites, TLS extensions).
* **Identification:** If a `Real Browser` works but `Headless Playwright + Proxy` fails instantly, it is likely a JA3 mismatch.
* **Implementation:**
    * Use `curl_cffi` in Python.
    * **Logic:** It impersonates the TLS handshake of specific browser versions (e.g., Chrome 120), ensuring the network signature matches the `User-Agent`.

---

## 5. Scalable Execution Logic
To maximize efficiency while maintaining high success rates:

1.  **Hybrid Approach:** Use a patched browser (Camaufox/XDriver) to perform the initial login/session handshake and solve challenges.
2.  **Cookie Extraction:** Harvest the validated session cookies and headers.
3.  **Request Reuse:** Pass these cookies to a lightweight requester like `curl_cffi`.
4.  **IP Management:** * Rotate **Residential or Mobile Proxies** only.
    * Implement randomized delays and concurrency caps to prevent rate-limiting.
5.  **Session Monitoring:** Track cookie expiry. If a request fails with a 403 or a CAPTCHA challenge, revert to **Step 1** to refresh the session.

---