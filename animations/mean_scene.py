from manim import *

from animations.base import DataScene, fmt, axis_range
from statistics_core.central_tendency import calculate_mean

class MeanScene(DataScene):
    
    def construct(self):
        data, n = self.data, len(self.data)
        m = calculate_mean(data)

        title = Text("Mean = Balance Point", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Number line that fits the data
        start, end, step, dec = axis_range(data)
        line = NumberLine(
            x_range=[start, end, step], length=11, include_numbers=True, font_size=24,
            decimal_number_config={"num_decimal_places": dec},
        ).shift(DOWN * 1.5)
        self.play(Create(line))

        # One dot per value; repeated values stack upward
        dots, seen = VGroup(), {}
        for v in data:
            seen[v] = seen.get(v, 0) + 1
            dots.add(Dot(line.n2p(v) + UP * 0.3 * seen[v], color=BLUE, radius=0.11))
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN) for d in dots], lag_ratio=0.15))

        # Formula with the real numbers (written out only for short lists)
        parts = [r"\bar{x} = \frac{\sum x_i}{n}"]
        if n <= 8:
            terms = " + ".join(f"({fmt(v)})" if v < 0 else fmt(v) for v in data)
            parts.append(rf"= \frac{{{terms}}}{{{n}}}")
        parts.append(rf"= \frac{{{fmt(sum(data))}}}{{{n}}} = {fmt(m)}")
        formula = MathTex(*parts).scale(0.8).next_to(title, DOWN, buff=0.4)
        if formula.width > 12.5:
            formula.scale_to_fit_width(12.5)
        for part in formula:
            self.play(Write(part))

        # Fulcrum (triangle) slides from the left end to the mean.
        # ValueTracker = a number we can animate; always_redraw follows it.
        tracker = ValueTracker(start)
        fulcrum = always_redraw(
            lambda: Triangle(color=YELLOW, fill_opacity=1).scale(0.2)
            .next_to(line.n2p(tracker.get_value()), DOWN, buff=0.5)
        )
        self.play(FadeIn(fulcrum))
        self.play(tracker.animate.set_value(m), run_time=2.5)

        height = max(seen.values()) * 0.3 + 0.6
        mean_line = DashedLine(line.n2p(m), line.n2p(m) + UP * height, color=YELLOW)
        label = Text(f"mean = {fmt(m)}", font_size=28, color=YELLOW).next_to(mean_line, UP)
        self.play(Create(mean_line), Write(label))
        self.wait(1.5)
