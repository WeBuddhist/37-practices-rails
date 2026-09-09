---
name: format-root-text
description: Format and normalise source files (root texts, translations, commentaries) in the 1-Human-Sources/ folder. Handles frontmatter, block IDs (including Chapter 0), heading structures (TOC), and cleaning OCR artifacts. Reference [[1-Human-Sources-Guideline]] for standards.
---
# Root-text verse format (real example)

Source pattern seen in this project's vault for root-text  (e.g. `LSDC14_TMZP-bo.md`, the Tibetan language རྒྱལ་སྲས་ལག་ལེན་སོ་བདུན་མ།).

```markdown
---
title: རྒྱལ་སྲས་ལག་ལེན་སོ་བདུན་མ།
...
verse_id_format: chapter-verse
root_text: 1-SOURCES/Text/LSDC14_TMZP-bo.md
covers_verses: 1-1–10-61?
...
---
# རྒྱལ་སྲས་ལག་ལེན་སོ་བདུན་མ། ^0

## 0. ཀླད་ཀྱི་དོན། ^I-0

༄༅༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར། ^I-1

བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། ^I-2

## 1. ལེའུ་དང་པོ། བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ། ^1-0

![[1-SOURCES/Text/BCAV08_SH_sk.md#^1-1]]

བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །
ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །
བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །
ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། ། ^1-1

![[1-SOURCES/Text/BCAV08_SH_sk.md#^1-2]]

སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །
...
```

And at the very end, after the last chapter, a colophon:

```markdown
## འགྱུར་བྱང། ^b-0

རྒྱ་གར་གྱི་མཁན་པོ་སརྦ་ཛྙཱ་དེ་བ་དང་། ... ^b-1
...
```
# Format Root Text

This skill normalises source files (root texts, translations, and commentaries) in the `1-Human-Sources/` folder to meet the project's structural and linking standards. 

## Core Principles
Before processing any file, review **[[1-Human-Sources-Guideline]]**. The block ID is the single most important linking mechanism in the vault.

### 1. Heading Structure (TOC)
- **Level 2 (`##`)**: Author-defined books or chapters.
- **Level 3 (`###`)**: Author-defined sub-sections (e.g., from the author's own Table of Contents).
- **Level 4 (`####`)**: DO NOT USE. Block IDs replace verse-level headings.
- **Chapter 0**: Any content preceding Chapter 1 (titles, colophons, homages, scribal intros) MUST be placed under a `## 0. ཀླད་ཀྱི་དོན། heading.

### 2. Block ID Format
- **Standard**: `^chapter-verse` (e.g., `^1-1`, `^6-33`).
- **Chapter 0**: Verses in the introduction section use `^0-verse` (e.g., `^0-1`, `^0-2`).
- **No Zero-Padding**: Use `^6-33`, NOT `^06-033`.
- **Placement**: At the end of the last line of the verse/passage, preceded by a single space.
- **Numbering**: Verse numbers restart at 1 for each chapter. Convert continuous numbering to per-chapter numbering.

---

## Step 1 — Audit and Identification
Identify files in `1-Human-Sources/` that lack frontmatter, have missing/incorrect block IDs, or have stray line numbers from OCR/PDF extraction.

## Step 2 — Process Formatting
For each file:
1. **Insert/Update Frontmatter**: Ensure the YAML block is at the very top.
2. **Standardise Headings**:
    - Ensure Chapter 1 starts with `## 1. [Title]`.
    - Ensure pre-chapter material is under `## 0. Introduction`.
    - Map author-defined structural divisions to `##` and `###`.
3. **Apply Block IDs**:
    - Add `^0-n` to introduction verses.
    - Add `^c-v` to chapter verses, restarting `v` at 1 for each `c`.
    - For Sanskrit, extract verse numbers from `॥N॥`.
    - For Tibetan, count verses (runs of lines ending in `། །`).
4. **Clean Content**:
    - Remove OCR artifacts, page numbers, and stray line-number prefixes (e.g., `7.`, `42.`).
    - Restore two-line formatting for Sanskrit verses if hemistichs are run together.

## Step 3 — Frontmatter Fields
Minimum required fields:
```yaml
---
title: 
author: 
language: 
file_type: root-text | commentary | translation | edition
lang_tag: sk | bo | zh | en | pi
source_description: "Detailed source info (required)"
verse_id_format: chapter-verse | verse | book-chapter-verse
---
```
For commentaries/translations, also include:
- `root_text: [[Path/to/root-text]]`
- `covers_verses: "1-1–10-58"`

## Step 4 — Commentary Specifics
- Commentary passages should use their own block ID system (declared in `verse_id_format`).
- Transclude the relevant root verse(s) immediately before the commentary on that verse: `![[Path/to/root-text#^1-1]]`.
- Use sequential individual transclusions for multi-verse sections.

---

## Dos and Don'ts
- **DO** work on one file at a time.
- **DO** use editorial notes `[Ed: ...]` in English for ambiguous cases.
- **DO** preserve original Tibetan/Chinese scripts in content while using English for metadata.
- **DON'T** renumber verses based on your own interpretation; follow the source's logical structure.
- **DON'T** put block IDs on heading lines.
- **DON'T** use `####` headings.