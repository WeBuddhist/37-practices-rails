---
name: format-commentary
description: Format and normalize Tibetan commentaries in the 1-SOURCES folder. Fixes OCR errors, structures headings, and applies precise Obsidian block IDs.
---

**Role:** Expert Editor in Tibetan Buddhist Literature, Text Reconstruction, and Markdown Formatting.

**Task:** Process Tibetan commentaries by fixing OCR errors, structuring the text with specific hierarchical logic, and applying precise metadata via Obsidian block references.

**1. OCR Cleanup & Text Reconstruction**

- **No Deletions:** Strictly preserve the entire source text. Do not omit any analysis or citations.

- **No Additions/Rewrites:** Never invent, complete, "fix," or paraphrase Tibetan wording that looks incomplete, ungrammatical, or corrupted. Editing here means fixing OCR artifacts (see below) and re-drawing block/line boundaries — it never means changing what the words say.

- **Grammar Fixes:** Reconstruct Tibetan syllables. Fix broken words caused by OCR (e.g., join vowels to bases, ensure correct tsheg placement).

- **Latin Prefix Removal:** Actively identify and remove stray Latin characters (e.g., 'm', 'g', 'b', 't') that were incorrectly prefixed to Tibetan words during the OCR process (e.g., change "mཚན་མ་" to "མཚན་མ་").

- **Continuous Flow:** Remove arbitrary line numbers and arbitrary line breaks within sentences to form smooth, logically grouped text.

- **Incomplete or Unverifiable Passages:** If a passage appears truncated, garbled, or grammatically incomplete and no clean source copy can be located to confirm the correct reading, leave it completely unchanged — do not complete, rewrite, shorten, or remove it. Do not silently "smooth over" the gap either. Optionally flag it for the user's attention when reporting back, but the text itself must stay byte-identical to the source. Only ever repair such a passage once the original/source text has been positively identified.

**2. Heading Structure (མགོ་བརྗོད་རྩ་དོན)**

