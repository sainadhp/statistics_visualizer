"""
Median = middle value. Boxes sort themselves, the middle one(s) light up.

Test alone (from the project root):
    python -m manim -pql animations/median_scene.py MedianScene
"""

import numpy as np
from manim import *

from animations.base import DataScene, fmt
from statistics_core.central_tendency import calculate_mean as mean, calculate_median as median


class MedianScene(DataScene):
    def make_cell(self, value):
        box = Square(side_length=0.9, color=WHITE)
        num = Text(fmt(value), font_size=28)
        if num.width > 0.8:                          # long numbers shrink to fit
            num.scale_to_fit_width(0.8)
        return VGroup(box, num)                      # [0] = box, [1] = number

    def construct(self):
        data, n = self.data, len(self.data)
        med, avg = median(data), mean(data)

        title = Text("Median = Middle Value", font_size=40).to_edge(UP)
        self.play(Write(title))

        cells = VGroup(*[self.make_cell(v) for v in data]).arrange(RIGHT, buff=0.15)
        if cells.width > 12.5:
            cells.scale_to_fit_width(12.5)
        self.play(FadeIn(cells, lag_ratio=0.1))

        # Step 1: sort -> move each box to its sorted slot
        step = Text("Step 1: sort the values", font_size=28).to_edge(DOWN)
        self.play(Write(step))
        order = np.argsort(data, kind="stable")
        slots = cells.copy().arrange(RIGHT, buff=0.15).move_to(cells)
        self.play(*[cells[i].animate.move_to(slots[s]) for s, i in enumerate(order)], run_time=2)
        sorted_cells = VGroup(*[cells[i] for i in order])
        svals = sorted(data)

        # Step 2: odd n -> one middle value; even n -> average of two
        if n % 2 == 1:
            mid = [n // 2]
            msg = f"Step 2: n = {n} (odd) -> take position {n // 2 + 1}"
            tex = rf"\text{{median}} = {fmt(med)}"
        else:
            mid = [n // 2 - 1, n // 2]
            a, b = svals[mid[0]], svals[mid[1]]
            msg = f"Step 2: n = {n} (even) -> average the two middle values"
            tex = rf"\text{{median}} = \frac{{{fmt(a)} + {fmt(b)}}}{{2}} = {fmt(med)}"
        self.play(Transform(step, Text(msg, font_size=26).to_edge(DOWN)))
        self.play(*[sorted_cells[i][0].animate.set_color(GREEN).set_fill(GREEN, 0.3) for i in mid])

        result = MathTex(tex, color=GREEN).next_to(cells, DOWN, buff=0.7)
        self.play(Write(result))
        self.wait(1)

        # Compare with the mean -> hint about skew / outliers
        if abs(avg - med) < 1e-9:
            hint = "mean = median -> data is balanced"
        elif avg > med:
            hint = "mean > median -> pulled right by large values"
        else:
            hint = "mean < median -> pulled left by small values"
        compare = VGroup(
            MathTex(rf"\text{{mean}} = {fmt(avg)}", color=YELLOW),
            Text(hint, font_size=26, color=ORANGE),
        ).arrange(DOWN).next_to(title, DOWN, buff=0.5)
        self.play(Write(compare))
        self.wait(1.5)
