"""훅(harness/hooks/guard.py) 검증: 허용/차단 케이스를 실제로 넣어 본다.
사용: python3 harness/tests/test_guard.py
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "harness" / "hooks" / "guard.py"

CASES = [
    # (설명, agent_type, tool, tool_input, 기대: allow/deny)
    ("사람 승인 파일은 누구도 못 씀", None, "Write", {"file_path": "runs/finish-workout/human/approval.md"}, "deny"),
    ("오케스트레이터 state.json 허용", None, "Write", {"file_path": "runs/finish-workout/state.json"}, "allow"),
    ("오케스트레이터 산출물 직접 작성 금지", None, "Write", {"file_path": "runs/finish-workout/s2/screens.md"}, "deny"),
    ("오케스트레이터 하네스 유지보수 허용", None, "Edit", {"file_path": "harness/gates.md"}, "allow"),
    ("screen-planner 자기 폴더 허용", "screen-planner", "Write", {"file_path": "runs/finish-workout/s2/screens.md"}, "allow"),
    ("screen-planner 다른 스테이지 금지", "screen-planner", "Write", {"file_path": "runs/finish-workout/s4/export.json"}, "deny"),
    ("에이전트 harness/ 쓰기 금지", "ui-designer", "Edit", {"file_path": "harness/rules.json"}, "deny"),
    ("에이전트 docs/ 쓰기 금지", "ref-researcher", "Write", {"file_path": "docs/prd.md"}, "deny"),
    ("에이전트 프로젝트 밖 쓰기 금지", "ui-designer", "Write", {"file_path": "/tmp/x.json"}, "deny"),
    ("ui-designer s4 허용", "ui-designer", "Write", {"file_path": "runs/finish-workout/s4/export.json"}, "allow"),
    ("judge Write 금지", "judge", "Write", {"file_path": "runs/finish-workout/s5/report.json"}, "deny"),
    ("judge 게이트 실행 허용", "judge", "Bash", {"command": "python3 harness/gates/gate_s5.py runs/finish-workout --out runs/finish-workout/s5/report.json"}, "allow"),
    ("judge --out 경로 제한", "judge", "Bash", {"command": "python3 harness/gates/gate_s5.py runs/finish-workout --out harness/rules.json"}, "deny"),
    ("judge 다른 명령 금지", "judge", "Bash", {"command": "rm -rf runs"}, "deny"),
    ("judge 명령 연결 금지", "judge", "Bash", {"command": "python3 harness/gates/gate_s5.py runs/x; rm -rf runs"}, "deny"),
    ("ref-researcher curl 허용", "ref-researcher", "Bash", {"command": "curl -sL -o runs/finish-workout/s1/refs/ref-1.png https://example.com/a.png"}, "allow"),
    ("ref-researcher curl 다른 곳 금지", "ref-researcher", "Bash", {"command": "curl -sL -o docs/a.png https://example.com/a.png"}, "deny"),
    ("screen-planner Bash 금지", "screen-planner", "Bash", {"command": "ls"}, "deny"),
    ("관계없는 에이전트는 통과", "Explore", "Write", {"file_path": "runs/finish-workout/s2/x.md"}, "allow"),
]


def run(agent, tool, ti):
    payload = {"tool_name": tool, "tool_input": ti, "cwd": str(ROOT), "hook_event_name": "PreToolUse"}
    if agent:
        payload["agent_type"] = agent
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(ROOT))
    p = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True, env=env)
    if p.returncode != 0:
        return f"error({p.returncode}) {p.stderr.strip()}"
    if p.stdout.strip():
        return json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"]
    return "allow"


def main():
    ok = True
    for desc, agent, tool, ti, want in CASES:
        got = run(agent, tool, ti)
        good = got == want
        ok &= good
        print(f"{'✅' if good else '❌'} {desc}: {got}")
    print("결과:", "통과" if ok else "실패", f"({len(CASES)}건)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
