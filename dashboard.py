import streamlit as st
import pandas as pd
import plotly.express as px




# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Smart Traffic Analytics",
    page_icon="🚦",
    layout="wide"
)


# ==========================================
# Load Data
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("traffic_density.csv")
    return df


df = load_data()


# ==========================================
# Title
# ==========================================

st.title("🚦 Smart Traffic Analytics")

st.markdown(
    "Interactive dashboard for traffic density analysis "
    "using YOLO and BoT-SORT."
)


# ==========================================
# Sidebar
# ==========================================

st.sidebar.header("Dashboard Controls")


# ------------------------------------------
# Metrics Selection
# ------------------------------------------

st.sidebar.subheader("Density Metrics")

show_total = st.sidebar.checkbox(
    "Total Density",
    value=True
)

show_left = st.sidebar.checkbox(
    "Left Density",
    value=True
)

show_right = st.sidebar.checkbox(
    "Right Density",
    value=True
)


# ==========================================
# Time Range
# ==========================================

min_time = float(df["time"].min())
max_time = float(df["time"].max())

time_range = st.sidebar.slider(
    "Time Range (seconds)",
    min_value=min_time,
    max_value=max_time,
    value=(min_time, max_time)
)


# Filter data
filtered_df = df[
    (df["time"] >= time_range[0])
    & (df["time"] <= time_range[1])
].copy()


# ==========================================
# Header Information
# ==========================================

st.subheader("Traffic Overview")


# ==========================================
# Calculate KPIs
# ==========================================

average_density = filtered_df[
    "total_density"
].mean()

maximum_density = filtered_df[
    "total_density"
].max()

minimum_density = filtered_df[
    "total_density"
].min()


peak_index = filtered_df[
    "total_density"
].idxmax()

peak_time = filtered_df.loc[
    peak_index,
    "time"
]


# ==========================================
# KPI Cards
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Average Density",
        f"{average_density:.2f}"
    )


with col2:

    st.metric(
        "Maximum Density",
        int(maximum_density)
    )


with col3:

    st.metric(
        "Minimum Density",
        int(minimum_density)
    )


with col4:

    st.metric(
        "Peak Time",
        f"{peak_time:.2f} s"
    )


# ==========================================
# Main Density Chart
# ==========================================

st.subheader("Traffic Density Over Time")


chart_data = filtered_df[
    [
        "time",
        "left_density",
        "right_density",
        "total_density"
    ]
].copy()


fig = px.line(
    chart_data,
    x="time",
    y=[],
    labels={
        "time": "Time (seconds)",
        "value": "Number of Vehicles",
        "variable": "Traffic Direction"
    }
)


# Add selected metrics
if show_total:

    fig.add_scatter(
        x=filtered_df["time"],
        y=filtered_df["total_density"],
        mode="lines",
        name="Total Density"
    )


if show_left:

    fig.add_scatter(
        x=filtered_df["time"],
        y=filtered_df["left_density"],
        mode="lines",
        name="Left Density"
    )


if show_right:

    fig.add_scatter(
        x=filtered_df["time"],
        y=filtered_df["right_density"],
        mode="lines",
        name="Right Density"
    )


fig.update_layout(
    xaxis_title="Time (seconds)",
    yaxis_title="Number of Vehicles",
    hovermode="x unified",
    height=500
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# Direction Comparison
# ==========================================

st.subheader("Left vs Right Traffic")


col1, col2 = st.columns(2)


with col1:

    average_left = filtered_df[
        "left_density"
    ].mean()

    st.metric(
        "Average Left Density",
        f"{average_left:.2f}"
    )


with col2:

    average_right = filtered_df[
        "right_density"
    ].mean()

    st.metric(
        "Average Right Density",
        f"{average_right:.2f}"
    )


# ==========================================
# Direction Chart
# ==========================================

direction_df = filtered_df[
    [
        "time",
        "left_density",
        "right_density"
    ]
].copy()


direction_fig = px.line(
    direction_df,
    x="time",
    y=[
        "left_density",
        "right_density"
    ],
    labels={
        "time": "Time (seconds)",
        "value": "Number of Vehicles",
        "variable": "Direction"
    }
)


direction_fig.update_layout(
    height=450,
    hovermode="x unified"
)


st.plotly_chart(
    direction_fig,
    use_container_width=True
)


# ==========================================
# Traffic Density Distribution
# ==========================================

st.subheader("Traffic Density Distribution")


distribution_fig = px.histogram(
    filtered_df,
    x="total_density",
    nbins=20,
    labels={
        "total_density": "Number of Vehicles"
    }
)


distribution_fig.update_layout(
    height=400
)


st.plotly_chart(
    distribution_fig,
    use_container_width=True
)


# ==========================================
# Maximum Density Information
# ==========================================

st.subheader("Peak Traffic Information")


peak_row = filtered_df.loc[
    filtered_df["total_density"].idxmax()
]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Peak Density",
        int(peak_row["total_density"])
    )


with col2:

    st.metric(
        "Left at Peak",
        int(peak_row["left_density"])
    )


with col3:

    st.metric(
        "Right at Peak",
        int(peak_row["right_density"])
    )


st.info(
    f"Peak traffic density occurred at "
    f"{peak_row['time']:.2f} seconds."
)


# ==========================================
# Data Table
# ==========================================

with st.expander("View Traffic Density Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ==========================================
# Video
# ==========================================

st.subheader("Traffic Tracking Video")


video_path = "demo.mp4"

try:

    st.video(video_path)

except Exception:

    st.warning(
        "Traffic tracking video could not be loaded."
    )


# ==========================================
# Footer
# ==========================================

st.markdown("---")

st.caption(
    "Smart Traffic Analytics | "
    "YOLO + BoT-SORT + Traffic Density Analysis"
)