"""
Mode = most frequent value. A frequency bar chart grows; the tallest bar(s) light up.

Test alone (from the project root):
    python -m manim -pql animations/mode_scene.py ModeScene
"""

from manim import *

from animations.base import DataScene, fmt
from statistics_core.central_tendency import frequencies, calculate_mode as mode


class ModeScene(DataScene):
    def construct(self):
        freq = frequencies(self.data)            # {value: count}, sorted by value
        modes = mode(self.data)                  # [] if no mode
        values, counts = list(freq.keys()), list(freq.values())
        k, top = len(values), max(counts)

        title = Text("Mode = Most Frequent Value", font_size=40).to_edge(UP)
        self.play(Write(title))

        # One slot per distinct value (positions 1..k), so decimals/negatives work too
        axes = Axes(
            x_range=[0, k + 1, 1], y_range=[0, top + 1, 1],
            x_length=min(10, 1.2 * (k + 1)), y_length=4,
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_numbers": True, "font_size": 24},
        ).shift(DOWN * 0.6)
        y_label = Text("count", font_size=22).next_to(axes.y_axis, UP)
        self.play(Create(axes), Write(y_label))

        bar_width = min(0.7, axes.x_length / (k + 1) * 0.7)
        bars, labels = VGroup(), VGroup()
        for i, (v, c) in enumerate(freq.items(), start=1):
            bottom, top_pt = axes.c2p(i, 0), axes.c2p(i, c)
            bar = Rectangle(width=bar_width, height=top_pt[1] - bottom[1],
                            fill_color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
            bar.move_to(bottom, aligned_edge=DOWN)
            bars.add(bar)
            lbl = Text(fmt(v), font_size=22).next_to(bottom, DOWN, buff=0.15)
            if lbl.width > bar_width * 1.4:
                lbl.scale_to_fit_width(bar_width * 1.4)
            labels.add(lbl)
        self.play(FadeIn(labels))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15))

        if not modes:
            msg = Text("Every value appears once -> no mode", font_size=28, color=ORANGE)
            self.play(Write(msg.next_to(title, DOWN, buff=0.4)))
        else:
            tallest = [bars[i] for i, c in enumerate(counts) if c == top]
            self.play(*[Indicate(b, color=GOLD) for b in tallest])
            self.play(*[b.animate.set_fill(GOLD, 1) for b in tallest])
            names = ", ".join(fmt(m) for m in modes)
            kind = "mode" if len(modes) == 1 else f"modes ({len(modes)} tied)"
            msg = Text(f"{kind} = {names}   (appears {top} times)", font_size=28, color=GOLD)
            self.play(Write(msg.next_to(title, DOWN, buff=0.4)))
        self.wait(1.5)
