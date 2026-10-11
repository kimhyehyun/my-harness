"""G2 — S2→S3 화면 설계 게이트.

입력: runs/{flow}/s2/screens.md (형식: harness/templates/screens.md)
  ## 화면: {이름}
  - 스토리: 3, 4
  - 상태: 미완료, 완료
  - 전이: {출발} → {도착} (트리거: {무엇})
  - 되돌리기: 체크 전부 지우기
"""
import re

from common import Report, load_rules, parse_args

ARROW = re.compile(r"전이:\s*(.+?)\s*(?:→|->)\s*(.+?)\s*\(트리거:\s*(.+?)\)")


def parse(text):
    screens, cur = [], None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"^##\s*화면:\s*(.+)$", line)
        if m:
            cur = {"name": m.group(1).strip(), "stories": [], "states": [], "transitions": [], "undo": []}
            screens.append(cur)
            continue
        if cur is None:
            continue
        if line.startswith("- 스토리:"):
            cur["stories"] = [int(x) for x in re.findall(r"\d+", line)]
        elif line.startswith("- 상태:"):
            cur["states"] = [x.strip() for x in line.split(":", 1)[1].split(",") if x.strip()]
        elif line.startswith("- 전이:"):
            t = ARROW.search(line)
            cur["transitions"].append(
                {"from": t.group(1), "to": t.group(2), "trigger": t.group(3)} if t else {"raw": line}
            )
        elif line.startswith("- 되돌리기:"):
            cur["undo"].append(line.split(":", 1)[1].strip())
    return screens


def main():
    args = parse_args(__doc__)
    rules = load_rules(args.rules)
    rep = Report("G2", args.run_dir)
    path = rep.run_dir / "s2" / "screens.md"
    if not path.exists():
        rep.add("G2-0", "s2/screens.md", "파일 없음", "있어야 함")
        rep.finish(args.out)
    text = path.read_text(encoding="utf-8")
    screens = parse(text)
    es = rules["exercise_status"]

    # G2-1 범위 밖 금지어
    rep.check("G2-1")
    for word in rules["out_of_scope"]:
        if word in text:
            rep.add("G2-1", "s2/screens.md", word, "out_of_scope 0개")

    # G2-2 모든 화면에 스토리, 플로우 스토리 포함
    rep.check("G2-2")
    if not screens:
        rep.add("G2-2", "s2/screens.md", "화면 0개", "## 화면: 1개 이상")
    for s in screens:
        if not s["stories"]:
            rep.add("G2-2", s["name"], "스토리 없음", "1개 이상")
    need = rules.get("flow_stories", {}).get(rep.flow)
    if need is None:
        rep.add("G2-2", rep.flow, "알 수 없는 플로우", rules["flows"])
    else:
        have = {i for s in screens for i in s["stories"]}
        for i in need:
            if i not in have:
                rep.add("G2-2", rep.flow, f"스토리 {i} 없음", need)

    # ★G2-3 운동 상태값
    rep.check("G2-3")
    for s in screens:
        for st in s["states"]:
            if st not in es["allowed"]:
                rep.add("G2-3", s["name"], st, es["allowed"])

    # ★G2-4 완료는 사용자 체크로만, 자동 완료 문구 0
    rep.check("G2-4")
    for s in screens:
        for t in s["transitions"]:
            if "raw" in t:
                rep.add("G2-4", s["name"], t["raw"], "전이: A → B (트리거: X)")
            elif t["to"] == "완료" and t["trigger"] != es["complete_trigger"]:
                rep.add("G2-4", s["name"], t["trigger"], es["complete_trigger"])
    for word in es["auto_complete_forbidden"]:
        if word in text:
            rep.add("G2-4", "s2/screens.md", word, "자동 완료 문구 0개")

    # ★G2-5 체크 되돌리기 수단 (완료 상태를 쓰는 설계일 때)
    rep.check("G2-5")
    uses_done = any("완료" in s["states"] for s in screens)
    if uses_done and not any(w in text for w in es["undo_required_any"]):
        rep.add("G2-5", "s2/screens.md", "되돌리기 없음", es["undo_required_any"])

    # ★G2-6 운동 완료 화면 진입은 마치기 버튼으로만
    rep.check("G2-6")
    for s in screens:
        for t in s["transitions"]:
            if t.get("to") == "운동 완료" and t.get("trigger") != es["finish_trigger"]:
                rep.add("G2-6", s["name"], t.get("trigger"), es["finish_trigger"])

    rep.finish(args.out)


if __name__ == "__main__":
    main()
