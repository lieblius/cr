"""Resume the most recent Claude Code session for the current git branch."""

import json
import os
import subprocess
import sys


def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def get_project_dir():
    cwd = os.getcwd()
    project_hash = cwd.replace("/", "-")
    return os.path.expanduser(f"~/.claude/projects/{project_hash}")


def find_sessions(project_dir, branch):
    matches = []
    for name in os.listdir(project_dir):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(project_dir, name)
        try:
            with open(path) as f:
                for line in f:
                    msg = json.loads(line)
                    if msg.get("type") == "system":
                        if msg.get("gitBranch") == branch:
                            mtime = os.path.getmtime(path)
                            session_id = name.removesuffix(".jsonl")
                            matches.append((mtime, session_id))
                        break
        except (json.JSONDecodeError, OSError):
            continue
    matches.sort(reverse=True)
    return matches


def main():
    branch = get_current_branch()
    if not branch:
        print("Not in a git repo or on a detached HEAD")
        sys.exit(1)

    project_dir = get_project_dir()
    if not os.path.isdir(project_dir):
        print("No Claude sessions for this project, starting new session")
        os.execvp("claude", ["claude"])

    sessions = find_sessions(project_dir, branch)

    if not sessions:
        print(f"No session found for branch '{branch}', starting new session")
        os.execvp("claude", ["claude"])

    _, session_id = sessions[0]
    print(f"Resuming session {session_id} (branch: {branch})")
    os.execvp("claude", ["claude", "--resume", session_id])
