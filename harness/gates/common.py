"""게이트 스크립트 공통 도구. 판정 스크립트는 읽기만 한다 (--out 리포트 파일 하나만 예외)."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_rules(path=None):
    p = Path(path) if path else ROOT / "harness" / "rules.json"
    return json.loads(p.read_text(encoding="utf-8"))


def parse_args(desc):
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("run_dir", help="runs/{flow} 폴더")
    ap.add_argument("--rules", help="rules.json 경로 (기본: harness/rules.json)")
    ap.add_argument("--out", help="리포트를 이 파일에 JSON으로 저장 (judge 전용)")
    return ap.parse_args()


class Report:
    def __init__(self, gate, run_dir):
        self.gate = gate
        self.run_dir = Path(run_dir)
        self.flow = self.run_dir.name
        self.violations = []
        self.checked = set()

    def check(self, rule_id):
        self.checked.add(rule_id)

    def add(self, rule, target, actual, allowed):
        self.checked.add(rule)
        self.violations.append(
            {"rule": rule, "target": target, "actual": actual, "allowed": allowed}
        )

    def finish(self, out=None):
        data = {
            "gate": self.gate,
            "flow": self.flow,
            "checked": sorted(self.checked),
            "count": len(self.violations),
            "violations": self.violations,
            "result": "pass" if not self.violations else "fail",
        }
        text = json.dumps(data, ensure_ascii=False, indent=2)
        print(text)
        if out:
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            Path(out).write_text(text + "\n", encoding="utf-8")
        sys.exit(0 if not self.violations else 1)


def md_table_rows(text):
    """마크다운 표에서 헤더·구분선을 뺀 행을 셀 리스트로 돌려준다."""
    rows = []
    lines = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip("|").split("|")]
        if i == 0:
            continue  # 헤더
        if all(set(c) <= set("-: ") for c in cells):
            continue  # 구분선
        rows.append(cells)
    return rows
