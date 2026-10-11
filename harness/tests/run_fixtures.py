"""판정 스크립트 검증 (harness/verification.md §1).

pass/: 모든 게이트를 통과하는 샘플 1세트
MUTATIONS: 게이트 ID마다 pass/ 사본에서 그 규칙 하나만 어기도록 바꾼 샘플
통과 조건: pass는 위반 0건, 각 fail 샘플은 그 게이트 ID만 걸림, 24개 ID 모두 걸림
사용: python3 harness/tests/run_fixtures.py
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PASS = ROOT / "harness" / "tests" / "fixtures" / "pass" / "finish-workout"
GATES = ["gate_s1.py", "gate_s2.py", "gate_s5.py"]
STAR = {"G2-3", "G2-4", "G2-5", "G2-6", "G5-10", "G5-11"}


def edit(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert old in t, (path, old)
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


def exp_edit(d, fn):
    p = d / "s4" / "export.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data["screens"][0]["nodes"]}
    fn(data, nodes, d)
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def m_g1_1(d): shutil.copy(d / "s1/refs/ref-1.png", d / "s1/refs/extra.png")
def m_g1_2(d): edit(d / "s1/refs/index.md", "https://uibowl.io/example/2", "")
def m_g1_3(d): edit(d / "s1/refs/index.md", "| 예시 앱 C | 운동 진행/체크 |", "| 예시 앱 C | 기타 |")
def m_g1_4(d): edit(d / "s1/points.md", "- P3: 마치기 전에 오늘 기록 요약 | refs: ref-3.png, ref-1.png | stories: 4\n", "")
def m_g1_5(d): edit(d / "s1/points.md", "refs: ref-2.png", "refs: missing.png")
def m_g1_6(d): edit(d / "s1/points.md", "stories: 3\n", "stories: 9\n")
def m_g2_1(d): edit(d / "s2/screens.md", "- 스토리: 4\n", "- 스토리: 4\n- 요소: 로그인 버튼\n")
def m_g2_2(d): edit(d / "s2/screens.md", "## 화면: 운동 완료\n- 스토리: 4\n", "## 화면: 운동 완료\n")
def m_g2_3(d): edit(d / "s2/screens.md", "- 상태: 미완료, 완료", "- 상태: 미완료, 완료, 보류")
def m_g2_4(d): edit(d / "s2/screens.md", "(트리거: 사용자 체크)", "(트리거: 타이머)")
def m_g2_5(d): edit(d / "s2/screens.md", "- 되돌리기: 체크 전부 지우기\n", "")
def m_g2_6(d): edit(d / "s2/screens.md", "- 스토리: 4\n", "- 스토리: 4\n- 전이: 기록 → 운동 완료 (트리거: 앱 실행)\n")
def m_g5_1(d): exp_edit(d, lambda x, n, _: n["1:5"]["fills"][0].pop("var"))
def m_g5_2(d): exp_edit(d, lambda x, n, _: n["1:5"].update(radius=[20]))
def m_g5_3(d): exp_edit(d, lambda x, n, _: n["1:5"].update(padding=[15, 16, 16, 16]))
def m_g5_4(d): exp_edit(d, lambda x, n, _: n["1:5"].update(effects=[{"type": "DROP_SHADOW", "visible": True}]))
def m_g5_5(d): exp_edit(d, lambda x, n, _: x["screens"][0]["nodes"].append(dict(n["1:7"], id="1:9")))
def m_g5_6(d): exp_edit(d, lambda x, n, _: n["1:4"].pop("textStyle"))
def m_g5_7(d): exp_edit(d, lambda x, n, _: n["1:3"].update(height=48))
def m_g5_8(d): exp_edit(d, lambda x, n, _: n["1:7"].update(height=40))
def m_g5_9(d): exp_edit(d, lambda x, n, _: x["screens"][0]["nodes"].append({"id": "1:10", "name": "Chip", "type": "FRAME"}))
def m_g5_10(d): exp_edit(d, lambda x, n, _: n["1:6"].update(name="thumbnail"))


def m_g5_11(d):
    h = hashlib.sha1((d / "s1/refs/ref-1.png").read_bytes()).hexdigest()
    exp_edit(d, lambda x, n, _: n["1:6"]["fills"][0].update(imageHash=h))


def m_g5_12(d): exp_edit(d, lambda x, n, _: n["1:8"].update(characters="문의 010-1234-5678"))


MUTATIONS = {k.replace("m_g", "G").replace("_", "-", 1).replace("_", "-"): v
             for k, v in dict(globals()).items() if k.startswith("m_g")}


def run(case_dir):
    ids, codes = set(), []
    for g in GATES:
        p = subprocess.run([sys.executable, str(ROOT / "harness" / "gates" / g), str(case_dir)],
                           capture_output=True, text=True)
        codes.append(p.returncode)
        ids |= {v["rule"] for v in json.loads(p.stdout)["violations"]}
    return ids, codes


def main():
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        ids, codes = run(PASS)
        print(f"pass: exit {codes} 위반 {sorted(ids) or 0}")
        ok &= not ids and codes == [0, 0, 0]
        hit = set()
        for gid, fn in sorted(MUTATIONS.items(), key=lambda kv: (kv[0][:2], int(kv[0].split("-")[1]))):
            case = Path(tmp) / gid / "finish-workout"
            shutil.copytree(PASS, case)
            fn(case)
            ids, codes = run(case)
            good = ids == {gid} and 1 in codes
            hit |= ids
            ok &= good
            print(f"{'✅' if good else '❌'} {gid}{' ★' if gid in STAR else ''}: 걸린 규칙 {sorted(ids)}")
    expected = {f"G1-{i}" for i in range(1, 7)} | {f"G2-{i}" for i in range(1, 7)} | {f"G5-{i}" for i in range(1, 13)}
    miss = expected - hit
    print(f"커버리지 {len(expected - miss)}/{len(expected)}, ★ 누락 {sorted(STAR - hit) or 0}")
    ok &= not miss
    print("결과:", "통과" if ok else "실패")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
