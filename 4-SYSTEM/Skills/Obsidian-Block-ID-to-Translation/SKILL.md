---
name: Obsidian-Block-ID-to-Translation and add transclusion of the original Tibetan root text to Translations
description: Stamp Obsidian block IDs onto Translations
---

# Obsidian Block IDs and Tibetan Root-Text Transclusions for Translations

## Description

Add Obsidian block IDs to the English translation file and insert accurate transclusions of the corresponding original Tibetan root text from:

`1-SOURCES/Text/LSDC14_TMZP_bo.md`

The skill works section by section and stanza by stanza. It must preserve the existing English translation and section structure and must match each English stanza with the correct Tibetan root-text stanza.

---

## Inputs

- **Translation file:** the target English translation file, typically under `1-SOURCES/Translations/`
    
- **Tibetan root text:** `1-SOURCES/Text/LSDC14_TMZP_bo.md`
    

The translation file must contain `##` section headings with their section block IDs already present.

---

## Rules

### 1. Keep the existing `##` section block IDs

Do not change, remove, or regenerate the block ID already attached to any `##` heading.

These `##` block IDs are the base IDs for everything inside that section.

For example:

```markdown
## Introduction ^I-0
## Main Text ^1-0
## Conclusion ^2-0
## Colophon ^a-0
```

---
### 2. Add block IDs to `###` and `####` headings

Add block IDs to all `###` and `####` headings according to the block ID of their enclosing `##` section.

Examples:

```markdown
## Main Text ^1-0
### The First Practice ^1-1-0
#### Explanation ^1-1-1-0
```

Use the existing numbering pattern of the file where applicable.

Rules:
- Every `###` heading must have a block ID.
- Every `####` heading must have a block ID.
- Do not create unnecessary deeper heading levels.
- Do not change the heading text.
- Do not change an existing correct heading ID.
- Keep the hierarchy consistent with the enclosing `##` section.
    

---

### 3. Add block IDs to the end of every Shloka/Stanza

Each English Shloka or stanza must have one block ID at the **end of its final line**.

The ID must follow the block-ID sequence of its enclosing `##` section.

For example:

```markdown
## Main Text ^1-0

The practice of all the bodhisattvas is to study, reflect and meditate,
Tirelessly, both day and night, without ever straying into idleness,
In order to free oneself and others from this ocean of saṃsāra,
Having gained this supreme vessel—a free, well-favoured human life, so difficult to find. ^1-1

The next practice is...
...
^1-2
```

Important:

- One complete Shloka/Stanza = one block ID.
- Put the ID only at the end of the stanza's final line.
- Do not put a separate ID on every line of a stanza.
- Continue the numbering according to the enclosing `##` section.
- Do not restart the stanza numbering at every `###` or `####`.
- Do not modify the English translation itself.
- Preserve punctuation and line breaks unless a change is absolutely necessary to correctly identify the stanza boundary.
    

---

### 4. Add Tibetan root-text transclusions Shloka by Shloka

Use:

`1-SOURCES/Text/LSDC14_TMZP_bo.md`

as the authoritative source for the original Tibetan root text.

For **every English root-text Shloka/Stanza**, find the exact corresponding Tibetan root-text block and insert its transclusion **directly above the English Shloka/Stanza**.

Example:

```markdown
![[LSDC14_TMZP_bo.md#^1-1]]

The practice of all the bodhisattvas is to study, reflect and meditate,
Tirelessly, both day and night, without ever straying into idleness,
In order to free oneself and others from this ocean of saṃsāra,
Having gained this supreme vessel—a free, well-favoured human life, so difficult to find. ^1-1
```

The transclusion must point to the **actual corresponding block ID in the Tibetan root-text file**.

---

### 5. Match the Tibetan and English versions accurately

Do not match root-text blocks only by their sequence number or position.

For each English Shloka/Stanza:

