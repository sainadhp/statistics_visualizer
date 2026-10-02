import streamlit as st
from statistics_core.central_tendency import *
from statistics_core.dispersion import *
from animations import SCENES
from animations.base import DEFAULT_DATA, fmt
from utils.renderer import QUALITIES, render_scene, video_path


# Page setup
st.set_page_config(page_title="Statistics Visualizer", page_icon="📊", layout="wide")


# Helper: turn the text box into a list of numbers
def parse_numbers(text):
    """'3, 7 4' -> [3.0, 7.0, 4.0]. Raises ValueError if something isn't a number."""
    cleaned = text.replace(";", ",").replace("\n", ",").replace(" ", ",")
    return [float(t) for t in cleaned.split(",") if t.strip()]


# Sidebar = the menu on the left (collapses to ☰ / ">" on small screens)
st.sidebar.title("📊 Stats Visualizer")
concept = st.sidebar.radio("Choose a concept", list(SCENES))      # "Mean", "Median", "Mode"

st.sidebar.divider()
st.sidebar.subheader("Your data")
raw_text = st.sidebar.text_area(
    "Numbers (separate with commas or spaces)",
    value=", ".join(fmt(v) for v in DEFAULT_DATA),                 # default input
    height=100,
)

# Only variance & standard deviation need this choice
params = {}
if concept in ("Variance", "Standard Deviation"):
    kind = st.sidebar.radio(
        "Treat the data as a...",
        ["Population (÷ n)", "Sample (÷ n − 1)"],
        help="Population = you have every value. Sample = your data is a subset of a bigger group.",
    )
    params["ddof"] = 0 if kind.startswith("Population") else 1

quality_label = st.sidebar.selectbox("Video quality", list(QUALITIES))

# Validate the input before doing anything else
try:
    data = parse_numbers(raw_text)
except ValueError:
    st.error("Only numbers please, for example: 3, 7, 4, 9")
    st.stop()                                                      # stop this run here
if not 2 <= len(data) <= 15:
    st.error("Please enter between 2 and 15 numbers.")
    st.stop()

def show_mean(data, params):
    st.write("The **mean** (average) is the balance point of the data: "
             "add everything up and share it equally.")
    st.latex(r"\bar{x} = \frac{\sum x_i}{n}")

    st.subheader("Step by step")
    total = sum(data)
    st.markdown(f"1. Add all values: {' + '.join(fmt(v) for v in data)} = **{fmt(total)}**")
    st.markdown(f"2. Count the values: n = **{len(data)}**")
    st.markdown(f"3. Divide: {fmt(total)} ÷ {len(data)} = **{fmt(calculate_mean(data))}**")
    st.metric("Mean", fmt(calculate_mean(data)))

