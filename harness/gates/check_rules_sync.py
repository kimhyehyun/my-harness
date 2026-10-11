"""규칙 동기화 검사: docs/design.md(원본)와 harness/rules.json(사본)이 같은지 본다.

비교: color 변수 이름·hex, radius 변수, space 변수, 텍스트 스타일 이름·크기
사용: python3 harness/gates/check_rules_sync.py   (다르면 exit 1)
"""
import json
import re
import sys

from common import ROOT, load_rules

ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|")


def design_tables():
    text = (ROOT / "docs" / "design.md").read_text(encoding="utf-8")
    sections, cur = {}, None
    for line in text.splitlines():
        h = re.match(r"^#{2,3}\s+(.+)$", line)
        if h:
            cur = h.group(1).strip()
            continue
        m = ROW.match(line.strip())
        if m and cur:
            sections.setdefault(cur, {})[m.group(1)] = m.group(2).strip()
    return sections


def num(v):
    m = re.search(r"-?\d+(?:\.\d+)?", v)
    return float(m.group()) if m else None


def main():
    rules = load_rules()
    sec = design_tables()
    diffs = []

    # 색: hex 6자리 행만 비교 (alpha 행은 이름만)
    doc_colors = {}
    for name in ("Surface", "Text", "Accent", "Alpha"):
        doc_colors.update(sec.get(name, {}))
    rc = rules["colors"]["variables"]
    for name, val in doc_colors.items():
        if name not in rc:
            diffs.append(("color", name, "design.md에만 있음"))
        elif re.fullmatch(r"#[0-9A-Fa-f]{6}", val) and rc[name].upper() != val.upper():
            diffs.append(("color", name, f"design {val} / rules {rc[name]}"))
    for name in rc:
        if name not in doc_colors and not name.startswith("alpha/pt-"):
            diffs.append(("color", name, "rules.json에만 있음"))

    # radius
    doc_r = {k: num(v) for k, v in sec.get("Shapes", {}).items()}
    for k, v in rules["radius"]["variables"].items():
        if doc_r.get(k) != float(v):
            diffs.append(("radius", k, f"design {doc_r.get(k)} / rules {v}"))

    # space
    doc_s = {k: num(v) for k, v in sec.get("Spacing", {}).items()}
    for k, v in rules["spacing"]["variables"].items():
        if doc_s.get(k) != float(v):
            diffs.append(("space", k, f"design {doc_s.get(k)} / rules {v}"))

    # 텍스트 스타일
    doc_t = {k: num(v) for k, v in sec.get("Typography", {}).items()}
    rt = rules["typography"]["styles"]
    for k, v in rt.items():
        if doc_t.get(k) != float(v):
            diffs.append(("typography", k, f"design {doc_t.get(k)} / rules {v}"))
    for k in doc_t:
        if k not in rt:
            diffs.append(("typography", k, "design.md에만 있음"))

    out = {"result": "pass" if not diffs else "fail", "count": len(diffs),
           "diffs": [{"kind": a, "name": b, "detail": c} for a, b, c in diffs]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if diffs:
        print("design.md 변경됨, rules.json 갱신 필요", file=sys.stderr)
    sys.exit(0 if not diffs else 1)


if __name__ == "__main__":
    main()
