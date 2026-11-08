"""
tools/chapters.py — YouTube Validated Chapter Generator

Validates and generates timestamps for video descriptions according to YouTube's strict rules:
1. The first chapter MUST start at 00:00 (or 0:00).
2. There must be at least 3 chapters in ascending order.
3. Each chapter must be at least 10 seconds long.
"""

import sys
import re
import argparse


def parse_srt(srt_content: str) -> list:
    """Parses an SRT file into timecoded subtitle entries."""
    pattern = re.compile(
        r'(\d+)\s*\n'
        r'(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n'
        r'(.*?)(?=\n\s*\n|\Z)',
        re.DOTALL
    )
    entries = []
    for match in pattern.finditer(srt_content):
        start_raw = match.group(2).replace(',', '.')
        text = match.group(4).replace('\n', ' ').strip()
        h, m, s = start_raw.split(':')
        seconds = int(h) * 3600 + int(m) * 60 + float(s)
        entries.append({
            "seconds": int(seconds),
            "timestamp": f"{int(m):02d}:{int(float(s)):02d}",
            "text": text
        })
    return entries


def validate_chapters(chapters: list) -> dict:
    """Validates a list of chapter tuples: [(seconds, 'MM:SS', 'Title'), ...]"""
    errors = []
    
    if not chapters:
        return {"valid": False, "errors": ["No chapters provided."]}

    # Rule 1: Starts at 00:00
    if chapters[0][0] != 0:
        errors.append(f"First chapter starts at {chapters[0][1]} instead of 00:00.")

    # Rule 2: Minimum 3 chapters
    if len(chapters) < 3:
        errors.append(f"YouTube requires at least 3 chapters (found {len(chapters)}).")

    # Rule 3: Minimum 10 seconds apart
    for i in range(1, len(chapters)):
        diff = chapters[i][0] - chapters[i - 1][0]
        if diff < 10:
            errors.append(f"Chapter '{chapters[i][2]}' is only {diff}s after previous chapter (minimum 10s required).")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "formatted": "\n".join(f"{ch[1]} {ch[2]}" for ch in chapters)
    }


def main():
    parser = argparse.ArgumentParser(description="Validate and format YouTube chapters.")
    parser.add_argument("--srt", type=str, help="Path to .srt file to extract and summarize")
    args = parser.parse_args()

    if args.srt:
        try:
            with open(args.srt, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            entries = parse_srt(content)
            print(f"Extracted {len(entries)} subtitles from {args.srt}.")
        except Exception as e:
            print(f"Error reading SRT: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

