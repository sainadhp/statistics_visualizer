import streamlit as st
from statistics_core.basic_stats import *

st.title("📊 Statistics Visualizer")

statistic = st.selectbox(
    "Choose a statistic",
    ["Mean", "Median"]
)

st.subheader("Enter your data")
data_input = st.text_input(
    "Enter numbers separated by commas",
    "3,7,4,7,9,2,7,5"
)

st.write("Your input:")
st.write(data_input)

data = [float(x.strip()) for x in data_input.split(",")]
mean_value = calculate_mean(data)
median_value = calculate_median(data)

if statistic == "Mean":
    st.subheader("Mean")
    st.write(f"The mean of your data is: {mean_value}")
else:
    st.subheader("Median")
    st.write(f"The median of your data is: {median_value}")
