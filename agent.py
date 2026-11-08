"""
agent.py — YouTube Shorts AI Agent (Powered by Google Gemini)

Generates viral YouTube Shorts scripts, scores hooks against 21 proven formulas,
lints titles and thumbnail text, and builds complete video packaging.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Import local tools
from tools.hookscore import score_hook
from tools.title_linter import lint_package
from tools.retention_pacing import calculate_pacing

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
HOOKS_FILE = CONFIG_DIR / "hooks.json"
VOICE_FILE = CONFIG_DIR / "voice.md"


def get_gemini_client():
    """Initializes Google GenAI Client with API key."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n[ERROR] No Gemini API key found!")
        print("Please set GEMINI_API_KEY in your .env file.")
        print("You can get a free API key at: https://aistudio.google.com/\n")
        sys.exit(1)
    
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except ImportError:
        print("\n[ERROR] 'google-genai' library not installed.")
        print("Run: pip install google-genai python-dotenv\n")
        sys.exit(1)


def load_voice_guidelines() -> str:
    if VOICE_FILE.exists():
        try:
            return VOICE_FILE.read_text(encoding="utf-8")
        except Exception:
            pass
    return "Tone: punchy, fast, curious, no filler words."


def load_hook_formulas() -> list:
    if HOOKS_FILE.exists():
        try:
            data = json.loads(HOOKS_FILE.read_text(encoding="utf-8"))
            return data.get("formulas", [])
        except Exception:
            pass
    return []


def generate_with_gemini(client, prompt: str, model: str = None) -> str:
    """Invokes Gemini model with clean error handling."""
    model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        raw = response.text.strip()
        # Clean markdown wrappers if present
        raw = re.sub(r'^```json\s*', '', raw, flags=re.MULTILINE)
        raw = re.sub(r'^```\s*', '', raw, flags=re.MULTILINE)
        raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)
        return raw.strip()
    except Exception as e:
        print(f"[Gemini Error]: {e}")
        raise


def run_hook_generator(topic: str, client=None):
    """Generates 5 hooks across distinct formulas and scores each."""
    client = client or get_gemini_client()
    formulas = load_hook_formulas()
    formulas_sample = formulas[:8] if formulas else []
    formulas_hint = "\n".join([f"- {f['name']}: {f['template']}" for f in formulas_sample])

    prompt = f"""You are an elite YouTube Shorts retention strategist.
Topic: "{topic}"

Generate 5 different viral hook candidates for a 60-second YouTube Short.
Each hook must be 8 to 14 words max.
Start directly with the subject, action, or surprising contrast.
NEVER start with "Did you know", "Hey guys", or "In this video".

Available formula references:
{formulas_hint}

Respond ONLY in valid JSON format:
{{
  "hooks": [
    {{"formula": "The Contrarian", "hook": "..."}},
    {{"formula": "The Secret Mechanism", "hook": "..."}},
    {{"formula": "The Timeline Twist", "hook": "..."}},
    {{"formula": "The Warning", "hook": "..."}},
    {{"formula": "The Impossible Juxtaposition", "hook": "..."}}
  ]
}}"""

    print(f"\n[AGENT] Generating and scoring hooks for topic: '{topic}'...")
    raw_json = generate_with_gemini(client, prompt)
    
    try:
        data = json.loads(raw_json)
        candidates = data.get("hooks", [])
    except Exception:
        print("[Warning] Could not parse JSON response; displaying raw text:")
        print(raw_json)
        return

    scored_hooks = []
    for item in candidates:
        text = item.get("hook", "")
        formula = item.get("formula", "General")
        score_data = score_hook(text)
        scored_hooks.append({
            "formula": formula,
            "hook": text,
            "score": score_data["score"],
            "rating": score_data["rating"],
            "feedback": score_data["feedback"]
        })

    # Sort descending by score
    scored_hooks.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 65)
    print(f"🎯 RANKED VIRAL HOOKS FOR: {topic.upper()}")
    print("=" * 65)
    for idx, h in enumerate(scored_hooks, 1):
        star = "⭐ [TOP PICK]" if idx == 1 else ""
        print(f"\n#{idx} {star} Score: {h['score']}/100 [{h['rating']}] | Formula: {h['formula']}")
        print(f"   \"{h['hook']}\"")
        for fb in h["feedback"]:
            print(f"    - {fb}")
    print("\n" + "=" * 65 + "\n")
    return scored_hooks