1. Read the English text.
2. Locate the corresponding Tibetan root text in `LSDC14_TMZP_bo.md`.
3. Confirm that the Tibetan passage and English translation correspond in meaning and sequence.
4. Use the exact Tibetan root-text block ID.
5. Insert that transclusion immediately above the English Shloka/Stanza.

The goal is an accurate **Tibetan root text ↔ English translation** correspondence.

Do not assume that `^1-10` in the Tibetan file automatically corresponds to the tenth English stanza. Verify the actual text.

---

### 6. Do not skip or invent root-text blocks

Every English root-text Shloka/Stanza that corresponds to the Tibetan source must have a transclusion.

Do not:
- skip a stanza,
- reuse the wrong Tibetan block,
- invent a Tibetan block ID,
- guess a correspondence,
- insert a transclusion merely because the numbering appears similar.

If the corresponding Tibetan text cannot be confidently identified, search the root-text file again using the actual Tibetan/English passage and surrounding context before making a decision.

If a genuine correspondence still cannot be established, flag it for review rather than inserting an incorrect transclusion.

---
### 7. Preserve existing correct transclusions

If a correct Tibetan root-text transclusion already exists:
- keep it,
- do not duplicate it,
- do not replace it unnecessarily.

If an existing transclusion points to the wrong Tibetan block, correct it only after verifying the proper correspondence.

---
### 8. Do not modify the actual text

This skill is for **structure, block IDs, and root-text transclusions**.

Do not:
- rewrite the English translation,
- retranslate the text,
- change Tibetan text,
- correct the translator's wording,
- change punctuation unnecessarily,
- change the meaning,
- rearrange Shlokas/Stanzas,
- merge or split Shlokas unless the source structure clearly requires it.

Preserve the existing content as much as possible.

---
## Procedure

### Step 1 — Read the translation structure

Identify:
- the `##` sections and their existing block IDs,
- all `###` and `####` headings,
- all English Shlokas/Stanzas,
- any existing block IDs,
- any existing Tibetan transclusions.

### Step 2 — Add subsection IDs

For every `###` and `####` heading, add or correct its block ID according to the enclosing `##` section.

Do not alter the existing `##` IDs.

### Step 3 — Identify every English Shloka/Stanza

Read each section carefully and determine the exact beginning and end of every Shloka/Stanza.

Add one block ID to the final line of each Shloka/Stanza.

### Step 4 — Match each stanza with the Tibetan root text

Search:

`1-SOURCES/Text/LSDC14_TMZP_bo.md`

and identify the exact Tibetan root-text block corresponding to each English Shloka/Stanza.

### Step 5 — Insert transclusions

Insert the verified Tibetan transclusion immediately above its corresponding English Shloka/Stanza.

Use this format:

```markdown
![[LSDC14_TMZP_bo.md#^BLOCK-ID]]
```

### Step 6 — Final verification

Check the complete file for:
- every `##` section retaining its original block ID,
- every `###` heading having a correct block ID,
- every `####` heading having a correct block ID,
- every English Shloka/Stanza having one block ID at its end,
- every root-text Shloka/Stanza having the correct Tibetan transclusion immediately above it,
- no missing transclusions,
- no incorrect or duplicated transclusions,
- no duplicate block IDs,
- no unnecessary changes to the English translation or structure.

## Completion Checklist

-  All existing `##` block IDs are preserved.
-  All `###` headings have correct block IDs.
-  All `####` headings have correct block IDs.
-  Every English Shloka/Stanza has one block ID at its end.
-  Block IDs follow the numbering of their enclosing `##` section.
-  Every English root-text Shloka/Stanza has a Tibetan root-text transclusion directly above it.
-  Every transclusion points to the exact corresponding block in `LSDC14_TMZP_bo.md`.
-  Tibetan and English versions have been checked for actual correspondence, not merely matching numbers.
-  No root-text stanza has been skipped.
-  No incorrect or duplicate transclusions have been added.
-  No unnecessary changes have been made to the original text.
-  No duplicate block IDs remain.
