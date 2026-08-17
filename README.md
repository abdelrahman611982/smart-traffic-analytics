# Smart Traffic Analytics

## Demo

Watch the traffic tracking demo:

[🎥 Watch Demo Video](demo.mp4)

[🚀 Live Dashboard](https://smart-traffic-analytics-xphsj5y8dkdlwpsptpzds.streamlit.app/)

A Computer Vision project for traffic analysis using YOLO and BoT-SORT.
The system detects and tracks vehicles, counts vehicles crossing a line,
measures current traffic density inside selected road regions, stores
density data over time, and provides an interactive Streamlit dashboard.

## Pipeline

``` text
Input Frames
    ↓
YOLO Detection
    ↓
BoT-SORT Tracking
    ↓
Track IDs
    ↓
Line Crossing
    ↓
Vehicle Counting
    ↓
ROI-Based Traffic Density
    ↓
CSV Time-Series Data
    ↓
Traffic Analytics
    ↓
Interactive Streamlit Dashboard
```

## Features

-   Vehicle detection using YOLO.
-   Multi-object tracking using BoT-SORT.
-   Car, motorcycle, bus, and truck detection.
-   Line crossing using BoT-SORT track IDs.
-   Counting each tracked vehicle once.
-   Vehicle counts by class.
-   Separate left and right traffic ROIs.
-   Current traffic density based on tracked IDs inside each ROI.
-   Density recorded for every processed frame.
-   CSV-based traffic analytics.
-   Traffic density statistics and visualization.
-   Interactive Streamlit dashboard.

## Project Structure

``` text
smart-traffic-analytics/
│
├── MVI_40191/                 # Input image frames
├── tracker.py                 # Main detection, tracking, counting and density pipeline
├── roi_selector.py            # Interactive ROI point selection
├── density_analysis.py        # Density statistics and plots
├── dashboard.py               # Streamlit dashboard
├── check_data.py              # Dataset checking utility
│
├── traffic_density.csv        # Density time-series output
├── traffic_tracking.mp4       # Tracking/counting output video
├── traffic_roi.mp4            # ROI test/output video
│
├── yolo11n.pt                 # YOLO model weights
├── requirements.txt
└── README.md
```

## Installation

Install the required Python packages:

``` bash
pip install -r requirements.txt
```

## Run the Main Pipeline

``` bash
python tracker.py
```

This processes the frames in `MVI_40191/` and generates:

``` text
traffic_tracking.mp4
traffic_density.csv
```

## Analyze Traffic Density

``` bash
python density_analysis.py
```

This calculates:

-   Average density
-   Maximum density
-   Minimum density
-   Peak density time
-   Average left density
-   Average right density

It also displays the traffic density graph.

## Run the Dashboard

Start Streamlit with:

``` bash
streamlit run dashboard.py
```

The dashboard provides interactive controls for the time range and
displayed density metrics and shows the tracking video and analytics.

## Vehicle Counting

BoT-SORT track IDs are used to avoid counting the same vehicle multiple
times.

A vehicle is counted when its tracked center crosses the configured
horizontal counting line.

The cumulative counters include:

``` text
Total Count
Cars
Motorcycles
Buses
Trucks
```

## Traffic Density

Traffic density is calculated for every frame:

``` text
Left Density  = unique tracked IDs inside the left ROI
Right Density = unique tracked IDs inside the right ROI
Total Density = unique tracked IDs across both ROIs
```

The values are saved to:

``` text
traffic_density.csv
```

with:

``` text
frame
time
left_density
right_density
total_density
```

## Dashboard

The Streamlit dashboard includes:

-   Average density
-   Maximum density
-   Minimum density
-   Peak traffic time
-   Left vs. right density
-   Traffic density over time
-   Density distribution
-   Time-range filtering
-   Raw density data table
-   Processed tracking video

## Speed Estimation

Speed estimation was intentionally excluded.

Reliable speed in km/h requires camera calibration or known real-world
reference distances. The available footage does not provide a
sufficiently reliable metric reference, so speed estimation was not
included rather than reporting inaccurate values.

## Technologies

-   Python
-   YOLO
-   Ultralytics
-   BoT-SORT
-   OpenCV
-   NumPy
-   Pandas
-   Matplotlib
-   Plotly
-   Streamlit

## Notes

The input frames, YOLO weights, CSV output, and MP4 videos can be large.
For a GitHub repository, consider excluding large generated files and
dataset/model files with `.gitignore`, or using Git LFS when
appropriate.

## Future Improvements

-   Automatic congestion-level classification.
-   More advanced traffic-flow statistics.
-   Vehicle trajectory and lane-level analysis.
-   Multiple video/camera support.
-   Real-time camera or video input.
-   Robust camera calibration for metric speed estimation.

