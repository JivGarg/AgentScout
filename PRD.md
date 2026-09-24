
---

# PRD: AgentScout – The Deep-Research Outreach Agent

**Project Vision:** To eliminate the "manual research" phase of B2B sales by using AI to instantly understand a company's mission, news, and pain points from their URL.

---

## 1. Target Audience & User Stories

* **The Freelancer:** Needs to send 20 personalized cold emails a day without spending 4 hours on research.
* **The Agency Owner:** Wants a standardized way for their sales team to generate high-quality outreach.
* **User Story:** *"As a user, I want to input a URL and receive a structured JSON report and a draft email so that I can copy-paste it into my outreach tool immediately."*

---

## 2. Functional Requirements

### Phase 1: The Core Engine (MVP)

* **URL Processing:** A robust input field that validates URLs.
* **The "Scraper" Service:** A FastAPI endpoint that uses `Firecrawl` or `Crawl4AI` to bypass bot-blockers and extract clean Markdown text.
* **AI Researcher:** A LangChain/CrewAI sequence that:
1. Summarizes the company's core product.
2. Identifies "Pain Points" based on their copy.
3. Drafts a 3-paragraph outreach email.


* **Persistence:** Store every search in **PostgreSQL** so users can view their history.

### Phase 2: Enhanced Features

* **Export Options:** "Copy to Clipboard" and "Download as PDF/Markdown."
* **Search History:** A dashboard showing previous research results.
* **User Auth:** Simple login/signup (using FastAPI Users or Clerk) to track individual credits.

---

## 3. Technical Stack & Architecture

| Component | Technology | Why? |
| --- | --- | --- |
| **Frontend** | React.js + Tailwind | Fast, component-based, industry standard. |
| **UI Components** | [Uiverse.io](https://uiverse.io) | High-end, "copy-paste" CSS/Tailwind elements for a premium feel. |
| **Backend** | FastAPI (Python) | High performance, native `async` support for AI calls. |
| **Database** | PostgreSQL | Relational data is perfect for storing user history and structured AI outputs. |
| **AI Orchestration** | LangChain / PydanticAI | Forces the AI to return data in a strict format. |

---

## 4. Database Schema (PostgreSQL)

* **Users Table:** `id`, `email`, `hashed_password`, `created_at`.
* **SearchLogs Table:** * `id` (Primary Key)
* `user_id` (Foreign Key)
* `target_url` (String)
* `raw_content` (Text - for auditing)
* `summary` (Text)
* `generated_pitch` (Text)
* `timestamp` (DateTime)



---

## 5. UI/UX Plan (using Uiverse.io)

To make the app look like it costs ₹5,00,000 to build:

1. **The Input:** Use a "Cyberpunk" or "Glassmorphism" search bar from Uiverse for the URL entry.
2. **The Loading State:** A "Scanning..." animation while the scraper and LLM are working.
3. **The Results:** Display the research in "Cards" with sleek hover effects.

---

## 6. Success Metrics (The "Earn" Strategy)

* **Technical Success:** Research is generated in under 20 seconds with >90% accuracy.
* **Financial Success:** Land **one** local digital marketing agency as a "Beta Client" for ₹20,000/month to use this tool for their sales team.

---