def show_median(data, params):
    st.write("The **median** is the middle value after sorting. "
             "Half the data is below it, half above.")
    st.latex(r"\text{median} = \begin{cases} x_{\left(\frac{n+1}{2}\right)} & n \text{ odd} \\[4pt]"
             r"\dfrac{x_{\left(\frac{n}{2}\right)} + x_{\left(\frac{n}{2}+1\right)}}{2} & n \text{ even}"
             r"\end{cases}")

    st.subheader("Step by step")
    s, n = sorted(data), len(data)
    st.markdown(f"1. Sort: {', '.join(fmt(v) for v in s)}")
    if n % 2 == 1:
        pos = (n + 1) // 2
        st.markdown(f"2. n = {n} is **odd** → take position {pos}")
        st.markdown(f"3. Median = **{fmt(s[pos - 1])}**")
    else:
        a, b = s[n // 2 - 1], s[n // 2]
        st.markdown(f"2. n = {n} is **even** → average positions {n // 2} and {n // 2 + 1}")
        st.markdown(f"3. ({fmt(a)} + {fmt(b)}) ÷ 2 = **{fmt(calculate_median(data))}**")
    col1, col2 = st.columns(2)
    col1.metric("Median", fmt(calculate_median(data)))
    col2.metric("Mean (for comparison)", fmt(calculate_mean(data)))

def show_mode(data, params):
    st.write("The **mode** is the value that appears most often. "
             "Data can have one mode, several modes, or no mode.")
    st.latex(r"\text{mode} = \text{value with the highest frequency}")

    st.subheader("Step by step")
    st.markdown("1. Count how often each value appears:")
    freq = frequencies(data)
    st.table({"value": [fmt(v) for v in freq], "count": list(freq.values())})
    modes = calculate_mode(data)
    if not modes:
        st.markdown("2. Every value appears once → **no mode**")
        st.metric("Mode", "none")
    else:
        st.markdown(f"2. Highest count = {max(freq.values())} → mode = "
                    f"**{', '.join(fmt(m) for m in modes)}**")
        st.metric("Mode", ", ".join(fmt(m) for m in modes))

def show_variance(data, params):
    ddof = params["ddof"]
    n = len(data)
    st.write("**Variance** measures spread: the average *squared* distance of each value from the mean. "
             "Bigger variance = data more spread out.")
    if ddof == 0:
        st.latex(r"\sigma^2 = \frac{\sum (x_i - \mu)^2}{n}")
    else:
        st.latex(r"s^2 = \frac{\sum (x_i - \bar{x})^2}{n - 1}")
        st.info("Sample: we divide by n − 1 (Bessel's correction). Deviations from a sample's own mean "
                "come out a little too small, and n − 1 fixes that.")

    st.subheader("Step by step")
    m = calculate_mean(data)
    st.markdown(f"1. Find the mean: **{fmt(m)}**")
    st.markdown("2. Subtract the mean from each value, then square the result:")
    devs = deviations(data)
    st.table({
        "value (xᵢ)": [fmt(v) for v in data],
        "deviation (xᵢ − x̄)": [fmt(d) for d in devs],
        "squared (xᵢ − x̄)²": [fmt(d ** 2) for d in devs],
    })
    st.markdown(f"Notice: the deviations add up to **{fmt(sum(devs))}**. "
                "Positives and negatives cancel, which is why we square them.")
    ss = sum_of_squares(data)
    st.markdown(f"3. Add the squares: **{fmt(ss)}**")
    divisor = n - ddof
    st.markdown(f"4. Divide by {'n' if ddof == 0 else 'n − 1'} = {divisor}: "
                f"{fmt(ss)} ÷ {divisor} = **{fmt(variance(data, ddof))}**")
    st.metric("Variance", fmt(variance(data, ddof)))

def show_std(data, params):
    ddof = params["ddof"]
    sym = "σ" if ddof == 0 else "s"
    st.write("**Standard deviation** is the square root of variance. It brings the spread back to the "
             "data's original units, so you can read it as the *typical distance from the mean*.")
    if ddof == 0:
        st.latex(r"\sigma = \sqrt{\sigma^2} = \sqrt{\frac{\sum (x_i - \mu)^2}{n}}")
    else:
        st.latex(r"s = \sqrt{s^2} = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n - 1}}")

    st.subheader("Step by step")
    var, sd, m = variance(data, ddof), std(data, ddof), calculate_mean(data)
    st.markdown(f"1. Variance ({'population' if ddof == 0 else 'sample'}): **{fmt(var)}** "
                "(see the Variance page for how)")
    st.markdown(f"2. Square root: √{fmt(var)} = **{fmt(sd)}**")
    k, total = within_k_std(data, 1, ddof)
    st.markdown(f"3. Range mean ± {sym}: {fmt(m - sd)} to {fmt(m + sd)}. "
                f"**{k} of {total}** values fall inside it.")

    col1, col2 = st.columns(2)
    col1.metric("Population σ (÷ n)", fmt(std(data, 0)))
    col2.metric("Sample s (÷ n − 1)", fmt(std(data, 1)))

PAGES = {
    "Mean": show_mean, 
    "Median": show_median, 
    "Mode": show_mode,
    "Variance": show_variance,
    "Standard Deviation": show_std,
} 


# ------------------------------------------------------------------
# Main area
# ------------------------------------------------------------------
st.title(concept)
st.caption(f"Data ({len(data)} values): {', '.join(fmt(v) for v in data)}")

left, right = st.columns([1, 1.4])                 # two side-by-side areas

with left:
    PAGES[concept](data, params)                   # calls show_mean, show_variance, ...

with right:
    st.subheader("🎬 Animation")
    scene_cls = SCENES[concept]
    quality = QUALITIES[quality_label]

    # A button returns True only on the run right after it's clicked
    if st.button(f"Generate {concept.lower()} animation", type="primary"):
        with st.spinner("Manim is rendering the video... (about 5-15 seconds)"):
            render_scene(scene_cls, data, quality, params)

    # If a video for this exact data already exists, show it (survives reruns)
    path = video_path(scene_cls, data, quality, params)
    if path.exists():
        st.video(str(path), autoplay=True, muted=True)
    else:
        st.info("Click the button to create the animation for your data.")