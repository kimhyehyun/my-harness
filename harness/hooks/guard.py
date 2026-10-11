"""PreToolUse 훅: 에이전트별 편집 폴더를 강제한다 (harness/roles.md).

stdin: Claude Code 훅 입력 JSON (tool_name, tool_input, agent_type, cwd ...)
차단: stdout에 permissionDecision "deny" JSON을 쓰고 exit 0
허용: 아무것도 쓰지 않고 exit 0

규칙
- 모두: runs/*/human/approval.md 쓰기 금지 (사람만 쓴다)
- 하네스 서브에이전트: harness/, docs/, .claude/ 쓰기 금지, 자기 폴더(runs/{flow}/sN/)만 쓰기 가능
- judge: Write/Edit 금지, Bash는 `python3 harness/gates/gate_*.py ...`만
- ref-researcher: Bash는 s1/refs 안으로 받는 `curl -o`만
- 그 밖의 서브에이전트: Bash 금지
- 메인 세션(오케스트레이터): runs/*/s1~s5 산출물 쓰기 금지. 그 외(state.json, retro.md, 하네스 유지보수)는 허용
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

AGENT_DIR = {
    "ref-researcher": "s1",
    "screen-planner": "s2",
    "keyscreen-designer": "s3",
    "ui-designer": "s4",
    "judge": "s5",
}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"[harness guard] {reason}"}}, ensure_ascii=False))
    sys.exit(0)


def rel(path, root):
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    try:
        return p.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None  # 프로젝트 밖


def main():
    data = json.load(sys.stdin)
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    agent = data.get("agent_type")
    harness_agent = agent in AGENT_DIR

    if tool in WRITE_TOOLS:
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        r = rel(path, root)
        if r and re.fullmatch(r"runs/[^/]+/human/approval\.md", r):
            deny("human/approval.md는 사람만 작성합니다.")
        if harness_agent:
            if agent == "judge":
                deny("judge는 파일을 직접 쓰지 않습니다. gate_s5.py --out으로만 리포트를 저장합니다.")
            if r is None or not re.fullmatch(rf"runs/[^/]+/{AGENT_DIR[agent]}/.+", r):
                deny(f"{agent}는 runs/{{flow}}/{AGENT_DIR[agent]}/ 안에만 쓸 수 있습니다: {path}")
        elif agent is None and r and re.fullmatch(r"runs/[^/]+/s[1-5]/.+", r):
            deny("오케스트레이터는 s1~s5 산출물을 직접 쓰지 않습니다. 담당 에이전트를 호출하세요.")
        sys.exit(0)

    if tool == "Bash" and harness_agent:
        cmd = ti.get("command", "").strip()
        if re.search(r"[;&|`$<>]|\n", cmd.replace("2>&1", "")):
            deny("하네스 에이전트의 Bash는 명령 하나만 허용합니다 (연결·리다이렉트 금지).")
        try:
            args = shlex.split(cmd)
        except ValueError:
            deny("명령을 해석할 수 없습니다.")
        if agent == "judge":
            ok = (len(args) >= 3 and args[0] in ("python3", "python")
                  and re.fullmatch(r"(?:\./)?harness/gates/(gate_s[125]|check_rules_sync)\.py", args[1] or ""))
            if not ok:
                deny("judge는 python3 harness/gates/gate_*.py만 실행할 수 있습니다.")
            if "--out" in args:
                i = args.index("--out")
                r = rel(args[i + 1], root) if i + 1 < len(args) else None
                if not r or not re.fullmatch(r"runs/[^/]+/s5/report\.json", r):
                    deny("judge의 --out은 runs/{flow}/s5/report.json만 허용합니다.")
            sys.exit(0)
        if agent == "ref-researcher":
            if not args or args[0] != "curl":
                deny("ref-researcher의 Bash는 curl 다운로드만 허용합니다.")
            outs = [args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-o", "--output")]
            if not outs or any(not re.fullmatch(r"runs/[^/]+/s1/refs/[^/]+\.(png|jpg|jpeg|webp)", rel(o, root) or "") for o in outs):
                deny("curl -o 대상은 runs/{flow}/s1/refs/ 안의 이미지 파일이어야 합니다.")
            sys.exit(0)
        deny(f"{agent}는 Bash를 쓸 수 없습니다.")

    sys.exit(0)


if __name__ == "__main__":
    main()
