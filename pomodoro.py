# -*- coding: utf-8 -*-
"""番茄钟（基础版）—— Python + Tkinter，零外部依赖。

功能：
- 25 分钟工作 / 5 分钟休息循环
- 开始 / 暂停 / 重置
- 每段结束时响铃提醒
"""

import tkinter as tk
import tkinter.font as tkfont

# 时长配置（秒）
WORK_SECONDS = 25 * 60
BREAK_SECONDS = 5 * 60

# 配色
COLOR_WORK = "#e74c3c"    # 工作时红色
COLOR_BREAK = "#2ecc71"  # 休息时绿色
COLOR_BG = "#f7f7f7"
COLOR_TEXT = "#2c3e50"


class PomodoroApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("番茄钟")
        self.root.geometry("360x300")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.mode = "work"          # 当前模式：work / break
        self.remaining = WORK_SECONDS
        self.running = False        # 计时是否在跑
        self.after_id = None        # 挂起的 after 任务 id

        self._build_ui()
        self._render()

    # ---------- 界面 ----------
    def _build_ui(self) -> None:
        self.mode_label = tk.Label(
            self.root, text="", font=("Microsoft YaHei", 16, "bold"),
            bg=COLOR_BG, fg=COLOR_TEXT,
        )
        self.mode_label.pack(pady=(28, 4))

        # 用等宽字体避免数字跳动
        clock_font = tkfont.Font(family="Consolas", size=56, weight="bold")
        self.clock_label = tk.Label(
            self.root, text="", font=clock_font,
            bg=COLOR_BG, fg=COLOR_TEXT,
        )
        self.clock_label.pack(pady=(0, 24))

        btn_row = tk.Frame(self.root, bg=COLOR_BG)
        btn_row.pack()

        self.start_btn = tk.Button(
            btn_row, text="开始", width=8, command=self.toggle,
            font=("Microsoft YaHei", 11),
        )
        self.start_btn.grid(row=0, column=0, padx=6)

        self.reset_btn = tk.Button(
            btn_row, text="重置", width=8, command=self.reset,
            font=("Microsoft YaHei", 11),
        )
        self.reset_btn.grid(row=0, column=1, padx=6)

    # ---------- 状态与显示 ----------
    def _render(self) -> None:
        mode_text = "工作中" if self.mode == "work" else "休息中"
        self.mode_label.config(text=mode_text)

        color = COLOR_WORK if self.mode == "work" else COLOR_BREAK
        self.clock_label.config(fg=color)
        self.mode_label.config(fg=color)

        m, s = divmod(self.remaining, 60)
        self.clock_label.config(text=f"{m:02d}:{s:02d}")

        self.start_btn.config(text="暂停" if self.running else "开始")

    def _tick(self) -> None:
        """每秒回调，推进倒计时。"""
        if not self.running:
            return
        self.remaining -= 1
        if self.remaining <= 0:
            self._finish()
        else:
            self._render()
            self.after_id = self.root.after(1000, self._tick)

    def _finish(self) -> None:
        """一段结束：响铃并切换到另一模式。"""
        self.running = False
        self.after_id = None  # 当前 tick 已结束，无待取消的回调
        self._beep()

        if self.mode == "work":
            self.mode = "break"
            self.remaining = BREAK_SECONDS
        else:
            self.mode = "work"
            self.remaining = WORK_SECONDS

        self._render()

    # ---------- 操作 ----------
    def _cancel_tick(self) -> None:
        """取消挂起的计时回调（若有）。"""
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def toggle(self) -> None:
        """开始 / 暂停。"""
        self.running = not self.running
        if self.running:
            self.after_id = self.root.after(1000, self._tick)
        else:
            self._cancel_tick()
        self._render()

    def reset(self) -> None:
        """回到当前模式的初始时长。"""
        self.running = False
        self._cancel_tick()
        self.remaining = WORK_SECONDS if self.mode == "work" else BREAK_SECONDS
        self._render()

    # ---------- 声音 ----------
    @staticmethod
    def _beep() -> None:
        """结束提示音：Windows 用 winsound，其余平台退化为终端响铃。"""
        try:
            import winsound

            for freq, dur in ((880, 200), (1175, 300)):
                winsound.Beep(freq, dur)
        except ImportError:
            print("\a", end="", flush=True)


def main() -> None:
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
