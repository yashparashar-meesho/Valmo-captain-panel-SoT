#!/usr/bin/env python3
"""Markdown -> HTML, with the subset this project actually writes.

Extracted from build_docs_preview.py so the review page and the DRD renderer
share one converter. A second copy of a converter drifts exactly like a second
copy of a fact.

Handles: headings, paragraphs, lists, GFM pipe tables, fenced code, inline
code, bold, italic, links, blockquotes, hr, HTML comments.
"""
import html
import re


# ---------------------------------------------------------------- inline ----
def inline(s):
    """Inline markdown -> HTML. Code spans are extracted first so nothing
    inside them is treated as markup."""
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    s = re.sub(r"`([^`]+)`", stash, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"<em>\1</em>", s)
    s = re.sub(r"\x00(\d+)\x00",
               lambda m: "<code>%s</code>" % html.escape(spans[int(m.group(1))], quote=False), s)
    return s


def cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    # a escaped pipe inside a cell is content, not a separator
    parts, buf = [], ""
    i = 0
    while i < len(row):
        if row[i] == "\\" and i + 1 < len(row) and row[i + 1] == "|":
            buf += "|"
            i += 2
        elif row[i] == "|":
            parts.append(buf)
            buf = ""
            i += 1
        else:
            buf += row[i]
            i += 1
    parts.append(buf)
    return [p.strip() for p in parts]


# ----------------------------------------------------------------- block ----
def md(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):                                   # fenced code
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf), quote=False))
            continue

        if ln.strip().startswith("<!--"):                          # comment
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", ln)                       # heading
        if m:
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv))
            i += 1
            continue

        if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\-*_]*$", ln):       # hr
            out.append("<hr>"); i += 1; continue

        if ln.lstrip().startswith("|") and i + 1 < len(lines) \
           and re.match(r"^\s*\|?[\s:\-|]+\|[\s:\-|]*$", lines[i + 1]):
            head = cells(ln)
            i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body.append(cells(lines[i])); i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % inline(h) for h in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                r = (r + [""] * len(head))[:len(head)]
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        if ln.lstrip().startswith(">"):                            # blockquote
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append("<blockquote>%s</blockquote>" % md("\n".join(buf)))
            continue

        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)", ln)          # list
        if m:
            ordered = not m.group(2) in "-*+"
            tag = "ol" if ordered else "ul"
            items, base = [], len(m.group(1))
            while i < len(lines):
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)", lines[i])
                if mm and len(mm.group(1)) == base:
                    items.append([mm.group(3)]); i += 1
                elif items and lines[i].strip() and lines[i].startswith(" " * (base + 1)):
                    items[-1].append(lines[i].strip()); i += 1
                else:
                    break
            out.append("<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % inline(" ".join(it)) for it in items), tag))
            continue

        if not ln.strip():                                         # blank
            i += 1
            continue

        buf = []                                                   # paragraph
        while i < len(lines) and lines[i].strip() \
                and not re.match(r"^(#{1,6}\s|```|\s*\||\s*>)", lines[i]) \
                and not re.match(r"^(\s*)([-*+]|\d+[.)])\s+", lines[i]):
            buf.append(lines[i].strip()); i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "\n".join(out)
