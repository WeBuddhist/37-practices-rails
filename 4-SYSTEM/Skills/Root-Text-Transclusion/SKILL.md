---
name: Root-Text-Transclusion
description: Insert Obsidian transclusions of a root text's block-tagged
  passages into the corresponding locations of a commentary that quotes it.
---

# Root-Text-Transclusion

This skill adds Obsidian transclusion links (`![[<root-text-file>#^ID]]`) from an already block-ID-tagged root-text file into a commentary that quotes or discusses that root text, one block at a time, placing each transclusion directly above the corresponding root-text passage as it appears (quoted, paraphrased-but-still-quoted, or reproduced) in the commentary. The goal is a commentary file where every root-text passage it quotes is anchored to a live, clickable transclusion of the authoritative source, so nothing drifts between the two files over time.

The root text's own block-ID system (`^I-1`, `^1-1`, `^2-1`, …, produced by the `Obsidian-Block-ID-to-Commentary` skill or equivalent hand-tagging) is walked start to finish, section by section, and is never confused with the commentary's own independent block-ID system (e.g. `^1-0-3`, `^1-3-5`) — the two id schemes coexist in the same commentary file but belong to different documents and are never mixed.

---

## Inputs

- `root_text` — path to the root-text markdown file, typically under `1-SOURCES/Text/`. It must already carry a complete, correctly-ordered block-ID structure (`##` section labels each ending `-0`, body blocks numbered sequentially within each section, e.g. `^I-1…^I-n`, `^1-1…^1-n`, `^2-1…^2-n`). This skill treats that file as read-only ground truth.
- `commentary` — path to the commentary markdown file, typically under `1-SOURCES/Commentaries/`, that quotes or discusses the root text. It may already contain some correct transclusions (e.g. worked examples the human contributor added by hand) and may already carry its own, unrelated block-ID tagging from `Obsidian-Block-ID-to-Commentary`.

## Output

