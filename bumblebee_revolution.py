#!/usr/bin/env python3
"""Bumblebee → shapes + sounds → spark revolution → JUSTICE."""

import math
import random
import sys
import tkinter as tk

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# --- palette ---
BG = "#0a0612"
GOLD = "#ffd54f"
AMBER = "#ff8f00"
TEXT = "#f5e6c8"
MUTED = "#8a7f6a"

NOTES = [262, 330, 392, 523, 659]
THRESHOLD = 12
JUSTICE_TARGET = 8


def beep(freq: int, ms: int = 120) -> None:
    if HAS_WINSOUND:
        winsound.Beep(freq, ms)
    else:
        print(f"\a {freq}Hz", end="", flush=True)


def buzz_sound() -> None:
    for f in (90, 110, 95, 120, 100, 130, 105, 140):
        beep(f, 40)


def fanfare() -> None:
    for f in (262, 330, 392, 523, 659, 784):
        beep(f, 160)


def justice_chime() -> None:
    for f in (392, 523, 659, 784, 988):
        beep(f, 200)


class Spark:
    __slots__ = ("x", "y", "dx", "dy", "life", "color")

    def __init__(self, x: float, y: float, color: str = GOLD) -> None:
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 7)
        self.x = x
        self.y = y
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.life = random.randint(18, 32)
        self.color = color


