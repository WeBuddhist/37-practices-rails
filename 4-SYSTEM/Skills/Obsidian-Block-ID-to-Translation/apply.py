#!/usr/bin/env python3
"""
apply.py — Obsidian-Block-ID-to-Translation helper.

Subcommands:
  audit <file>          Report per-## section (label, first id, last id, body count).
                         Aborts (no write) if any ## heading is missing a manual ^{label}-0 id.
  apply <file> [out]     Tag the title, ###/#### sub-headings, and body-text blocks with
                         Obsidian block ids, keyed off each ##'s manual label. Writes to
                         `out` if given, else overwrites `file` in place. `##` heading lines
                         are never modified. Idempotent: re-running on tagged output is a no-op.
"""
import re
import sys

HEADING_RE = re.compile(r'^(#{1,6})\s+')
TRANSCLUSION_RE = re.compile(r'^!\[\[.*\]\]\s*$')
ID_SUFFIX_RE = re.compile(r'\^([^\s\^]+)$')          # trailing ^token at end of (rstripped) line
HEADING_ID_RE = re.compile(r'\^([^\s\^]+)-0$')        # trailing ^{label}-0 at end of a heading line


def read_lines(path):
    with open(path, 'r', encoding='utf-8', newline='') as f:
        return f.readlines()


def write_lines(path, lines):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.writelines(lines)


def split_frontmatter(lines):
    if lines and lines[0].rstrip('\n') == '---':
        for i in range(1, len(lines)):
            if lines[i].rstrip('\n') == '---':
                return lines[:i + 1], lines[i + 1:]
    return [], lines


def heading_level(line):
    m = HEADING_RE.match(line.rstrip('\n'))
    return len(m.group(1)) if m else None


def has_trailing_id(line):
    stripped = line.rstrip('\n').rstrip()
    return bool(ID_SUFFIX_RE.search(stripped))


def append_id(line, new_id):
    newline = '\n' if line.endswith('\n') else ''
    core = (line[:-1] if newline else line).rstrip()
    return f"{core} ^{new_id}{newline}"


def find_missing_h2_ids(body, offset):
    missing = []
    for i, line in enumerate(body):
        if heading_level(line) == 2:
            stripped = line.rstrip('\n').rstrip()
            if not HEADING_ID_RE.search(stripped):
                missing.append((offset + i + 1, stripped))
    return missing


def process(body, dry_run):
    """Walk body lines, tagging in place (unless dry_run) per the skill rules.
    Returns a list of per-section report dicts (label, heading_line, first_id, last_id, body_count).
    """
    current_label = None
    h3 = 0
    h4 = 0
    n = 0
    pending = []
    sections = []
    cur_section = None

    def finalize_block():
        nonlocal n, pending
        if not pending:
            return
        last_idx = pending[-1]
        last_line = body[last_idx]
        if has_trailing_id(last_line):
            stripped = last_line.rstrip('\n').rstrip()
            m = ID_SUFFIX_RE.search(stripped)
            tag = m.group(1)
            prefix = f"{current_label}-"
            if tag.startswith(prefix) and tag[len(prefix):].isdigit():
                n = max(n, int(tag[len(prefix):]))
                if cur_section is not None:
                    cur_section['last_id'] = tag
                    if cur_section['first_id'] is None:
                        cur_section['first_id'] = tag
            # else: manual override with a different label — leave counter untouched
            pending = []
            return
        n += 1
        new_id = f"{current_label}-{n}"
        if not dry_run:
            body[last_idx] = append_id(last_line, new_id)
        if cur_section is not None:
            cur_section['body_count'] += 1
            cur_section['last_id'] = new_id
            if cur_section['first_id'] is None:
                cur_section['first_id'] = new_id
        pending = []

    for i, line in enumerate(body):
        lvl = heading_level(line)
        if lvl is not None:
            finalize_block()
            stripped = line.rstrip('\n').rstrip()
            if lvl == 1:
                if not has_trailing_id(line) and not dry_run:
                    body[i] = append_id(line, '0')
            elif lvl == 2:
                m = HEADING_ID_RE.search(stripped)
                current_label = m.group(1)
                h3 = 0
                h4 = 0
                n = 0
                cur_section = {'label': current_label, 'line': i, 'heading': stripped,
                                'first_id': None, 'last_id': None, 'body_count': 0}
                sections.append(cur_section)
                # ## lines are never modified
            elif lvl == 3:
                if has_trailing_id(line):
                    m2 = HEADING_ID_RE.search(stripped)
                    if m2:
                        tag = m2.group(1)
                        prefix = f"{current_label}-"
                        if tag.startswith(prefix) and tag[len(prefix):].isdigit():
                            h3 = max(h3, int(tag[len(prefix):]))
                    h4 = 0
                else:
                    h3 += 1
                    h4 = 0
                    if not dry_run:
                        body[i] = append_id(line, f"{current_label}-{h3}-0")
            elif lvl == 4:
                if h3 == 0:
                    print(f"ABORT: line {i+1}: #### with no enclosing ### heading: {stripped!r}",
                          file=sys.stderr)
                    sys.exit(2)
                if has_trailing_id(line):
                    m2 = HEADING_ID_RE.search(stripped)
                    if m2:
                        tag = m2.group(1)
                        prefix = f"{current_label}-{h3}-"
                        if tag.startswith(prefix) and tag[len(prefix):].isdigit():
                            h4 = max(h4, int(tag[len(prefix):]))
                else:
                    h4 += 1
                    if not dry_run:
                        body[i] = append_id(line, f"{current_label}-{h3}-{h4}-0")
            else:
                print(f"ABORT: line {i+1}: ##### and deeper are not supported: {stripped!r}",
                      file=sys.stderr)
                sys.exit(2)
        elif TRANSCLUSION_RE.match(line.rstrip('\n')):
            finalize_block()
            # transclusion lines are structural: never tagged, never counted
        elif line.strip() == '':
            finalize_block()
        else:
            pending.append(i)
    finalize_block()
    return sections


def audit(path):
    lines = read_lines(path)
    fm, body = split_frontmatter(lines)
    offset = len(fm)
    missing = find_missing_h2_ids(body, offset)
    if missing:
        print("ABORT: the following ## headings are missing a manual ^{label}-0 id:")
        for ln, txt in missing:
            print(f"  line {ln}: {txt}")
        return 1
    sections = process(body, dry_run=True)
    print(f"{'label':<8} {'heading':<40} {'first id':<10} {'last id':<10} body_count")
    for s in sections:
        heading_txt = s['heading'][:38]
        print(f"{s['label']:<8} {heading_txt:<40} {str(s['first_id']):<10} {str(s['last_id']):<10} {s['body_count']}")
    return 0


def apply(path, outpath=None):
    lines = read_lines(path)
    fm, body = split_frontmatter(lines)
    offset = len(fm)
    missing = find_missing_h2_ids(body, offset)
    if missing:
        print("ABORT: the following ## headings are missing a manual ^{label}-0 id; nothing written:")
        for ln, txt in missing:
            print(f"  line {ln}: {txt}")
        return 1
    process(body, dry_run=False)
    target = outpath if outpath else path
    write_lines(target, fm + body)
    print(f"Wrote {target}")
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'audit':
        sys.exit(audit(sys.argv[2]))
    elif cmd == 'apply':
        out = sys.argv[3] if len(sys.argv) > 3 else None
        sys.exit(apply(sys.argv[2], out))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
