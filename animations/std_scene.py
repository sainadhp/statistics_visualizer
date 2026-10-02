"""
Standard deviation = square root of variance.
Part 1: variance is the AREA of a square -> σ is its SIDE (back in original units).
Part 2: on a number line, the band mean ± σ shows the "typical distance" from the mean.

Test alone (from the project root):
    python -m manim -pql animations/std_scene.py StdScene
"""

from manim import *

from animations.base import DataScene, axis_range, fmt
from statistics_core.central_tendency import calculate_mean as mean
from statistics_core.dispersion import variance, std, within_k_std


class StdScene(DataScene):
    def construct(self):
        data, n, ddof = self.data, len(self.data), self.ddof
        m, var, sd = mean(data), variance(data, ddof), std(data, ddof)
        vsym, ssym = (r"\sigma^2", r"\sigma") if ddof == 0 else (r"s^2", r"s")

        title = Text("Standard Deviation = √Variance", font_size=38).to_edge(UP)
        self.play(Write(title))

        # ---------- Part 1: area -> side ----------
        if sd > 0:
            square = Square(side_length=2.6, color=BLUE, fill_opacity=0.35).shift(LEFT * 2.5 + DOWN * 0.3)
            area = MathTex(rf"\text{{area}} = {vsym} = {fmt(var)}", font_size=30).move_to(square)
            self.play(DrawBorderThenFill(square), Write(area))

            side = Brace(square, DOWN)
            side_lbl = MathTex(rf"\text{{side}} = {ssym} = \sqrt{{{fmt(var)}}} = {fmt(sd)}",
                               font_size=30, color=YELLOW).next_to(side, DOWN)
            self.play(GrowFromCenter(side), Write(side_lbl))

            why = VGroup(
                Text("Variance is in squared units", font_size=24),
                Text("(e.g. marks², rupees²)", font_size=20, color=GRAY),
                Text("Square root brings it back", font_size=24, color=YELLOW),
                Text("to the original units", font_size=24, color=YELLOW),
            ).arrange(DOWN, buff=0.15).shift(RIGHT * 3.2 + DOWN * 0.3)
            self.play(FadeIn(why, lag_ratio=0.3))
            self.wait(1.5)
            self.play(FadeOut(VGroup(square, area, side, side_lbl, why)))
        else:
            msg = Text("All values are equal -> standard deviation = 0", font_size=28, color=ORANGE)
            self.play(Write(msg))
            self.wait(1.5)
            return

        # ---------- Part 2: mean ± σ on the number line ----------
        start, end, step, dec = axis_range(list(data) + [m - sd, m + sd])
        line = NumberLine(
            x_range=[start, end, step], length=11.5, include_numbers=True, font_size=22,
            decimal_number_config={"num_decimal_places": dec},
        ).shift(DOWN * 1.8)
        self.play(Create(line))

        dots, seen = VGroup(), {}
        for v in data:
            seen[v] = seen.get(v, 0) + 1
            d = Dot(line.n2p(v) + UP * 0.28 * seen[v], radius=0.1, color=BLUE)
            d.value = v
            dots.add(d)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN) for d in dots], lag_ratio=0.1))

        height = max(seen.values()) * 0.28 + 0.9
        mean_line = DashedLine(line.n2p(m), line.n2p(m) + UP * height, color=YELLOW)
        mean_lbl = MathTex(rf"\bar{{x}} = {fmt(m)}", color=YELLOW, font_size=28).next_to(mean_line, UP)
        self.play(Create(mean_line), Write(mean_lbl))

        # The band grows outwards from the mean: one σ to each side
        left, right = line.n2p(m - sd), line.n2p(m + sd)
        band = Rectangle(width=right[0] - left[0], height=height, stroke_width=0,
                         fill_color=GREEN, fill_opacity=0.2)
        band.move_to(line.n2p(m), aligned_edge=DOWN)
        self.play(GrowFromCenter(band))
        lo_lbl = MathTex(rf"\bar{{x}} - {ssym} = {fmt(m - sd)}", font_size=24, color=GREEN)
        hi_lbl = MathTex(rf"\bar{{x}} + {ssym} = {fmt(m + sd)}", font_size=24, color=GREEN)
        lo_lbl.next_to(line.n2p(m - sd), DOWN, buff=0.6)
        hi_lbl.next_to(line.n2p(m + sd), DOWN, buff=0.6)
        self.play(Write(lo_lbl), Write(hi_lbl))

        # Colour dots inside the band
        inside = [d for d in dots if abs(d.value - m) <= sd + 1e-12]
        self.play(*[d.animate.set_color(GREEN) for d in inside],
                  *[d.animate.set_color(GRAY) for d in dots if d not in inside])
        k, total = within_k_std(data, 1, ddof)
        summary = Text(f"{k} of {total} values ({k / total:.0%}) lie within 1 standard deviation of the mean",
                       font_size=24, color=GREEN).next_to(title, DOWN, buff=0.4)
        self.play(Write(summary))
        self.wait(2)
