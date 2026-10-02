import streamlit as st
from statistics_core.central_tendency import *
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
quality_label = st.sidebar.selectbox("Video quality", list(QUALITIES))

# Validate the input before doing anything else
try:
    data = parse_numbers(raw_text)
except ValueError:
    st.error("Only numbers please, for example: 3, 7, 4, 9")
    st.stop()                                                      # stop this run here
if not 2 <= len(data) <= 15:
    st.error("Please enter between 2 to 15 values.")
    st.stop()

def show_mean(data):
    st.write("The **mean** (average) is the balance point of the data: "
             "add everything up and share it equally.")
    st.latex(r"\bar{x} = \frac{\sum x_i}{n}")

    st.subheader("Step by step")
    total = sum(data)
    st.markdown(f"1. Add all values: {' + '.join(fmt(v) for v in data)} = **{fmt(total)}**")
    st.markdown(f"2. Count the values: n = **{len(data)}**")
    st.markdown(f"3. Divide: {fmt(total)} ÷ {len(data)} = **{fmt(calculate_mean(data))}**")
    st.metric("Mean", fmt(calculate_mean(data)))

PAGES = {"Mean": show_mean, "Median": None, "Mode": None}  # add show_median / show_mode later


# ------------------------------------------------------------------
# Main area
# ------------------------------------------------------------------
st.title(concept)
st.caption(f"Data ({len(data)} values): {', '.join(fmt(v) for v in data)}")

left, right = st.columns([1, 1.4])                 # two side-by-side areas

with left:
    PAGES[concept](data)                           # calls show_mean / show_median / show_mode

with right:
    st.subheader("🎬 Animation")
    scene_cls = SCENES[concept]
    quality = QUALITIES[quality_label]

    # A button returns True only on the run right after it's clicked
    if st.button(f"Generate {concept.lower()} animation", type="primary"):
        with st.spinner("Manim is rendering the video... (about 5-15 seconds)"):
            render_scene(scene_cls, data, quality)

    # If a video for this exact data already exists, show it (survives reruns)
    path = video_path(scene_cls, data, quality)
    if path.exists():
        st.video(str(path), autoplay=True, muted=True)
    else:
        st.info("Click the button to create the animation for your data.")