- The same `commentary` file modified in place, with one `![[<root_text_filename>#^ID]]` line (followed by a blank line) inserted directly above every commentary passage that quotes or reproduces the corresponding root-text block, for every root-text block that is actually quoted. Existing correct transclusions are left untouched. Root-text blocks that, after thorough verification, are genuinely never quoted (only summarized/paraphrased in the commentator's own words) are correctly left without a transclusion. The root text file itself is never modified. No commentary content is rearranged, rewritten, merged, or otherwise changed beyond inserting the transclusion lines.

---

## Output file format

Given a root text already tagged like:

```
## ཀླད་ཀྱི་དོན། ^I-0
### མཆོད་བརྗོད། ^I-1-0
ན་མོ་ལོ་ཀེ་ཤྭ་ར་ཡ། ^I-1
...verse... ^I-2
## གཞུང་དོན་དངོས། ^1-0
...verse 1... ^1-1
...verse 2... ^1-2
## མཇུག་གི་དོན། ^2-0
...colophon verse 1... ^2-1
```

and a commentary that quotes those same passages in the same order, the skill inserts a transclusion immediately above each quoted block:

```
### མདོར་བསྟན་པ། ^I-2-1-0

![[LSDC14_TMZP-bo.md#^I-1]]

དེ་ལ་རྒྱལ་བའི་སྲས་པོ་ཐོགས་མེད་བཟང་པོ་དཔལ་གྱིས་མཛད་པའི་... ^I-4

![[LSDC14_TMZP-bo.md#^I-2]]

...commentary prose discussing that verse... ^I-5

#### དལ་འབྱོར་དོན་ཡོད། ^1-2-1-0

![[LSDC14_TMZP-bo.md#^1-1]]

དང་པོ་རྙེད་དཀའི་དལ་འབྱོར་དོན་ཡོད་པར་བྱ་བ་ནི། ། ^1-1
...quoted verse continues... ^1-2

### གང་གི་དོན་དུ་ཇི་ལྟར་བརྩམས་པ། ^2-1-0

![[LSDC14_TMZP-bo.md#^2-1]]

དང་པོ་ནི། ^2-1
...quoted colophon verse... ^2-2
```

Note: the transclusion's target file name and block id are the *root text's own*, never the commentary's own block ids that may appear later on the same lines (those belong to a different, unrelated numbering system and are left exactly as they were).

---

## Rules

1. **Walk the root text section by section, in order, using its own existing block-ID structure as the checklist.** Each top-level `##` section of the root text has its own independent id run (e.g. `^I-1…^I-n` for the first section, `^1-1…^1-n` for the second, `^2-1…^2-n` for the third, or whatever labels that particular root text actually uses) — never renumber, relabel, or invent a different scheme, and never let one section's numbering run into another's.
2. **Never silently skip a root-text block.** If a block cannot be found quoted anywhere in the commentary on a first pass, search again before concluding it is genuinely absent: check for line-break differences, punctuation or spacing variants, OCR artifacts, and passages the commentary quotes out of strict sequence or split across two locations. Only after this thorough search may a block be left without a transclusion — and when that happens, note explicitly (to the human contributor, in the completion report) which block it was and why it was judged absent (e.g. "discussed only in paraphrase, never directly quoted").
3. **Match by the actual Tibetan wording, not by position or assumption.** The correspondence between a root-text block and a commentary passage must be verified against the real text of both — never inferred merely from running order, paragraph position, or "this is probably verse N because it's the Nth quote block found." Two adjacent root-text blocks are sometimes quoted out of order, split, or combined in a commentary; matching on content catches this, matching on position does not.
4. **Never confuse the root text's transclusion ids with the commentary's own block-ID system.** A commentary passage may carry its own unrelated block id (from `Obsidian-Block-ID-to-Commentary`, e.g. `^1-0-3`) on the very same line the transclusion sits above — that id is untouched and irrelevant to which root-text id the transclusion should reference. Only the root text file's own ids (as found in `root_text`) are ever used inside a `![[...]]` link.
5. **Preserve every existing, correct transclusion exactly as found.** Do not duplicate a transclusion that is already correctly placed, and do not re-derive or re-verify blocks that already have one unless there is a specific reason to doubt it (e.g. it appears to reference the wrong id). Continue the walk from the next block that is missing one.
6. **Never modify the root text file.** No rewriting, translating, modernizing spelling, changing punctuation or wording, or "correcting" it in any way — it is read-only ground truth for this skill.
7. **Never modify commentary content beyond inserting transclusion lines.** No rearranging paragraphs, rewriting prose, merging or splitting blocks, or changing any existing block id (of either numbering system) merely for convenience. The only new lines added are `![[...]]` + a blank line.
8. **A transclusion always goes immediately above the root-text passage it points to**, as its own line followed by a blank line, never inline, never below, never separated from the passage by unrelated commentary text.
9. **Completeness over speed.** When uncertain whether a block is quoted, investigate further (reread the surrounding commentary prose, recheck for near-duplicate wording) rather than guessing or leaving a block unresolved.

---

## Procedure

1. **Read `root_text` in full** and extract its complete block-ID structure: every `##` section label and every body-block id within it, in order, together with the actual text each id anchors (needed later for content matching).
2. **Read `commentary` in full** and note any transclusions already present (target file + id), so they can be preserved and excluded from the walk.
3. **Walk the root text's blocks in order, one `##` section at a time.** For each block not already transcluded in the commentary:
   - Search the commentary for a passage whose wording matches that block's actual text (quoted verbatim, or reproduced with only the kind of minor variation described in Rule 3).
   - If found, insert `![[<root_text_filename>#^ID]]` plus a blank line immediately above that passage.
   - If not found on first search, search again per Rule 2 before concluding it is genuinely absent; if still absent, leave it untranscluded and record it for the completion report.
4. **Verify content correspondence, not just sequence.** For every inserted transclusion, confirm the commentary passage it sits above actually corresponds to that root-text block's wording (a normalized text-similarity comparison against the root text is a reliable check) — never rely solely on the fact that blocks were processed in order.
5. **Final full audit, per `##` section of the root text:**
   - No block silently skipped (every block is either transcluded or explicitly recorded as genuinely absent, with reason).
   - No duplicate transclusions.
   - No transclusion references the wrong root-text id.
   - Each section's transclusion ids appear in strictly increasing order with no gaps other than recorded absences.
   - No mixing between different sections' numbering (e.g. no `^I-*` id appearing where a `^1-*` id belongs, or vice versa).
   - Every transclusion sits immediately above its corresponding passage.
   - All pre-existing, correct transclusions are still present and unchanged.
   - The root text file is unmodified (diff against its original content is empty).
   - No commentary content besides the inserted transclusion lines has changed (diff the commentary before/after with all transclusion lines stripped from both sides — it should be empty).
6. **Report to the human contributor**: total transclusions present (pre-existing + newly added), any blocks left genuinely untranscluded and why, and confirmation that the audit in step 5 passed.

---

## Completion check

- [ ] Root text's full block-ID structure (all sections, all ids, actual text) extracted before any commentary edits began
- [ ] Every pre-existing transclusion in the commentary identified and preserved untouched
- [ ] Every root-text block walked in order; none silently skipped
- [ ] Any block left untranscluded was searched for thoroughly first, and is recorded with a stated reason for absence
- [ ] Every inserted transclusion verified against the root text's actual wording, not assumed from position alone
- [ ] No transclusion mixes one section's numbering system with another's
- [ ] No duplicate transclusions
- [ ] Every transclusion placed immediately above its corresponding passage, as its own line plus a blank line
- [ ] Root text file diff-empty against its original (completely unmodified)
- [ ] Commentary diff-empty against its original once all transclusion lines are stripped from both (no unintended content changes)
- [ ] Final per-section audit (sequential order, no gaps beyond recorded absences, no wrong references) completed and passed
- [ ] Final tagged file written to the correct vault path
