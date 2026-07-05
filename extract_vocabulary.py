#!/usr/bin/env python3
"""Clean and refine vocabulary data extracted from 4 PEP English textbook PDFs."""

import json
import re
import os

PDF_FILES = [
    (r"C:\Users\Admin\.workbuddy\projects\c-Users-Admin-WorkBuddy-Claw\f8f2a481-4f4a-481b-a386-89f79c0572f6\tool-results\mcp-connector-proxy-ima-mcp_fetch_media_content-1783068694731-c6b419.txt", "七年级上册"),
    (r"C:\Users\Admin\.workbuddy\projects\c-Users-Admin-WorkBuddy-Claw\f8f2a481-4f4a-481b-a386-89f79c0572f6\tool-results\mcp-connector-proxy-ima-mcp_fetch_media_content-1783068771950-e82056.txt", "七年级下册"),
    (r"C:\Users\Admin\.workbuddy\projects\c-Users-Admin-WorkBuddy-Claw\f8f2a481-4f4a-481b-a386-89f79c0572f6\tool-results\mcp-connector-proxy-ima-mcp_fetch_media_content-1783068776569-b9793a.txt", "八年级上册"),
    (r"C:\Users\Admin\.workbuddy\projects\c-Users-Admin-WorkBuddy-Claw\f8f2a481-4f4a-481b-a386-89f79c0572f6\tool-results\mcp-connector-proxy-ima-mcp_fetch_media_content-1783068780719-9b2ff0.txt", "八年级下册"),
]

def load_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('content', '')

def extract_vocabulary_az(content):
    """Extract the 'Vocabulary A-Z' section - the main alphabetically sorted word list."""
    # Find the second occurrence of 'Vocabulary A-Z' or 'Vocabulary A–Z'
    pattern = r'Vocabulary\s+A[–-]Z'
    matches = list(re.finditer(pattern, content))
    if len(matches) >= 2:
        start = matches[1].start()
    elif len(matches) >= 1:
        start = matches[0].start()
    else:
        return ''

    # Find the end - look for 'Vocabulary from Primary School' or 'Reference Word List' or '后记'
    remaining = content[start + 100:]
    end_patterns = [r'Vocabulary\s+from\s+Primary\s+School', r'Reference\s+Word\s+List', r'后\s*记']
    end_pos = len(remaining)
    for ep in end_patterns:
        m = re.search(ep, remaining)
        if m and m.start() < end_pos:
            end_pos = m.start()

    return content[start:start + 100 + end_pos]

def extract_vocabulary_in_units(content):
    """Extract the 'Vocabulary in Each Unit' section."""
    pattern = r'Vocabulary\s+in\s+Each\s+Unit'
    matches = list(re.finditer(pattern, content))
    if len(matches) >= 2:
        start = matches[1].start()
    elif len(matches) >= 1:
        start = matches[0].start()
    else:
        return ''

    # End at 'Vocabulary A-Z'
    remaining = content[start + 100:]
    m = re.search(r'Vocabulary\s+A[–-]Z', remaining)
    if m:
        return content[start:start + 100 + m.start()]
    return content[start:start + 50000]

def extract_primary_school_vocab(content):
    """Extract 'Vocabulary from Primary School' section."""
    pattern = r'Vocabulary\s+from\s+Primary\s+School'
    matches = list(re.finditer(pattern, content))
    if len(matches) >= 2:
        start = matches[1].start()
    elif len(matches) >= 1:
        start = matches[0].start()
    else:
        return ''

    remaining = content[start + 100:]
    m = re.search(r'Reference\s+Word\s+List', remaining)
    if m:
        return content[start:start + 100 + m.start()]
    return content[start:start + 30000]

