"""
Strip [Source: ...], [E1], [E2], [E3], [E4], [R1], [R2], [T1 Ch.X], [O1], etc.
citation tags from the explanation and analogy fields in seed_batch1.py and seed_batch2.py.
Run from the backend/ folder.
"""
import re
import sys
import os

def strip_citations(text: str) -> str:
    """Remove all source/citation markers from lesson text."""
    # Pattern matches things like:
    #   [Source: T1 Ch.2, O1]
    #   [Source: E1 — Farah et al., 2023]
    #   [E1], [E2], [E3], [E4]
    #   [R1], [R2]
    #   [T1 Ch.X], [T2 Ch.X], [O1], [O2], etc.
    patterns = [
        r'\s*\[Source:[^\]]+\]',        # [Source: ...]
        r'\s*\[[ETOR]\d+[^\]]*\]',       # [E1], [R2], [T1 Ch.2], [O1] etc.
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    # Clean up any double spaces or trailing spaces on lines
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    return '\n'.join(lines)


def process_file(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Find all string literals that look like explanation/analogy content
    # Replace [Source: ...] and citation tags inside Python string contents
    cleaned = strip_citations(content)

    if cleaned == original:
        print(f"  No changes needed in {os.path.basename(filepath)}")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    # Count removals
    removed = len(re.findall(r'\[Source:[^\]]+\]|\[[ETOR]\d+[^\]]*\]', original))
    print(f"  Cleaned {removed} citation(s) from {os.path.basename(filepath)}")


if __name__ == '__main__':
    base = os.path.dirname(__file__)
    files = [
        os.path.join(base, 'seed_batch1.py'),
        os.path.join(base, 'seed_batch2.py'),
    ]
    for f in files:
        print(f"Processing {f}...")
        process_file(f)
    print("Done. Re-run seed scripts to update the database.")
