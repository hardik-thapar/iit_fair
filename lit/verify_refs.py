"""Merge the per-area .bib files and check each entry's title against arXiv / Crossref.

Usage: python lit/verify_refs.py
Writes paper/refs.bib and lit/ref_check.csv.
"""
import csv
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ["refs_decisions.bib", "refs_india.bib", "refs_faithfulness.bib", "refs_added.bib"]

# Keys dropped from the merged output (duplicates of another key).
DROP = {"phutane2025ableist"}  # superseded by phutane2026ableist (AIES 2026 version)

# Manual verification overrides: applied after the automatic check, so re-runs are reproducible.
# Each value overrides status/score/source (and remote_title if given) for that key.
MANUAL = {
    "bertrand2004emily": {"status": "ok", "score": "manual", "source": "doi:10.1257/0002828042002561 (manual)"},
    "wang2024large": {"status": "ok", "score": "manual", "source": "doi:10.18653/v1/2024.acl-long.511 (manual)"},
    "kusner2017counterfactual": {"status": "ok", "score": "manual", "source": "papers.nips.cc page title (manual)"},
    "bowen2025measuring": {"status": "ok", "score": "manual", "source": "ideas.repec.org page title (manual)"},
    "zaveri2025caste": {"status": "partial", "score": "manual",
                        "source": "OpenAlex title+authors match; IIMB PDF 403 on recheck, method details unconfirmed"},
}


def split_entries(text):
    """Split a .bib file into (key, raw_entry) pairs."""
    parts = re.split(r"(?m)^(?=@)", text)
    out = []
    for p in parts:
        m = re.match(r"@\w+\{([^,]+),", p.strip())
        if m:
            out.append((m.group(1).strip(), p.strip()))
    return out


def field(entry, name):
    m = re.search(rf"(?im)^\s*{name}\s*=\s*[{{\"](.+?)[}}\"]\s*,?\s*$", entry)
    return m.group(1) if m else ""


def norm(s):
    s = re.sub(r"[{}\\]", "", s).lower()
    return re.sub(r"[^a-z0-9 ]", " ", s).split()


def get(url, tries=5):
    req = urllib.request.Request(url, headers={"User-Agent": "fairaudit-refcheck/0.1"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:  # back off on rate limiting, otherwise fail
            if e.code != 429 or i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def remote_title(entry):
    blob = entry
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", blob) or re.search(r"(?im)eprint\s*=\s*[{\"](\d{4}\.\d{4,5})", blob)
    if m:
        xml = get(f"http://export.arxiv.org/api/query?id_list={m.group(1)}")
        t = re.findall(r"<title>(.*?)</title>", xml, re.S)
        if len(t) > 1:
            return "arxiv:" + m.group(1), " ".join(t[1].split())
    doi = field(entry, "doi")
    if not doi:
        m = re.search(r"doi\.org/(10\.[^\s},]+)", blob)
        doi = m.group(1) if m else ""
    if doi:
        d = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))
        return "doi:" + doi, " ".join(d["message"]["title"][0].split())
    m = re.search(r"aclanthology\.org/([\w.\-]+?)/?[}\s,]", blob)
    if m:
        html = get(f"https://aclanthology.org/{m.group(1)}/")
        t = re.search(r"<title>(.*?)</title>", html, re.S)
        if t:
            return "acl:" + m.group(1), " ".join(t.group(1).replace(" - ACL Anthology", "").split())
    return "", ""


def main():
    merged = {}
    for name in SOURCES:
        for key, raw in split_entries((ROOT / "lit" / name).read_text()):
            # keep the longer (more complete) version of a duplicated key
            if key not in merged or len(raw) > len(merged[key]):
                merged[key] = raw
    for key in DROP:
        merged.pop(key, None)
    rows = []
    for key, raw in sorted(merged.items()):
        title = field(raw, "title")
        try:
            src, rt = remote_title(raw)
        except Exception as e:  # network or parse failure: flag, don't guess
            src, rt = "error", str(e)[:80]
        score = difflib.SequenceMatcher(None, " ".join(norm(title)), " ".join(norm(rt))).ratio() if rt else 0.0
        status = "ok" if score >= 0.9 else ("check" if rt else "no_id")
        row = {"key": key, "status": status, "score": round(score, 2), "source": src,
               "bib_title": title, "remote_title": rt}
        if key in MANUAL:  # manual check takes precedence
            row.update(MANUAL[key])
            status = row["status"]
        rows.append(row)
        print(f"{status:6} {score:.2f} {key}", file=sys.stderr)
        time.sleep(1)
    with open(ROOT / "lit" / "ref_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    header = "% Merged from lit/refs_*.bib by lit/verify_refs.py. Check status in lit/ref_check.csv.\n\n"
    (ROOT / "paper" / "refs.bib").write_text(header + "\n\n".join(merged[k] for k in sorted(merged)) + "\n")


if __name__ == "__main__":
    main()
