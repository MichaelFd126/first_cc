# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file desktop Pomodoro timer built with Python + Tkinter. No external dependencies, no build system, no test suite, no linter config.

## Running

```bash
python pomodoro.py     # or: py pomodoro.py
```

Requires a Tkinter-capable Python (CPython on Windows ships it). Note: Python is **not installed** on this machine — only the Microsoft Store stub is present, so the app cannot be launched or syntax-checked locally. Verify changes by reading, or install Python first.

## Architecture

Everything lives in `pomodoro.py` — a single `PomodoroApp` class instantiated inside `main()`.

- **Timing is event-loop based, not threaded.** The countdown runs on Tkinter's `root.after(1000, self._tick)` scheduler, not a background thread or `time.sleep`. A one-second tick decrements `self.remaining`; the next tick is re-armed only after `_tick` returns.
- **State** is a small set of instance fields: `mode` (`"work"` / `"break"`), `remaining` (seconds), `running` (bool), and `after_id` (handle to the pending `after` callback).
- **`after_id` bookkeeping is the one subtle bit.** `toggle`/`reset`/`_finish` must call `_cancel_tick()` to prevent a stale scheduled tick from firing after the timer is paused or switched. A new tick is scheduled in `toggle` (on start) and at the end of `_tick` (on continue).
- **Cycle:** `_tick` → `_finish` → `_beep` → swap mode + reset `remaining` to `WORK_SECONDS` / `BREAK_SECONDS`.
- **Sound is platform-specific:** `winsound.Beep` on Windows, falling back to a terminal bell (`print("\a")`) on other platforms via `ImportError`.

Duration constants (`WORK_SECONDS = 25 * 60`, `BREAK_SECONDS = 5 * 60`) and colors (`COLOR_WORK`, `COLOR_BREAK`, …) are module-level and are the natural place to adjust behavior.

## Repo conventions

- `.claude/settings.local.json` is gitignored — it holds this machine's local permission grants only.
- The remote is `git@github.com:MichaelFd126/first_cc.git` (SSH). Commit messages are written in Chinese; keep that convention.