def parse_entries(text, source):
    """Parse vocabulary entries with improved regex."""
    entries = []

    # Main pattern: word /phonetic/ pos. meaning [p.XX]
    # The key improvement: stop meaning at the next word entry or page reference
    lines = text.split('\n')

    # Reconstruct cleaned lines by joining fragments
    cleaned_lines = []
    current_line = ''
    for line in lines:
        line = line.strip()
        if not line:
            if current_line:
                cleaned_lines.append(current_line)
                current_line = ''
            continue

        # If line starts with a word pattern (word /phonetic/), start new entry
        if re.match(r'^[a-zA-Z][a-zA-Z\'\-]*\s+/', line) or re.match(r'^[a-z][a-z\s]+[\u4e00-\u9fff]', line):
            if current_line:
                cleaned_lines.append(current_line)
            current_line = line
        else:
            # Continuation of previous line
            if current_line:
                current_line += ' ' + line
            else:
                current_line = line

    if current_line:
        cleaned_lines.append(current_line)

    # Parse each cleaned line
    pos_pattern = re.compile(
        r'^([a-zA-Z][a-zA-Z\'\-]*?)\s+'
        r'/([^/\n]+)/\s+'
        r'((?:n|v|adj|adv|prep|conj|pron|num|interj|art|aux|modal)\w*(?:\s*&\s*(?:n|v|adj|adv|prep|conj|pron|num|interj|art|aux|modal)\w*)*)\.\s*'
        r'(.+?)(?:\s+p\.\d+)?\s*$',
        re.IGNORECASE
    )

    simple_pos_pattern = re.compile(
        r'^([a-zA-Z][a-zA-Z\'\-]*?)\s+'
        r'/([^/\n]+)/\s+'
        r'(.+?)(?:\s+p\.\d+)?\s*$',
        re.IGNORECASE
    )

    # Pattern for phrases (no phonetic): "phrase Chinese meaning"
    phrase_pattern = re.compile(
        r'^([a-z][a-z\s]+?)\s+([\u4e00-\u9fff][^\n]*?)(?:\s+p\.\d+)?\s*$',
    )

    for line in cleaned_lines:
        # Remove page number references
        line = re.sub(r'\s*p\.\d+\s*', ' ', line).strip()
        # Remove section headers
        if re.match(r'^(Vocabulary|Reference|Unit|Starter|数词|基数词|序数词|月份|星期)', line):
            continue
        # Remove page numbers
        if re.match(r'^\d{2,3}', line):
            continue

        # Try main pattern (with explicit part of speech)
        m = pos_pattern.match(line)
        if m:
            word = m.group(1).strip().lower()
            phonetic = '/' + m.group(2).strip() + '/'
            pos = m.group(3).strip() + '.'
            meaning = m.group(4).strip()

            # Clean meaning - remove trailing content that looks like another entry
            meaning = clean_meaning(meaning)

            if is_valid_word(word, meaning):
                entries.append({
                    'word': word,
                    'phonetic': phonetic,
                    'pos': pos,
                    'meaning': meaning,
                    'source': source
                })
            continue

        # Try simple pattern (without explicit part of speech)
        m = simple_pos_pattern.match(line)
        if m:
            word = m.group(1).strip().lower()
            phonetic = '/' + m.group(2).strip() + '/'
            rest = m.group(3).strip()

            # Check if rest starts with part of speech
            pos_match = re.match(
                r'^((?:n|v|adj|adv|prep|conj|pron|num|interj|art|aux|modal)\w*(?:\s*&\s*(?:n|v|adj|adv|prep|conj|pron|num|interj|art|aux|modal)\w*)*)\.\s*(.+)',
                rest, re.IGNORECASE
            )
            if pos_match:
                pos = pos_match.group(1) + '.'
                meaning = clean_meaning(pos_match.group(2))
            else:
                pos = ''
                meaning = clean_meaning(rest)

            if is_valid_word(word, meaning):
                entries.append({
                    'word': word,
                    'phonetic': phonetic,
                    'pos': pos,
                    'meaning': meaning,
                    'source': source
                })
            continue

        # Try phrase pattern
        m = phrase_pattern.match(line)
        if m:
            phrase = m.group(1).strip().lower()
            meaning = m.group(2).strip()
            if len(phrase) > 1 and len(meaning) > 0:
                entries.append({
                    'word': phrase,
                    'phonetic': '',
                    'pos': '',
                    'meaning': meaning,
                    'source': source
                })

    return entries

