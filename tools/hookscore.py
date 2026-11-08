"""
tools/hookscore.py — 5-Property Hook Scoring Panel for Short-Form Video

Evaluates hook lines on:
1. Length & Brevity (Ideal: 8-15 words, <90 characters for mobile display)
2. Tension & Contrast (Presence of contradiction, conflict, or curiosity triggers)
3. Directness / Ban Words (Penalizes 'did you know', 'in this video', 'hey guys', etc.)
4. Concrete Noun & Action Velocity (Favors physical subjects and verbs over abstractions)
5. Readability & Cadence (Simplicity of words for natural speech delivery)
"""

import sys
import re
import argparse

BANNED_OPENERS = [
    r"^did you know",
    r"^have you ever",
    r"^hey guys",
    r"^welcome back",
    r"^in this video",
    r"^today we will",
    r"^let me tell you",
    r"^so basically"
]

CONTRAST_WORDS = [
    "never", "stop", "wrong", "secret", "hidden", "illegal", "costly",
    "mistake", "banned", "refuse", "impossible", "lie", "shocking",
    "accidentally", "warning", "catastrophe", "blunder", "vanished",
    "loophole", "truth", "actually", "destroy"
]

ABSTRACT_FLUFF = [
    "concept", "journey", "tapestry", "delve", "testament", "unleash",
    "game-changer", "mind-blowing", "insane", "miraculous", "fascinating"
]


def score_hook(hook_text: str) -> dict:
    hook_clean = hook_text.strip()
    words = hook_clean.split()
    word_count = len(words)
    char_count = len(hook_clean)

    feedback = []
    penalties = 0
    bonuses = 0

    # 1. Banned Openers Check (Major Penalty: -40 pts)
    for pattern in BANNED_OPENERS:
        if re.search(pattern, hook_clean, re.IGNORECASE):
            penalties += 40
            matched = pattern.replace("^", "")
            feedback.append(f"CRITICAL: Contains weak opener '{matched}'. Cut it and start with subject directly.")
            break

    # 2. Length / Brevity Check (Max 25 pts)
    length_score = 0
    if 6 <= word_count <= 14:
        length_score = 25
    elif 15 <= word_count <= 18:
        length_score = 18
        feedback.append("Brevity: Slightly long for a 3-second hook (aim for 8-14 words).")
    elif word_count < 6:
        length_score = 12
        feedback.append("Brevity: Too short to establish tension.")
    else:
        length_score = 5
        feedback.append(f"Brevity: Too wordy ({word_count} words). Viewer will scroll before finishing.")

    # 3. Tension / Contrast Words (Max 25 pts)
    tension_matches = [w for w in CONTRAST_WORDS if re.search(r'\b' + re.escape(w) + r'\b', hook_clean, re.IGNORECASE)]
    has_number = bool(re.search(r'\b\d+(\%|\$|k|m)?\b', hook_clean, re.IGNORECASE))
    
    tension_score = min(25, (len(tension_matches) * 10) + (10 if has_number else 0))
    if tension_matches:
        bonuses += 5
    else:
        feedback.append("Tension: Lacks strong tension or contrast words (e.g. wrong, secret, stop, never).")

    # 4. Fluff / Jargon Check (Max 25 pts)
    fluff_matches = [w for w in ABSTRACT_FLUFF if re.search(r'\b' + re.escape(w) + r'\b', hook_clean, re.IGNORECASE)]
    fluff_penalty = len(fluff_matches) * 10
    clarity_score = max(0, 25 - fluff_penalty)
    if fluff_matches:
        feedback.append(f"Clarity: Remove buzzwords: {', '.join(fluff_matches)}.")

    # 5. Speech Cadence & Concrete Velocity (Max 25 pts)
    # Check if starts with a concrete noun / subject or an imperative verb
    first_word = words[0].lower() if words else ""
    cadence_score = 20
    if first_word in ["the", "this", "how", "why", "stop", "never", "in", "every", "if"]:
        cadence_score = 25
    elif first_word in ["i", "we", "my", "our"]:
        cadence_score = 10
        feedback.append("Cadence: Self-referential opener ('I', 'We'). Frame around the viewer or the subject instead.")

    # Final Composite Score Calculation (0-100)
    raw_score = length_score + tension_score + clarity_score + cadence_score + bonuses - penalties
    final_score = max(5, min(100, raw_score))

    rating = "VIRAL TIER (A+)" if final_score >= 85 else \
             "STRONG (B+)" if final_score >= 70 else \
             "AVERAGE (C)" if final_score >= 55 else "WEAK (Needs Rewrite)"

    return {
        "hook": hook_clean,
        "score": final_score,
        "rating": rating,
        "metrics": {
            "word_count": word_count,
            "char_count": char_count,
            "brevity_score": length_score,
            "tension_score": tension_score,
            "clarity_score": clarity_score,
            "cadence_score": cadence_score,
            "tension_words_found": tension_matches,
            "has_number": has_number
        },
        "feedback": feedback if feedback else ["Punchy, direct, and establishes an instant curiosity gap."]
    }


def main():
    parser = argparse.ArgumentParser(description="Score a YouTube Shorts hook line.")
    parser.add_argument("--hook", type=str, required=True, help="The hook sentence to evaluate.")
    args = parser.parse_args()

    result = score_hook(args.hook)
    print("\n" + "=" * 55)
    print(f"HOOK: \"{result['hook']}\"")
    print(f"SCORE: {result['score']}/100 [{result['rating']}]")
    print(f"WORDS: {result['metrics']['word_count']} words | {result['metrics']['char_count']} chars")
    print("=" * 55)
    print("ANALYSIS & FEEDBACK:")
    for item in result["feedback"]:
        print(f" • {item}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
