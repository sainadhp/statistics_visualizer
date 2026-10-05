# ---------------------------------------------------------------
# Statistics Visualizer: Streamlit + Manim
#
# Base image = official Manim image. It already contains:
#   - manim 0.21.0 (in a virtual env at /opt/venv, already on PATH)
#   - a minimal LaTeX installation (needed for MathTex formulas)
#   - Cairo / Pango libraries (needed for drawing and text)
# So we only add Streamlit and our own code.
# ---------------------------------------------------------------
FROM manimcommunity/manim:v0.21.0

USER root
LABEL maintainer="Sainadhp"
LABEL description="A Streamlit dashboard for visualizing statistics using Manim."
LABEL email="sainadh.potta390@gmail.com"
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=manimuser:manimuser . .

USER manimuser

# Streamlit's default port
EXPOSE 8501

# Lets Docker check that the app is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# Start the dashboard. 0.0.0.0 makes it reachable from outside the container.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]