class BumblebeeRevolution:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bumblebee Revolution — Python Edition")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.w = 520
        self.h = 620
        self.cx = self.w // 2
        self.cy = 250

        self.charge = 0
        self.phase = "revolution"  # revolution | ignited | justice | served
        self.angle = 0.0
        self.bee_bounce = 0.0
        self.sparks: list[Spark] = []
        self.justice_left = 0
        self.justice_right = 0
        self.flash = 0

        self._build_ui()
        self._tick()

    def _build_ui(self) -> None:
        self.title = tk.Label(
            self.root, text="BUMBLEBEE", font=("Segoe UI", 22, "bold"),
            fg=GOLD, bg=BG,
        )
        self.title.pack(pady=(18, 0))

        self.subtitle = tk.Label(
            self.root, text="shapes + sounds → spark revolution → JUSTICE",
            font=("Segoe UI", 9), fg=MUTED, bg=BG,
        )
        self.subtitle.pack(pady=(4, 10))

        self.canvas = tk.Canvas(
            self.root, width=self.w, height=420, bg=BG, highlightthickness=0,
        )
        self.canvas.pack()

        self.meter_label = tk.Label(
            self.root, text="REVOLUTION CHARGE", font=("Segoe UI", 8),
            fg=MUTED, bg=BG,
        )
        self.meter_label.pack(pady=(8, 4))

        self.meter_bg = tk.Canvas(self.root, width=360, height=10, bg=BG, highlightthickness=0)
        self.meter_bg.pack()
        self.meter_fill = self.meter_bg.create_rectangle(
            0, 0, 0, 10, fill=AMBER, outline="",
        )

        self.status = tk.Label(
            self.root, text="click shapes · buzz the bee · speak python",
            font=("Segoe UI", 9), fg=TEXT, bg=BG,
        )
        self.status.pack(pady=(8, 16))

        self.shapes = [
            {"name": "circle",  "r": 36, "color": "#ff6b6b", "note": 0},
            {"name": "square",  "r": 36, "color": "#4ecdc4", "note": 1},
            {"name": "triangle","r": 36, "color": "#a78bfa", "note": 2},
            {"name": "hexagon", "r": 36, "color": "#ffd54f", "note": 3},
            {"name": "diamond", "r": 36, "color": "#f472b6", "note": 4},
        ]
        self.orbit_r = 190

        self.canvas.bind("<Button-1>", self._on_click)

    def _shape_pos(self, i: int) -> tuple[float, float]:
        a = self.angle + i * math.tau / len(self.shapes)
        return self.cx + math.cos(a) * self.orbit_r, self.cy + math.sin(a) * self.orbit_r

    def _hit_shape(self, x: float, y: float) -> int | None:
        for i in range(len(self.shapes)):
            sx, sy = self._shape_pos(i)
            if math.hypot(x - sx, y - sy) <= self.shapes[i]["r"]:
                return i
        return None

    def _hit_bee(self, x: float, y: float) -> bool:
        return math.hypot(x - self.cx, y - self.cy) <= 55

    def _spawn_sparks(self, x: float, y: float, n: int = 12, color: str = GOLD) -> None:
        self.sparks.extend(Spark(x, y, color) for _ in range(n))

    def _on_click(self, event: tk.Event) -> None:
        x, y = event.x, event.y

        if self.phase == "justice":
            self._justice_click(x, y)
            return

        if self._hit_bee(x, y):
            buzz_sound()
            self.bee_bounce = 1.0
            self._add_charge(2, x, y)
            return

        idx = self._hit_shape(x, y)
        if idx is not None:
            beep(NOTES[idx], 140)
            beep(NOTES[idx] // 2, 60)
            self._add_charge(1, x, y)

    def _add_charge(self, amount: int, x: float, y: float) -> None:
        if self.phase != "revolution":
            return
        self.charge = min(self.charge + amount, THRESHOLD + 3)
        pct = min(100, int(self.charge / THRESHOLD * 100))
        self.meter_bg.coords(self.meter_fill, 0, 0, 360 * pct / 100, 10)
        self.status.config(text=f"charge: {pct}% — keep going")
        self._spawn_sparks(x, y, 14 if amount > 1 else 8)
        if self.charge >= THRESHOLD:
            self._ignite()

    def _ignite(self) -> None:
        self.phase = "ignited"
        self.title.config(text="REVOLUTION SPARKED", fg=AMBER)
        self.status.config(text="now balance the scales. tap left & right.")
        self.meter_label.config(text="JUSTICE BALANCE")
        self.meter_bg.coords(self.meter_fill, 0, 0, 0, 10)
        self.flash = 12
        fanfare()
        self._spawn_sparks(self.cx, self.cy, 40)
        self.root.after(900, self._enter_justice)

    def _enter_justice(self) -> None:
        self.phase = "justice"
        self.title.config(text="JUSTICE", fg="#c8e6ff")
        self.justice_left = 0
        self.justice_right = 0
        self.status.config(text="tap LEFT shapes vs RIGHT shapes — balance wins")

    def _justice_click(self, x: float, y: float) -> None:
        if self._hit_bee(x, y):
            buzz_sound()
            self.bee_bounce = 1.0
            return

        idx = self._hit_shape(x, y)
        if idx is None:
            return

        sx, _ = self._shape_pos(idx)
        beep(NOTES[idx], 120)

        if sx < self.cx:
            self.justice_left += 1
        else:
            self.justice_right += 1

        diff = abs(self.justice_left - self.justice_right)
        balance = max(0, 100 - diff * 12)
        self.meter_bg.coords(self.meter_fill, 0, 0, 360 * balance / 100, 10)
        self.status.config(
            text=f"left: {self.justice_left}  ·  right: {self.justice_right}  ·  balance: {balance}%",
        )
        self._spawn_sparks(sx, self._shape_pos(idx)[1], 10, "#c8e6ff")

        if self.justice_left >= JUSTICE_TARGET and self.justice_right >= JUSTICE_TARGET:
            if diff <= 2:
                self._serve_justice()

    def _serve_justice(self) -> None:
        self.phase = "served"
        self.title.config(text="JUSTICE SERVED", fg=GOLD)
        self.status.config(text="bumblebee spoke python. w0rld balanced. ⚖")
        self.meter_bg.coords(self.meter_fill, 0, 0, 360, 10)
        self.flash = 20
        justice_chime()
        self._spawn_sparks(self.cx, self.cy, 50, GOLD)

    def _draw_hexagon(self, x: float, y: float, r: float, color: str) -> None:
        pts = []
        for k in range(6):
            a = math.pi / 6 + k * math.tau / 6
            pts.extend([x + math.cos(a) * r, y + math.sin(a) * r])
        self.canvas.create_polygon(*pts, fill=color, outline="", tags="scene")

    def _draw_scene(self) -> None:
        self.canvas.delete("scene")

        if self.flash > 0:
            alpha = self.flash / 20
            glow = f"#{int(255 * alpha):02x}{int(180 * alpha):02x}{int(40 * alpha):02x}"
            self.canvas.create_oval(
                self.cx - 200, self.cy - 200, self.cx + 200, self.cy + 200,
                fill=glow, outline="", tags="scene",
            )
            self.flash -= 1

        for i, shape in enumerate(self.shapes):
            x, y = self._shape_pos(i)
            r = shape["r"]
            c = shape["color"]
            if shape["name"] == "circle":
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline="", tags="scene")
            elif shape["name"] == "square":
                self.canvas.create_rectangle(x - r, y - r, x + r, y + r, fill=c, outline="", tags="scene")
            elif shape["name"] == "triangle":
                self.canvas.create_polygon(
                    x, y - r, x - r, y + r * 0.7, x + r, y + r * 0.7,
                    fill=c, outline="", tags="scene",
                )
            elif shape["name"] == "hexagon":
                self._draw_hexagon(x, y, r, c)
            elif shape["name"] == "diamond":
                self.canvas.create_polygon(
                    x, y - r, x + r, y, x, y + r, x - r, y,
                    fill=c, outline="", tags="scene",
                )

        if self.phase in ("justice", "served"):
            self.canvas.create_line(self.cx, self.cy - 80, self.cx, self.cy + 60, fill="#c8e6ff", width=3, tags="scene")
            self.canvas.create_line(self.cx - 70, self.cy - 40, self.cx + 70, self.cy - 40, fill="#c8e6ff", width=3, tags="scene")
            tilt = (self.justice_right - self.justice_left) * 4
            self.canvas.create_line(self.cx - 50, self.cy - 40 + tilt, self.cx - 50, self.cy - 10, fill="#c8e6ff", width=2, tags="scene")
            self.canvas.create_line(self.cx + 50, self.cy - 40 - tilt, self.cx + 50, self.cy - 10, fill="#c8e6ff", width=2, tags="scene")
            self.canvas.create_oval(self.cx - 58, self.cy - 18 + tilt, self.cx - 42, self.cy - 2 + tilt, fill=GOLD, outline="", tags="scene")
            self.canvas.create_oval(self.cx + 42, self.cy - 18 - tilt, self.cx + 58, self.cy - 2 - tilt, fill=GOLD, outline="", tags="scene")

        bounce = math.sin(self.bee_bounce * math.pi) * 8 if self.bee_bounce > 0 else math.sin(self.angle * 3) * 4
        by = self.cy + bounce
        bw, bh = 56, 44

        self.canvas.create_oval(self.cx - bw, by - bh, self.cx + bw, by + bh, fill=GOLD, outline="#1a1a1a", width=3, tags="scene")
        for stripe_y in (-12, 0, 12):
            self.canvas.create_line(self.cx - bw + 6, by + stripe_y, self.cx + bw - 6, by + stripe_y, fill="#1a1a1a", width=3, tags="scene")
        self.canvas.create_oval(self.cx + 30, by - 28, self.cx + 50, by - 8, fill="#1a1a1a", outline="", tags="scene")
        self.canvas.create_oval(self.cx + 36, by - 24, self.cx + 40, by - 20, fill="#fff", outline="", tags="scene")
        self.canvas.create_oval(self.cx - 38, by - 50, self.cx - 10, by - 30, fill="#b0c8e8", outline="", tags="scene")
        self.canvas.create_oval(self.cx + 10, by - 50, self.cx + 38, by - 30, fill="#b0c8e8", outline="", tags="scene")

        alive = []
        for sp in self.sparks:
            sp.x += sp.dx
            sp.y += sp.dy
            sp.life -= 1
            if sp.life > 0:
                r = max(1, sp.life // 6)
                self.canvas.create_oval(sp.x - r, sp.y - r, sp.x + r, sp.y + r, fill=sp.color, outline="", tags="scene")
                alive.append(sp)
        self.sparks = alive

    def _tick(self) -> None:
        self.angle += 0.012
        if self.bee_bounce > 0:
            self.bee_bounce = max(0, self.bee_bounce - 0.08)
        self._draw_scene()
        self.root.after(33, self._tick)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    print("🐝 bumblebee_revolution.py — close the window to quit")
    BumblebeeRevolution().run()


if __name__ == "__main__":
    main()