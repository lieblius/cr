# cr

Resume the most recent Claude Code session for the current git branch.

When you run `cr` in a git repo, it finds the last Claude Code session associated with your current branch and resumes it. If no session exists for the branch, it starts a new one.

## Install

```
pip install git+https://github.com/lieblius/cr.git
```

## Usage

```
cr
```

That's it. Run it from any git repo where you've used Claude Code before.
