"""
Variance = average squared distance from the mean.
Points -> mean line -> deviations -> squares -> add areas -> divide by n (or n - 1).

Test alone (from the project root):
    python -m manim -pql animations/variance_scene.py VarianceScene
"""

from manim import *

from animations.base import DataScene, axis_range, fmt
from statistics_core import deviations, calculate_mean as mean, sum_of_squares, variance

PANEL_X = 3.6          # horizontal center of the right-hand explanation panel
PANEL_WIDTH = 5.8


class VarianceScene(DataScene):
    def construct(self):
        data, n, ddof = self.data, len(self.data), self.ddof
        m, devs = mean(data), deviations(data)
        ss, var = sum_of_squares(data), variance(data, ddof)
        divisor = n - ddof
        sym = r"\sigma^2" if ddof == 0 else r"s^2"
        kind = "population (÷ n)" if ddof == 0 else "sample (÷ n-1)"

        title = Text("Variance = Average Squared Distance from Mean", font_size=32).to_edge(UP)
        self.play(Write(title))

        # ---- left: each value as a point (x = position, y = value) ----
        y0, y1, ystep, dec = axis_range(data)
        axes = Axes(
            x_range=[0, n + 1, 1], y_range=[y0, y1, ystep],
            x_length=5.8, y_length=4.2,
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_numbers": True, "font_size": 22,
                           "decimal_number_config": {"num_decimal_places": dec}},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        self.play(Create(axes))
        points = VGroup(*[Dot(axes.c2p(i + 1, v), color=BLUE) for i, v in enumerate(data)])
        self.play(LaggedStart(*[FadeIn(p, scale=2) for p in points], lag_ratio=0.1))

        mean_line = DashedLine(axes.c2p(0, m), axes.c2p(n + 1, m), color=YELLOW)
        mean_lbl = MathTex(rf"\bar{{x}} = {fmt(m)}", color=YELLOW, font_size=28)
        mean_lbl.next_to(axes.c2p(0, m), UP + RIGHT, buff=0.1)
        self.play(Create(mean_line), Write(mean_lbl))

        # ---- deviations: green above the mean, red below ----
        dev_lines = VGroup(*[
            Line(axes.c2p(i + 1, m), axes.c2p(i + 1, v),
                 color=GREEN if v >= m else RED, stroke_width=5)
            for i, v in enumerate(data)
        ])
        dev_text = MathTex(r"\text{deviation} = x_i - \bar{x}", font_size=30)
        dev_text.move_to([PANEL_X, 2.3, 0])
        self.play(Create(dev_lines), Write(dev_text))

        # Why square? Because plain deviations always cancel out to 0
        cancel = MathTex(r"\sum (x_i - \bar{x}) = 0 \;\Rightarrow\; \text{square them}",
                         font_size=28, color=ORANGE).next_to(dev_text, DOWN, buff=0.3)
        self.play(Write(cancel))

        if ss == 0:                                      # all values identical
            msg = Text("All values are equal -> no spread", font_size=26, color=ORANGE)
            result = MathTex(rf"{sym} = 0", font_size=36)
            self.play(Write(VGroup(msg, result).arrange(DOWN).next_to(cancel, DOWN, buff=0.6)))
            self.wait(1.5)
            return

        # ---- squares: side = |deviation|, so area = deviation² ----
        gap = 0.3 if n <= 8 else 0.12                   # more room when labels are shown
        abs_devs = [abs(d) for d in devs]
        unit = min(1.3 / max(abs_devs), (PANEL_WIDTH - gap * (n - 1)) / sum(abs_devs))
        squares = VGroup(*[
            Square(side_length=max(a * unit, 0.03), color=GREEN if d >= 0 else RED,
                   fill_opacity=0.5, stroke_width=2)
            for a, d in zip(abs_devs, devs)
        ]).arrange(RIGHT, buff=gap, aligned_edge=DOWN)
        squares.next_to(cancel, DOWN, buff=0.4).set_x(PANEL_X)
        self.play(*[TransformFromCopy(dev_lines[i], squares[i]) for i in range(n)], run_time=2)

        if n <= 8:                                       # area labels only when they fit
            areas = VGroup(*[
                Text(fmt(d ** 2), font_size=14).next_to(squares[i], DOWN, buff=0.08)
                for i, d in enumerate(devs)
            ])
            self.play(FadeIn(areas))
            anchor = areas
        else:
            anchor = squares

        # ---- add the areas, then divide ----
        ss_tex = MathTex(rf"\sum (x_i - \bar{{x}})^2 = {fmt(ss)}", font_size=30)
        ss_tex.next_to(anchor, DOWN, buff=0.35).set_x(PANEL_X)
        self.play(Write(ss_tex))

        result = MathTex(rf"{sym} = \frac{{{fmt(ss)}}}{{{divisor}}} = {fmt(var)}", font_size=36)
        result.next_to(ss_tex, DOWN, buff=0.3).set_x(PANEL_X)
        box = SurroundingRectangle(result, color=YELLOW, buff=0.12)
        note = Text(f"{kind}, n = {n}", font_size=20, color=GRAY).next_to(box, DOWN, buff=0.12)
        self.play(Write(result), Create(box), FadeIn(note))
        self.wait(1.5)
