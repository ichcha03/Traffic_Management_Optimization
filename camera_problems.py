# app.py
import streamlit as st
import numpy as np
import cv2
from vehicle_counter import VehicleCounter
from traffic_optimizer import TrafficSignalOptimizer

st.set_page_config(page_title="AI Traffic Signal Optimizer", layout="wide")

# Sidebar
st.sidebar.header("Settings")
confidence = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.3, 0.05)

# Load classes once
@st.cache_resource
def load_resources(conf_threshold):
    return VehicleCounter(conf_threshold=conf_threshold), TrafficSignalOptimizer()

counter, optimizer = load_resources(confidence)

# App Title
st.title("🚦 AI Traffic Flow Optimization System")
st.markdown("Upload images for all 4 lanes (North, South, East, West) to calculate optimal signal timings.")

# Create 4 columns for the 4 lanes
col1, col2, col3, col4 = st.columns(4)
lanes = ['North', 'South', 'East', 'West']
lane_files = {}

# File Uploaders
with col1:
    st.subheader("North Lane")
    lane_files['North'] = st.file_uploader("Upload North Image", type=["jpg", "jpeg", "png"], key="north")
with col2:
    st.subheader("South Lane")
    lane_files['South'] = st.file_uploader("Upload South Image", type=["jpg", "jpeg", "png"], key="south")
with col3:
    st.subheader("East Lane")
    lane_files['East'] = st.file_uploader("Upload East Image", type=["jpg", "jpeg", "png"], key="east")
with col4:
    st.subheader("West Lane")
    lane_files['West'] = st.file_uploader("Upload West Image", type=["jpg", "jpeg", "png"], key="west")

if st.button("Analyze Traffic & Optimize Signals"):
    # Check if all files are uploaded
    if not all(lane_files.values()):
        st.error("Please upload images for all 4 lanes to proceed.")
    else:
        lane_counts = {}
        processed_images = {}
        
        with st.spinner("Processing images and detecting vehicles..."):
            for lane, uploaded_file in lane_files.items():
                # Convert uploaded image to numpy array
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, 1)
                
                # Process image
                annotated_image, counts = counter.process_image(image)
                lane_counts[lane] = counts['by_class']
                processed_images[lane] = annotated_image

        # Optimize Signals
        optimization_results = optimizer.optimize_signals(lane_counts)
        
        st.success("Analysis and Optimization Complete!")
        
        # Display Results
        st.header("Optimization Results")
        st.metric("Total Cycle Time", f"{optimization_results['actual_cycle_time']}s")
        
        # Display Lane Details
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        cols = [res_col1, res_col2, res_col3, res_col4]
        
        for i, lane in enumerate(lanes):
            with cols[i]:
                st.subheader(f"{lane} Lane")
                st.image(cv2.cvtColor(processed_images[lane], cv2.COLOR_BGR2RGB), use_column_width=True)
                
                lane_data = optimization_results['lanes'][lane]
                st.markdown(f"**Green Time:** {lane_data['green_time']}s")
                st.markdown(f"**Red Time:** {lane_data['red_time']}s")
                st.markdown(f"**Yellow Time:** {lane_data['yellow_time']}s")
                st.markdown(f"**Density Score:** {lane_data['density_score']:.1f}")
                
                st.markdown("---")
                st.markdown("**Vehicle Counts:**")
                for v_type, count in lane_counts[lane].items():
                    if count > 0:
                        st.write(f"{v_type}: {count}")

# Footer
st.markdown("---")
st.markdown("Built with YOLOv8 + Streamlit")