def clean_meaning(meaning):
    """Clean up meaning text - remove trailing entries that got concatenated."""
    # Remove content after a pattern that looks like another word entry
    # e.g., "关于 adv. 大约wall /wɔːl/ n. 墙" -> "关于 adv. 大约"
    meaning = re.split(r'[a-z]+\s*/[^\s]+/', meaning)[0].strip()
    # Remove trailing "p.XX"
    meaning = re.sub(r'\s*p\.\d+\s*$', '', meaning).strip()
    return meaning

def is_valid_word(word, meaning):
    """Check if a word entry is valid."""
    if not word or len(word) < 1:
        return False
    if not meaning or len(meaning) < 1:
        return False
    # Skip if word is just a single letter (unless it has a meaningful entry)
    if len(word) == 1 and word not in ['a', 'i']:
        return False
    # Skip if meaning contains mostly English (parsing error)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', meaning))
    if chinese_chars < 1:
        return False
    return True

def extract_all():
    """Extract all vocabulary from all 4 PDFs."""
    all_entries = {}
    sources_count = {}

    for filepath, source_name in PDF_FILES:
        print(f"\nProcessing: {source_name}")
        content = load_content(filepath)
        print(f"  Content length: {len(content)} chars")

        # Extract all three vocabulary sections
        sections = []
        az_text = extract_vocabulary_az(content)
        if az_text:
            sections.append(('Vocabulary A-Z', az_text))
        unit_text = extract_vocabulary_in_units(content)
        if unit_text:
            sections.append(('Vocabulary in Each Unit', unit_text))
        prim_text = extract_primary_school_vocab(content)
        if prim_text:
            sections.append(('Vocabulary from Primary School', prim_text))

        print(f"  Found {len(sections)} vocabulary sections")

        for section_name, section_text in sections:
            entries = parse_entries(section_text, source_name)
            print(f"  {section_name}: {len(entries)} entries")

            for entry in entries:
                word = entry['word']
                if word not in all_entries:
                    all_entries[word] = entry
                    sources_count[word] = 1
                else:
                    sources_count[word] += 1
                    # Merge: prefer entries with more complete info
                    existing = all_entries[word]
                    if not existing['phonetic'] and entry['phonetic']:
                        existing['phonetic'] = entry['phonetic']
                    if not existing['pos'] and entry['pos']:
                        existing['pos'] = entry['pos']
                    if len(entry['meaning']) > len(existing['meaning']):
                        existing['meaning'] = entry['meaning']
                    if source_name not in existing['source']:
                        existing['source'] = existing['source'] + ', ' + source_name

    # Sort alphabetically
    sorted_entries = sorted(all_entries.values(), key=lambda x: x['word'].lower())

    print(f"\n=== Total unique words: {len(sorted_entries)} ===")

    # Print stats
    by_source = {}
    for e in sorted_entries:
        for s in e['source'].split(', '):
            by_source[s] = by_source.get(s, 0) + 1
    print("\nBy source:")
    for s, c in sorted(by_source.items()):
        print(f"  {s}: {c}")

    # Print first and last 10 for verification
    print("\n--- First 10 entries ---")
    for e in sorted_entries[:10]:
        print(f"  {e['word']} | {e['phonetic']} | {e['pos']} | {e['meaning'][:40]} | {e['source']}")

    print("\n--- Last 10 entries ---")
    for e in sorted_entries[-10:]:
        print(f"  {e['word']} | {e['phonetic']} | {e['pos']} | {e['meaning'][:40]} | {e['source']}")

    # Save to JSON
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vocabulary_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_entries, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to: {output_path}")

    return sorted_entries

if __name__ == '__main__':
    entries = extract_all()
