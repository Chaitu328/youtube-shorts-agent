# ⚡ YouTube Shorts AI Agent (Powered by Google Gemini)

An open-source AI agent and toolkit designed to research, write, score, and package viral 60-second YouTube Shorts with maximum audience retention.

Powered natively by **Google Gemini** (`gemini-2.5-flash`), with **100% free-tier compatibility** via [Google AI Studio](https://aistudio.google.com/). No Claude Pro or expensive subscriptions needed.

---

## 🚀 Key Features

* **🪝 21-Formula Hook Engine:** Automatically crafts 5 distinct hook angles (The Contrarian, The Micro-Story, The Secret Mechanism, The Warning, etc.) from any topic.
* **📊 Algorithmic Hook Scorer:** A 5-factor heuristic panel (`tools/hookscore.py`) that evaluates brevity, tension words, speech cadence, and flags banned openers like *"Did you know"*.
* **🎬 Retention-Structured Scripts:** Generates complete 60s scripts broken down into retention milestones:
  * `00:00 - 00:03`: Scroll-stopping hook
  * `00:03 - 00:15`: Premise & tension build
  * `00:15 - 00:42`: Escalating revelation (3s cuts)
  * `00:42 - 00:53`: Climax & payoff
  * `00:53 - 00:58`: Seamless loop outro (replays cleanly back to line 1)
* **🔍 Title & Thumbnail Linter:** Checks for mobile viewport truncation (<50 chars), thumbnail clutter, and redundancy.
* **🏷️ Viral SEO & Tag Generator:** Generates high-intent search tags, hashtags, and description summaries.
* **🎙️ Customizable Voice Profile:** Calibrate tone, target audience, and taboo words in `config/voice.md`.

---

## 📦 Quick Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/Chaitu328/youtube-shorts-agent.git
cd youtube-shorts-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Your Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key** and generate a free API key.
3. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
4. Paste your key into `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Verify Connection
```bash
python agent.py test
```

---

## 🛠️ Usage & Commands

### 1. Generate & Score Viral Hooks
Generate 5 hook variations off proven psychological formulas, scored and ranked:
```bash
python agent.py hook --topic "The Lost Library of Alexandria"
```

### 2. Generate a Complete 60-Second Short Script
Includes timecodes, narration text, and 9:16 vertical visual prompts for every scene:
```bash
python agent.py script --topic "Why Did the Roman Empire Really Fall?"
```

### 3. Lint Title & Thumbnail Text
Test your title and thumbnail text against mobile truncation and glanceability rules:
```bash
python agent.py package --title "The 1 Mistake That Destroyed an Empire" --thumb "HE WAS WRONG"
```

### 4. Generate SEO, Hashtags & Tags
Get optimized titles, search queries, and tag lists for YouTube Studio:
```bash
python agent.py seo --topic "Bizarre Historical Coincidences"
```

---

## 🧰 Standalone Tools (Zero Dependencies)

The helper tools in `tools/` run with standard clean Python 3 without any external libraries or API calls:

```bash
# Score any hook sentence offline
python tools/hookscore.py --hook "99% of people charge their phone completely wrong."

# Lint title & thumbnail text
python tools/title_linter.py --title "How One Typo Cost $400 Million" --thumb "COSTLY MISTAKE"
```

---

## 📄 Customizing Your Channel Voice
Edit [`config/voice.md`](config/voice.md) to define:
* Your niche and target audience.
* Sentence length and pacing preferences.
* Taboo words (banned jargon).

---

## 📜 License
MIT License. Free to use, adapt, and build upon!