def run_script_generator(topic: str, formula_choice: str = None, client=None):
    """Generates a complete 60-second retention-engineered script."""
    client = client or get_gemini_client()
    voice = load_voice_guidelines()

    prompt = f"""You are the Lead Creative Director and Scriptwriter for viral YouTube Shorts.

Channel Tone & Guidelines:
{voice}

Topic: "{topic}"
Target Duration: 55-60 seconds (~135-145 words total spoken).

Structure the script into 5 strict retention phases:
1. HOOK (00s-03s, 8-14 words): Scroll-stopping line with instant curiosity.
2. PREMISE (03s-15s, 25-30 words): Establishes why the viewer must stay until the end.
3. THE BUILD / ESCALATION (15s-42s, 65-75 words): Fast-paced revelation, 3-4 sentence beats.
4. THE CLIMAX / PAYOFF (42s-53s, 20-25 words): The core punchline or conclusion.
5. SEAMLESS LOOP OUTRO (53s-58s, 10-15 words): A line that connects back into line 1 so the video loops endlessly.

For each scene, output:
- "narration": Words spoken out loud.
- "visual_cue": What appears on screen (photorealistic 9:16 vertical prompt, cinematic lighting, no text).
- "duration_sec": Duration estimate for that scene.

Respond ONLY with valid JSON:
{{
  "title": "...",
  "thumbnail_text": "...",
  "target_duration": 60,
  "scenes": [
    {{
      "phase": "HOOK",
      "timestamp": "00:00 - 00:03",
      "narration": "...",
      "visual_cue": "...",
      "duration_sec": 3
    }},
    ...
  ]
}}"""

    print(f"\n[AGENT] Generating 60-second viral Short script for: '{topic}'...")
    raw_json = generate_with_gemini(client, prompt)

    try:
        data = json.loads(raw_json)
    except Exception:
        print("[Warning] Raw Gemini response:\n", raw_json)
        return

    full_narration = " ".join([s.get("narration", "") for s in data.get("scenes", [])])
    pacing = calculate_pacing(full_narration, target_seconds=60)
    hook_text = data.get("scenes", [{}])[0].get("narration", "")
    hook_eval = score_hook(hook_text) if hook_text else {"score": 0, "rating": "N/A"}

    print("\n" + "=" * 70)
    print(f"🎬 SHORT TITLE: {data.get('title')}")
    print(f"🖼️ THUMBNAIL TEXT: {data.get('thumbnail_text')}")
    print(f"⏱️ PACING: {pacing['total_words']} words (~{pacing['estimated_duration_sec']}s) | {pacing['pacing_status']}")
    print(f"🪝 HOOK RETENTION SCORE: {hook_eval.get('score', 'N/A')}/100 [{hook_eval.get('rating', '')}]")
    print("=" * 70)

    for s in data.get("scenes", []):
        print(f"\n[{s.get('phase')}] ({s.get('timestamp')}) ~{s.get('duration_sec')}s")
        print(f"🗣️ SPOKEN: \"{s.get('narration')}\"")
        print(f"🎥 VISUAL: {s.get('visual_cue')}")

    print("\n" + "=" * 70)
    print("💡 Loop Test: Read the final line directly into the first line to test seamless replay.")
    print("=" * 70 + "\n")
    return data


def run_seo_generator(topic: str, client=None):
    """Generates metadata, description, and high-volume tags."""
    client = client or get_gemini_client()

    prompt = f"""You are a YouTube Search and Algorithm specialist.
Generate viral packaging for a YouTube Short about: "{topic}"

Output ONLY in valid JSON format:
{{
  "titles": [
    "High-CTR Title Option 1 (<50 chars)",
    "High-CTR Title Option 2 (<50 chars)",
    "High-CTR Title Option 3 (<50 chars)"
  ],
  "thumbnail_texts": [
    "3-4 word phrase 1",
    "3-4 word phrase 2"
  ],
  "description": "2-3 punchy lines summarizing the video followed by 3 hashtags.",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8"],
  "search_queries": [
    "Query 1 users search for",
    "Query 2 users search for",
    "Query 3 users search for"
  ]
}}"""

    print(f"\n[AGENT] Generating YouTube SEO package for: '{topic}'...")
    raw_json = generate_with_gemini(client, prompt)

    try:
        data = json.loads(raw_json)
        print("\n" + "=" * 60)
        print("📌 RECOMMENDED TITLES (Mobile Optimized):")
        for t in data.get("titles", []):
            lint = lint_package(t)
            print(f"  • {t} ({len(t)} chars) [{lint['status']}]")
        
        print("\n🖼️ THUMBNAIL TEXT PAIRINGS:")
        for th in data.get("thumbnail_texts", []):
            print(f"  • \"{th}\"")

        print("\n📝 DESCRIPTION:")
        print(data.get("description", ""))

        print("\n🏷️ TAGS:")
        print(", ".join(data.get("tags", [])))

        print("\n🔍 TARGET SEARCH QUERIES:")
        for q in data.get("search_queries", []):
            print(f"  • {q}")
        print("=" * 60 + "\n")
    except Exception:
        print(raw_json)


def main():
    parser = argparse.ArgumentParser(description="YouTube Shorts Agent — Powered by Google Gemini")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Hook command
    p_hook = subparsers.add_parser("hook", help="Generate and score viral hooks")
    p_hook.add_argument("--topic", type=str, required=True, help="Topic of the Short")

    # Script command
    p_script = subparsers.add_parser("script", help="Generate full 60-second Short script")
    p_script.add_argument("--topic", type=str, required=True, help="Topic of the Short")

    # Package / Title Linter
    p_pkg = subparsers.add_parser("package", help="Lint title and thumbnail text")
    p_pkg.add_argument("--title", type=str, required=True, help="Video title")
    p_pkg.add_argument("--thumb", type=str, default="", help="Thumbnail text overlay")

    # SEO command
    p_seo = subparsers.add_parser("seo", help="Generate SEO title, description & tags")
    p_seo.add_argument("--topic", type=str, required=True, help="Topic of the Short")

    # Test command
    subparsers.add_parser("test", help="Test connection to Gemini and local tools")

    args = parser.parse_args()

    if args.command == "hook":
        run_hook_generator(args.topic)
    elif args.command == "script":
        run_script_generator(args.topic)
    elif args.command == "package":
        lint_package(args.title, args.thumb)
        # Also print formatted
        from tools.title_linter import main as lint_main
        sys.argv = ["title_linter.py", "--title", args.title, "--thumb", args.thumb]
        lint_main()
    elif args.command == "seo":
        run_seo_generator(args.topic)
    elif args.command == "test":
        print("\n[INFO] Testing Gemini API Connection...")
        client = get_gemini_client()
        res = generate_with_gemini(client, "Respond with: 'Gemini is connected and ready!'")
        print(f"[SUCCESS] {res}\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