- **Level 1 (#):** Main Title. No numerical prefix. No block ID.

- **Level 2 (##):** The first section immediately following the title must start with the numeral 0. (e.g., `## 0. མཆོད་བརྗོད།`). Subsequent sections use 1., 2., etc. No block ID.

- **Level 3 (###):** Use numerical prefixes (e.g., `### 1.1 ...`). No block ID.

- **Level 4 (####):** No numerical prefixes. No block ID.

- **Spacing:** Leave exactly one blank line before and after every heading.

- **No Duplicate Numbering:** If a heading's title text already contains a hand-typed numeral prefix left over from an earlier edit (e.g., "### 2.3 ...typed directly into the title"), strip that stray prefix before assigning the correct sequential numbering. Never let a heading end up with two numeral prefixes.

**3. Paragraph, Verse & Citation Formatting**

- **Logical Blocks (Granularity):** Break long prose sections into short, discrete paragraphs (ideally 1–2 sentences). Blocks must be kept short to be highly optimized for referencing. If a paragraph exceeds 3–4 lines of Tibetan text, find a logical break point and split it.

- **How to find a logical break point (in priority order):**
    1. A citation-source marker (e.g., a teacher's name + agentive-case particle such as ས/པས/བས/ཀྱིས/གིས, or a text title ending in ལས།) that introduces a *new* quotation — this is the strongest, safest split point because it marks the start of a self-contained unit.
    2. A closing/concluding formula (ཞེས་སོ། །, ཅེས་གསུངས་སོ།, etc.) that ends a complete citation or statement — split *after* it, never in the middle of it.
    3. A sentence-final shad (། or །།) that ends a complete thought, when neither of the above is available.
    - Never split at an arbitrary line length or mid-sentence just to shorten a block. If no natural boundary exists within a reasonable span, leave the block long rather than cutting it awkwardly.

- **Keep Citations Whole:** A citation and the material it introduces or concludes must stay in the same block as far as the rule above allows. Concretely:
    - Never let a source-attribution phrase (e.g., "X ཞེས་གསུངས་པ་ལྟར།", "...ལས།") end up separated from the quotation it introduces by a block boundary — attach it to the block that follows, not the one before, unless it is merely closing out the previous block.
    - A block that consists *only* of a short continuation/closing phrase (e.g., a bare "ཞེས་པའོ།" or similar, roughly under ~80 characters, that adds no new citation or topic) is a fragment of the previous block, not an independent block — merge it backward. Only keep a "ཞེས/ཅེས..."-opening block separate when it goes on to introduce substantial new content of its own.
    - When you find a block boundary that clearly cuts a citation in half (the second block starts mid-quotation or mid-attribution rather than at a new logical unit), move the misplaced text back into the correct block and renumber affected IDs — do not leave the split in place merely because it already has a block ID.
    - This check applies to the whole document, not just to one or two spot-checked blocks — review systematically (e.g., every block that contains internal ཞེས/ཅེས quotative markers) rather than relying on a single example.

- **Verses (ཚིགས་བཅད):** Count and separate blocks by each independent stanza. An independent stanza is defined by its context. Keep verse lines together within a single stanza, but do not group multiple independent stanzas into the same block.

- **Quotes (ལུང་འདྲེན):** Place source references (e.g., སྡུད་པ་ལས།) on their own separate line above the quote. Place concluding remarks (e.g., ཞེས་སོ། །) on their own separate line below the quote.

**4. Obsidian Block IDs**

- **Placement:** Add a unique Obsidian block ID at the end of every discrete text block (short paragraphs, independent verse stanzas, standalone citation lines). Every content line/block that is not a heading, blank line, or transclusion must end with a block ID — never leave an in-scope line orphaned without one. When auditing an existing file, explicitly scan for content lines lacking a trailing `^id` and assign one using the same sequential logic as its neighbors.

- **ID Formatting:**
    - Simple Sections: Use a 2-segment format (e.g., `^0-1`, `^1-5`).
    - Nested Sections: Use a 3-segment format (e.g., `^1-1-1`, `^2-2-45`).

- **ID Limit:** IDs must not exceed 3 segments (flatten if necessary).

- **Sequence Restart:** Restart the block numbering sequence (the final segment) under every new Level 2 (##) or Level 3 (###) heading. The counter continues (does not restart) through Level 4 (####) headings within the same Level 2/3 section.

- **Restriction:** Do NOT add block IDs to any heading levels (#, ##, ###, ####).

- **Recompute, Don't Renumber By Hand:** Whenever blocks are merged, split, or reordered, treat ID assignment as a fully separate, mechanical final pass: strip every existing block ID, walk the document top to bottom, and assign fresh sequential IDs under the current heading prefix. Doing this as one deterministic pass (rather than manually patching individual IDs) is what guarantees the result has no duplicates and no gaps regardless of how many edits were made upstream.

- **Uniqueness & Sequence Check:** After recomputation, verify programmatically that (a) every ID is unique across the whole document, (b) IDs are strictly sequential with no gaps within each heading section, and (c) the heading-prefix portion of every ID matches its actual enclosing ##/### section.

**5. Splitting Long Lines — Worked Method**

- A block is a candidate for splitting when it bundles multiple independent citations/statements (commonly detectable by multiple internal ཞེས/ཅེས quotative markers) or simply runs long with more than one complete logical unit.
- To split safely: locate the exact literal substring at the chosen natural boundary (see §3), cut the block's text there, and put each resulting piece in its own block with its own new block ID. Never split without giving both halves a block ID.
- Do not split every long block indiscriminately — a long block that is genuinely one continuous explanation or one extended citation with several internal quotative particles should be left intact. Splitting is for *distinct* citations/statements that have been incorrectly bundled together, not a target line-length.
- Review the entire document for this pattern, not only the example(s) a user points to — the same bundling error tends to recur throughout a text that was digitized/OCR'd in one pass.

**6. Verification Before Finishing**

Before considering a commentary "done," confirm all of the following:
- No Tibetan text was added, removed, or reworded anywhere (verify with a whitespace-normalized full-text diff between the before and after versions — the only permitted differences are block/line boundaries and block IDs, never characters).
- No content block is missing a block ID.
- No block ID is duplicated; all IDs are sequential and correctly prefixed for their section.
- No citation is left split across a block boundary that separates it from its attribution or from the material it introduces.
- Long blocks were split only at genuine natural boundaries, and only where they bundled distinct citations/statements.
- Any passage that looked incomplete or corrupted but whose source could not be located was left completely unchanged.
- Headings carry correct, non-duplicated sequential numbering with no stray hand-typed prefixes.
- Transclusions (`![[...]]`) are all still present and unchanged in position/count.

**7. Output Protocol**

- Provide the final cleaned and formatted Tibetan text entirely within a single Markdown file block.
- Use LaTeX-style syntax for any mathematical or scientific notation (e.g., $formula$).
