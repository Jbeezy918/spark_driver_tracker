
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Spark Driver Dashboard", layout="wide", page_icon="🚗")

# Custom styles
st.markdown(
    """
    <style>
        body {background-color: #f1f3f6;}
        .main {background-color: #ffffff;}
        .block-container {padding-top: 2rem;}
        .stTextInput, .stSelectbox, .stNumberInput, .stCheckbox {margin-bottom: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚗 Spark Trip Input Dashboard")

# Section 1: Trip Snapshot
st.subheader("Trip Snapshot")
col1, col2, col3, col4 = st.columns(4)
with col1:
    vehicle_type = st.selectbox("Vehicle Type", ["Sedan", "Pickup", "SUV", "Van"])
with col2:
    engine_type = st.selectbox("Engine Type", ["4-cylinder", "6-cylinder", "8-cylinder"])
with col3:
    fuel_type = st.selectbox("Fuel Type", ["Gas", "Hybrid", "Electric"])
with col4:
    avg_mpg = {"Sedan": 30, "Pickup": 18, "SUV": 22, "Van": 20}
    st.markdown(f"**MPG Avg:** {avg_mpg.get(vehicle_type, 'N/A')} MPG")

# Section 2: Delivery Details
st.subheader("Delivery Details")
col5, col6, col7 = st.columns(3)
with col5:
    stops = st.selectbox("Stops", list(range(1, 100)))
with col6:
    shopping = st.checkbox("Include Shopping")
with col7:
    if shopping:
        items = st.number_input("Items Picked Up", min_value=0, max_value=999, step=1)
    else:
        st.markdown("🛒 Shopping not included.")

# Section 3: Estimated Times
st.subheader("Estimated Time")
col8, col9 = st.columns(2)
with col8:
    est_hours = st.selectbox("Hours", list(range(0, 10)))
with col9:
    est_minutes = st.selectbox("Minutes", list(range(0, 60)))

# Section 4: Incentives
st.subheader("Incentives")
col10, col11 = st.columns(2)
with col10:
    incentive_name = st.text_input("Incentive Name", placeholder="e.g. Bonus Pay")
with col11:
    incentive_value = st.number_input("Incentive Value", min_value=0.0, step=0.5)

# Section 5: Summary Graph
st.subheader("Summary")
summary_type = st.selectbox("View Averages By", ["Hourly", "Daily", "Weekly", "Monthly"])
fake_data = pd.DataFrame({
    "Time Period": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "Earnings": [120.5, 145.0, 160.0, 135.5]
})
fig = px.bar(fake_data, x="Time Period", y="Earnings", title=f"Earnings by {summary_type}")
st.plotly_chart(fig, use_container_width=True)

# Section 6: Export
st.subheader("Export Options")
col12, col13 = st.columns(2)
with col12:
    st.button("Export CSV")
with col13:
    st.button("Export Excel")

st.success("Trip input complete! Make sure to review before saving.")
