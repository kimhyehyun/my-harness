"""G1 — S1→S2 레퍼런스 게이트.

입력: runs/{flow}/s1/refs/*.png, s1/refs/index.md, s1/points.md
  index.md 표: | 파일 | 출처 URL | 앱 | 화면 유형 |
  points.md 줄: - P1: 반영 내용 | refs: a.png, b.png | stories: 1, 3
"""
import re
from collections import Counter

from common import Report, load_rules, md_table_rows, parse_args

POINT_RE = re.compile(r"^-\s*P\d+\s*:")


def main():
    args = parse_args(__doc__)
    rules = load_rules(args.rules)
    rep = Report("G1", args.run_dir)
    s1 = rep.run_dir / "s1"
    refs_dir = s1 / "refs"
    index = refs_dir / "index.md"
    points = s1 / "points.md"

    pngs = sorted(p.name for p in refs_dir.glob("*.png")) if refs_dir.exists() else []
    rows = md_table_rows(index.read_text(encoding="utf-8")) if index.exists() else []

    # G1-1 PNG 개수 = index.md 행 수
    rep.check("G1-1")
    if len(pngs) != len(rows):
        rep.add("G1-1", "s1/refs", f"png {len(pngs)} / index {len(rows)}", "같아야 함")

    # G1-2 출처 URL 누락 0
    rep.check("G1-2")
    for r in rows:
        url = r[1] if len(r) > 1 else ""
        if not url.startswith("http"):
            rep.add("G1-2", r[0] if r else "?", url or "(없음)", "http(s) URL")

    # G1-3 유형별 장수, 전체 장수
    rep.check("G1-3")
    lo, hi = rules["refs"]["per_type"]
    types = Counter(r[3] for r in rows if len(r) > 3)
    for t, n in types.items():
        if t not in rules["refs"]["types"]:
            rep.add("G1-3", t, "알 수 없는 유형", rules["refs"]["types"])
        elif not lo <= n <= hi:
            rep.add("G1-3", t, n, f"{lo}~{hi}장")
    if len(rows) > rules["refs"]["max_total"]:
        rep.add("G1-3", "전체", len(rows), f"≤{rules['refs']['max_total']}")

    # G1-4 ~ G1-6 반영 포인트
    lines = []
    if points.exists():
        lines = [l.strip() for l in points.read_text(encoding="utf-8").splitlines() if POINT_RE.match(l.strip())]
    rep.check("G1-4")
    pmin, pmax = rules["points"]["min"], rules["points"]["max"]
    if not pmin <= len(lines) <= pmax:
        rep.add("G1-4", "s1/points.md", len(lines), f"{pmin}~{pmax}개")

    rep.check("G1-5")
    rep.check("G1-6")
    for line in lines:
        pid = line.split(":")[0].lstrip("- ").strip()
        refs = re.search(r"refs:\s*([^|]+)", line)
        names = [x.strip() for x in refs.group(1).split(",") if x.strip()] if refs else []
        if not names:
            rep.add("G1-5", pid, "근거 레퍼런스 없음", "파일명 1개 이상")
        for n in names:
            if n not in pngs:
                rep.add("G1-5", pid, n, "s1/refs에 있는 파일")
        st = re.search(r"stories:\s*([0-9,\s]+)", line)
        ids = [int(x) for x in re.findall(r"\d+", st.group(1))] if st else []
        if not ids or any(i not in rules["points"]["story_ids"] for i in ids):
            rep.add("G1-6", pid, ids or "없음", rules["points"]["story_ids"])

    rep.finish(args.out)


if __name__ == "__main__":
    main()
