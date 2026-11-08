"""
tools/retention_pacing.py — Shorts Retention Pacing & Beat Calculator

Audits YouTube Shorts scripts for speech rate and retention beat positioning:
- Ideal speech rate: 130 - 155 words per minute (~2.2 to 2.5 words/sec)
- 30s Short: 65 - 75 words
- 60s Short: 130 - 150 words
- Retention beats:
  * 00s - 03s: Hook (Scroll stopper, immediate tension)
  * 03s - 15s: Re-hook & Premise (Why viewer should care)
  * 15s - 45s: Escalating Evidence / The Turn (Fast cuts every 3s)
  * 45s - 55s: Payoff / Resolution
  * 55s - 60s: Seamless Loop back to line 1
"""

import sys
import argparse


def calculate_pacing(text: str, target_seconds: int = 60) -> dict:
    words = text.split()
    total_words = len(words)

    # Average narration speed for vertical shorts: ~2.4 words per second
    estimated_seconds = round(total_words / 2.4, 1)

    min_words = int(target_seconds * 2.1)
    max_words = int(target_seconds * 2.6)

    warnings = []
    if total_words < min_words:
        warnings.append(f"Script may run too fast (~{estimated_seconds}s). Target is {target_seconds}s ({min_words}-{max_words} words).")
    elif total_words > max_words:
        warnings.append(f"Script is too long (~{estimated_seconds}s). Narration will be rushed. Cut {total_words - max_words} words.")

    return {
        "total_words": total_words,
        "estimated_duration_sec": estimated_seconds,
        "target_duration_sec": target_seconds,
        "recommended_word_range": f"{min_words} - {max_words} words",
        "pacing_status": "OPTIMAL" if not warnings else "ADJUST_LENGTH",
        "warnings": warnings,
        "retention_milestones": [
            {"time": "0:00 - 0:03", "beat": "Scroll-Stopping Hook", "target_words": "8 - 14 words"},
            {"time": "0:03 - 0:15", "beat": "Context & Curiosity Gap", "target_words": "25 - 30 words"},
            {"time": "0:15 - 0:45", "beat": "The Escalating Story / Revelation", "target_words": "65 - 75 words"},
            {"time": "0:45 - 0:55", "beat": "The Payoff / Final Twist", "target_words": "20 - 25 words"},
            {"time": "0:55 - 1:00", "beat": "Loop Outro (Seamless rewatch)", "target_words": "10 - 15 words"}
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate YouTube Shorts script pacing.")
    parser.add_argument("--file", type=str, help="Path to text script file")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            script_text = f.read()
        res = calculate_pacing(script_text)
        print(f"Total Words: {res['total_words']} | Est Duration: {res['estimated_duration_sec']}s")


if __name__ == "__main__":
    main()
