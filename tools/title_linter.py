"""
tools/title_linter.py — Title & Thumbnail Packaging Linter

Validates the YouTube title + thumbnail pairing:
1. Mobile Truncation: Flags titles over 50 characters (cut off on smartphones).
2. Thumbnail Complementarity: Ensures thumbnail text doesn't duplicate the title word-for-word.
3. Thumbnail Word Count: Maximum 3-5 bold words for glanceability.
4. CTR Triggers: Looks for brackets, numbers, tension gaps, and clarity.
"""

import sys
import re
import argparse

VAGUE_TERMS = [
    "interesting", "amazing", "cool", "epic", "things", "stuff",
    "video", "watch this", "unbelievable"
]


def lint_package(title: str, thumbnail_text: str = "") -> dict:
    title_clean = title.strip()
    thumb_clean = thumbnail_text.strip()

    title_chars = len(title_clean)
    title_words = title_clean.split()
    thumb_words = thumb_clean.split() if thumb_clean else []

    issues = []
    strengths = []
    score = 100

    # 1. Title Truncation Check
    if title_chars > 60:
        score -= 25
        issues.append(f"Title is {title_chars} characters. It will be truncated with '...' on mobile screens (keep < 50 chars).")
    elif title_chars > 50:
        score -= 10
        issues.append(f"Title is {title_chars} characters. Borderline on mobile; optimal is 35-48 chars.")
    elif title_chars < 15:
        score -= 15
        issues.append("Title is too brief to provide clear context or curiosity.")
    else:
        strengths.append(f"Optimal title length ({title_chars} chars, fits perfectly without truncation).")

    # 2. Duplicate Words between Title & Thumbnail
    if thumb_clean:
        title_set = set(re.findall(r'\b[a-zA-Z]{3,}\b', title_clean.lower()))
        thumb_set = set(re.findall(r'\b[a-zA-Z]{3,}\b', thumb_clean.lower()))
        overlap = title_set.intersection(thumb_set)
        
        if len(overlap) >= 3:
            score -= 20
            issues.append(f"Duplication alert: Title and thumbnail share words {list(overlap)}. Use thumbnail to ask a question or show a reaction; use title to complete the thought.")
        else:
            strengths.append("Title and thumbnail text complement each other rather than repeating.")

        # 3. Thumbnail Word Count
        if len(thumb_words) > 5:
            score -= 15
            issues.append(f"Thumbnail text has {len(thumb_words)} words. Mobile viewers only glance for 0.4s — limit to 2-4 punchy words.")
        elif len(thumb_words) > 0:
            strengths.append(f"Clean thumbnail text brevity ({len(thumb_words)} words).")

    # 4. Vague Buzzwords Check
    found_vague = [w for w in VAGUE_TERMS if re.search(r'\b' + re.escape(w) + r'\b', title_clean, re.IGNORECASE)]
    if found_vague:
        score -= 15
        issues.append(f"Replace vague terms with concrete details: {found_vague}.")

    # 5. Positive CTR Signals
    has_number = bool(re.search(r'\b\d+(\%|\$|k|m)?\b', title_clean))
    has_brackets = bool(re.search(r'[\(\[\{].*?[\)\]\}]', title_clean))

    if has_number:
        strengths.append("Contains specific numbers (boosts trust & click credibility).")
    if has_brackets:
        strengths.append("Uses bracketed context (e.g. [True Story], (Shocking Origin)).")

    score = max(10, min(100, score))
    status = "READY TO PUBLISH" if score >= 80 else "NEEDS REFINEMENT" if score >= 60 else "REVISE"

    return {
        "title": title_clean,
        "thumbnail_text": thumb_clean,
        "score": score,
        "status": status,
        "strengths": strengths,
        "issues": issues
    }


def main():
    parser = argparse.ArgumentParser(description="Lint a YouTube title and thumbnail pairing.")
    parser.add_argument("--title", type=str, required=True, help="Proposed YouTube video title")
    parser.add_argument("--thumb", type=str, default="", help="Text written on the thumbnail image")
    args = parser.parse_args()

    result = lint_package(args.title, args.thumb)
    print("\n" + "=" * 55)
    print(f"TITLE: \"{result['title']}\"")
    if result["thumbnail_text"]:
        print(f"THUMB TEXT: \"{result['thumbnail_text']}\"")
    print(f"PACKAGE SCORE: {result['score']}/100 [{result['status']}]")
    print("=" * 55)
    if result["strengths"]:
        print("STRENGTHS:")
        for s in result["strengths"]:
            print(f"  + {s}")
    if result["issues"]:
        print("IMPROVEMENTS NEEDED:")
        for i in result["issues"]:
            print(f"  ! {i}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()

