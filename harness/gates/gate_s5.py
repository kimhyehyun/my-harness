"""G5 — S5 디자인 게이트 (읽기 전용 판정).

입력: runs/{flow}/s4/export.json (harness/figma/export_s4.js 출력)
  {"screens": [{"id","name","width","height","nodes": [노드...]}]}
  노드: id, name, type, in_instance, fills[], strokes[], radius[], padding[], gap,
        effects[], textStyle, characters, component, variant, height
  paint: {"type","visible","var","imageHash"}
"""
import hashlib
import re

from common import Report, load_rules, parse_args


def paints(node):
    for key in ("fills", "strokes"):
        for p in node.get(key) or []:
            yield key, p


def main():
    args = parse_args(__doc__)
    rules = load_rules(args.rules)
    rep = Report("G5", args.run_dir)
    path = rep.run_dir / "s4" / "export.json"
    if not path.exists():
        rep.add("G5-0", "s4/export.json", "파일 없음", "있어야 함")
        rep.finish(args.out)
    import json

    data = json.loads(path.read_text(encoding="utf-8"))
    colors = set(rules["colors"]["variables"])
    radius_ok = set(rules["radius"]["allowed"])
    radius_exc = [k.split(" (")[0] for k in rules["radius"].get("known_exceptions", {})]
    spacing_ok = set(rules["spacing"]["allowed"])
    styles = set(rules["typography"]["styles"])
    comp_names = {c for c in rules["components"] if not c.endswith("*")}
    src_ids = {s["id"] for s in rules["exercise_sources"]["allowed"]}
    pii = {k: re.compile(v) for k, v in rules["pii_patterns"].items()}
    ref_hashes = set()
    refs = rep.run_dir / "s1" / "refs"
    if refs.exists():
        for f in refs.iterdir():
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
                ref_hashes.add(hashlib.sha1(f.read_bytes()).hexdigest())
    fr = rules["frame"]
    pmax = rules["colors"]["primary_button_max_per_screen"]
    for gid in ["G5-%d" % i for i in range(1, 13)]:
        rep.check(gid)

    for sc in data.get("screens", []):
        sname = sc["name"]
        # G5-7 프레임
        if sc["width"] != fr["width"] or sc["height"] < fr["min_height"]:
            rep.add("G5-7", sname, [sc["width"], sc["height"]], f"너비 {fr['width']}, 높이 ≥{fr['min_height']}")
        primaries = 0
        for n in sc["nodes"]:
            tgt = f"{sname} > {n['name']}"
            inside = n.get("in_instance", False)
            # G5-1 색 바인딩
            if not inside:
                for key, p in paints(n):
                    if p.get("visible") is False or p["type"] == "IMAGE":
                        continue
                    if p["type"] != "SOLID" or p.get("var") not in colors:
                        rep.add("G5-1", tgt, f"{key}:{p['type']}:{p.get('var')}", "color 변수 바인딩")
            # G5-2 radius
            if not inside and n.get("radius"):
                if not any(n["name"].startswith(e) for e in radius_exc):
                    for r in n["radius"]:
                        if round(r, 1) not in radius_ok:
                            rep.add("G5-2", tgt, r, sorted(radius_ok))
            # G5-3 간격
            if not inside and n["type"] == "FRAME":
                for v in (n.get("padding") or []) + ([n["gap"]] if n.get("gap") is not None else []):
                    if v not in spacing_ok:
                        rep.add("G5-3", tgt, v, sorted(spacing_ok))
            # G5-4 그림자
            if not inside:
                for e in n.get("effects") or []:
                    if e.get("type") == "DROP_SHADOW" and e.get("visible", True):
                        rep.add("G5-4", tgt, "DROP_SHADOW", "0개")
            # G5-5 Primary 버튼 개수
            if n["type"] == "INSTANCE" and n.get("component") == "Button" and "Style=Primary" in (n.get("variant") or ""):
                if n.get("visible", True):
                    primaries += 1
            # G5-6 텍스트 스타일
            if not inside and n["type"] == "TEXT" and n.get("textStyle") not in styles:
                rep.add("G5-6", tgt, n.get("textStyle"), "typography.styles")
            # G5-7 헤더 높이
            if not inside and n["name"] == "header" and n.get("height") != fr["header_height"]:
                rep.add("G5-7", tgt, n.get("height"), fr["header_height"])
            # G5-8 터치
            if n["type"] == "INSTANCE" and n.get("component") == "Button" and n.get("height", 0) < rules["touch"]["min_height"]:
                rep.add("G5-8", tgt, n.get("height"), f"≥{rules['touch']['min_height']}")
            # G5-9 컴포넌트는 인스턴스로만
            if not inside and n["type"] != "INSTANCE" and n["name"] in comp_names:
                rep.add("G5-9", tgt, n["type"], "INSTANCE")
            # ★G5-10 이미지 출처 / ★G5-11 레퍼런스 이미지 재사용
            for key, p in paints(n):
                if p["type"] != "IMAGE":
                    continue
                m = re.search(r"source=([\w-]+)", n["name"])
                if not m or m.group(1) not in src_ids:
                    rep.add("G5-10", tgt, m.group(1) if m else "출처 없음", sorted(src_ids))
                if p.get("imageHash") in ref_hashes:
                    rep.add("G5-11", tgt, p.get("imageHash"), "s1/refs 이미지 사용 0건")
            # G5-12 개인정보 패턴
            if n["type"] == "TEXT":
                for k, rx in pii.items():
                    if rx.search(n.get("characters") or ""):
                        rep.add("G5-12", tgt, k, "개인정보 패턴 0건")
        if primaries > pmax:
            rep.add("G5-5", sname, primaries, f"≤{pmax}")

    rep.finish(args.out)


if __name__ == "__main__":
    main()
