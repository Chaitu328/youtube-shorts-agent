# Contributing to YouTube Shorts AI Agent

Thank you for your interest in contributing to **YouTube Shorts AI Agent**! We welcome all contributions from bug fixes and documentation enhancements to new hook formulas and multimodal integrations.

---

## 🛠️ Development Setup

1. **Fork & Clone**:
   ```bash
   git clone https://github.com/Chaitu328/youtube-shorts-agent.git
   cd youtube-shorts-agent
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   copy .env.example .env
   ```
   Add your Gemini API key from [Google AI Studio](https://aistudio.google.com/).

4. **Verify Offline Tools**:
   ```bash
   python tools/hookscore.py --hook "99% of people charge their phone completely wrong."
   python tools/title_linter.py --title "The Secret Hack to 10x Battery Life" --thumb "DON'T CHARGE"
   ```

---

## 💡 How to Contribute

- **Add New Hook Formulas**: Expand the psychological hook formulas in `agent.py`.
- **Improve Scoring Heuristics**: Enhance cadence, sentiment, or curiosity gap detection in `tools/hookscore.py`.
- **Packaging Rules**: Add checks for thumbnail contrast or title readability in `tools/title_linter.py`.
- **Integrations**: PRs integrating TTS engines (ElevenLabs, Edge-TTS) or vertical video renderers (FFmpeg, MoviePy) are warmly encouraged!

---

## 📋 Pull Request Guidelines

1. Create a feature branch: `git checkout -b feat/your-feature-name`
2. Commit your changes with clear, descriptive messages: `git commit -m "feat: add edge-tts voiceover engine"`
3. Push to your branch and open a Pull Request against `main`.
4. Ensure all standalone tools in `tools/` run without errors and maintain zero external dependencies.

---

## 📜 Code of Conduct

Be kind, constructive, and respectful to all collaborators.

