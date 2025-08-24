import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Spark Driver Tracker", layout="wide", page_icon="🚗")

# Custom styles
st.markdown(
    """
    <style>
        body {background-color: #f1f3f6;}
        .main {background-color: #ffffff;}
        .block-container {padding-top: 2rem;}
        .stTextInput, .stSelectbox, .stNumberInput, .stCheckbox {margin-bottom: 10px;}
        .metric-box {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚗 Spark Driver Tracker")
st.subheader("Track Every Trip. Maximize Every Dollar.")

# Initialize session state for trip data
if 'trips' not in st.session_state:
    st.session_state.trips = []

# Accurate MPG data based on research
MPG_DATA = {
    "🚗 Sedan": {"4️⃣ 4-cylinder": 28, "6️⃣ 6-cylinder": 24, "8️⃣ 8-cylinder": 20},
    "🚙 SUV": {"4️⃣ 4-cylinder": 25, "6️⃣ 6-cylinder": 22, "8️⃣ 8-cylinder": 18},
    "🛻 Pickup": {"4️⃣ 4-cylinder": 22, "6️⃣ 6-cylinder": 20, "8️⃣ 8-cylinder": 16},
    "🚐 Van": {"4️⃣ 4-cylinder": 24, "6️⃣ 6-cylinder": 20, "8️⃣ 8-cylinder": 17}
}

# Section 1: 🚘 Vehicle Details
st.subheader("🚘 Vehicle Details")
col1, col2, col3, col4 = st.columns(4)

with col1:
    vehicle_type = st.selectbox("Vehicle Type", list(MPG_DATA.keys()))

with col2:
    engine_options = list(MPG_DATA[vehicle_type].keys())
    engine_type = st.selectbox("Engine Type", engine_options)

with col3:
    fuel_type = st.selectbox("Fuel Type", ["Gas ⛽", "Hybrid ♻️", "Electric 🔋"])

with col4:
    default_mpg = MPG_DATA[vehicle_type][engine_type]
    st.markdown(f"**Default MPG:** {default_mpg}")

# MPG Override and Fuel Price
col5, col6 = st.columns(2)
with col5:
    override_mpg = st.number_input("Override MPG (optional)", min_value=5, max_value=50, value=default_mpg, help="Leave as default or customize")
    actual_mpg = override_mpg

with col6:
    fuel_price = st.number_input("Fuel Price ($/gal)", min_value=0.50, max_value=10.00, value=3.50, step=0.01)

# Section 2: 📍 Location & Route
st.subheader("📍 Location & Route")
col7, col8, col9 = st.columns(3)

with col7:
    zip_code = st.text_input("Zip Code", placeholder="12345", help="For local fuel prices")

with col8:
    miles_driven = st.number_input("Miles Driven", min_value=0.0, step=0.1, help="Total miles for this trip")

with col9:
    stops = st.number_input("🛑 Stops", min_value=1, max_value=99, value=1, step=1)

# Section 3: 📦 Delivery Details
st.subheader("📦 Delivery Details")
col10, col11, col12 = st.columns(3)

with col10:
    include_shopping = st.checkbox("🛒 Include shopping")

with col11:
    if include_shopping:
        shopping_items = st.number_input("Shopping items", min_value=0, max_value=999, step=1)
    else:
        shopping_items = 0

with col12:
    if include_shopping:
        shopping_minutes = st.number_input("Shopping minutes", min_value=0, max_value=999, step=1)
    else:
        shopping_minutes = 0

# Section 4: ⏱️ Time & Earnings
st.subheader("⏱️ Time & Earnings")
col13, col14, col15 = st.columns(3)

with col13:
    trip_minutes = st.number_input("Trip minutes", min_value=1, max_value=999, value=30, step=1)

with col14:
    gross_pay = st.number_input("Gross Pay ($)", min_value=0.00, step=0.01, help="Total earnings before expenses")

with col15:
    tips = st.number_input("Tips ($)", min_value=0.00, step=0.01)

# Section 5: 🎯 Trip Quality & Scoring
st.subheader("🎯 Trip Quality")

# Auto-calculate trip quality based on earnings per hour
total_gross = gross_pay + tips
trip_hours = trip_minutes / 60
earnings_per_hour = total_gross / trip_hours if trip_hours > 0 else 0

# Auto-suggest trip quality
if earnings_per_hour >= 30:
    suggested_quality = "🏆 Great"
elif earnings_per_hour >= 25:
    suggested_quality = "👍 Good"
elif earnings_per_hour >= 20:
    suggested_quality = "😐 Fair"
elif earnings_per_hour >= 15:
    suggested_quality = "⚠️ Bad"
else:
    suggested_quality = "🗑️ Trash"

col16, col17, col18 = st.columns(3)
with col16:
    trip_quality = st.selectbox(
        "Trip Quality", 
        ["🗑️ Trash", "⚠️ Bad", "😐 Fair", "👍 Good", "🏆 Great"],
        index=["🗑️ Trash", "⚠️ Bad", "😐 Fair", "👍 Good", "🏆 Great"].index(suggested_quality),
        help=f"Auto-suggested: {suggested_quality} (${earnings_per_hour:.1f}/hr)"
    )

with col17:
    st.metric("Earnings/Hour", f"${earnings_per_hour:.2f}")

with col18:
    fuel_cost = (miles_driven / actual_mpg * fuel_price) if actual_mpg > 0 and miles_driven > 0 else 0
    net_pay = total_gross - fuel_cost
    st.metric("Net After Fuel", f"${net_pay:.2f}")

# Add Trip Button
if st.button("➕ Add Trip", type="primary"):
    trip_data = {
        'timestamp': datetime.now(),
        'vehicle_type': vehicle_type,
        'engine_type': engine_type,
        'fuel_type': fuel_type,
        'mpg': actual_mpg,
        'fuel_price': fuel_price,
        'zip_code': zip_code,
        'miles': miles_driven,
        'stops': stops,
        'shopping': include_shopping,
        'shopping_items': shopping_items,
        'shopping_minutes': shopping_minutes,
        'trip_minutes': trip_minutes,
        'gross_pay': gross_pay,
        'tips': tips,
        'total_gross': total_gross,
        'fuel_cost': fuel_cost,
        'net_pay': net_pay,
        'trip_quality': trip_quality,
        'earnings_per_hour': earnings_per_hour
    }
    
    st.session_state.trips.append(trip_data)
    st.success(f"Trip added! Quality: {trip_quality} | Net: ${net_pay:.2f}")

# Section 6: 📈 Summary & Analytics
if st.session_state.trips:
    st.subheader("📈 Summary & Analytics")
    
    # Convert trips to DataFrame
    df = pd.DataFrame(st.session_state.trips)
    df['date'] = df['timestamp'].dt.date
    df['week'] = df['timestamp'].dt.to_period('W')
    df['month'] = df['timestamp'].dt.to_period('M')
    df['year'] = df['timestamp'].dt.to_period('Y')
    
    # Period selection
    period = st.selectbox("View by Period", ["Daily", "Weekly", "Monthly", "Yearly"])
    
    # Group data by selected period
    if period == "Daily":
        grouped = df.groupby('date').agg({
            'total_gross': 'sum',
            'net_pay': 'sum',
            'trip_minutes': 'sum',
            'miles': 'sum'
        }).reset_index()
        x_col = 'date'
    elif period == "Weekly":
        grouped = df.groupby('week').agg({
            'total_gross': 'sum',
            'net_pay': 'sum',
            'trip_minutes': 'sum',
            'miles': 'sum'
        }).reset_index()
        grouped['week'] = grouped['week'].astype(str)
        x_col = 'week'
    elif period == "Monthly":
        grouped = df.groupby('month').agg({
            'total_gross': 'sum',
            'net_pay': 'sum',
            'trip_minutes': 'sum',
            'miles': 'sum'
        }).reset_index()
        grouped['month'] = grouped['month'].astype(str)
        x_col = 'month'
    else:  # Yearly
        grouped = df.groupby('year').agg({
            'total_gross': 'sum',
            'net_pay': 'sum',
            'trip_minutes': 'sum',
            'miles': 'sum'
        }).reset_index()
        grouped['year'] = grouped['year'].astype(str)
        x_col = 'year'
    
    # Create chart
    if not grouped.empty:
        fig = go.Figure()
        
        # Add gross earnings bars
        fig.add_trace(go.Bar(
            x=grouped[x_col],
            y=grouped['total_gross'],
            name='Gross Earnings',
            text=[f'${val:.2f}' for val in grouped['total_gross']],
            textposition='auto',
            marker_color='lightblue'
        ))
        
        # Add net earnings bars
        fig.add_trace(go.Bar(
            x=grouped[x_col],
            y=grouped['net_pay'],
            name='Net Earnings',
            text=[f'${val:.2f}' for val in grouped['net_pay']],
            textposition='auto',
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title=f"Earnings by {period}",
            xaxis_title=period,
            yaxis_title="Earnings ($)",
            showlegend=True,
            yaxis={'showticklabels': False}  # Hide y-axis ticks as requested
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bold totals under chart
        total_gross = df['total_gross'].sum()
        total_net = df['net_pay'].sum()
        
        col19, col20 = st.columns(2)
        with col19:
            st.markdown(f"**Gross Total: ${total_gross:.2f}**")
        with col20:
            st.markdown(f"**Net Total: ${total_net:.2f}**")

# Section 7: 📊 Export Options
st.subheader("📊 Export Options")
if st.session_state.trips:
    df_export = pd.DataFrame(st.session_state.trips)
    
    col21, col22, col23 = st.columns(3)
    
    with col21:
        csv_data = df_export.to_csv(index=False)
        st.download_button(
            label="📄 Export CSV",
            data=csv_data,
            file_name=f"spark_trips_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col22:
        # Convert to Excel bytes
        import io
        excel_buffer = io.BytesIO()
        df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📊 Export Excel",
            data=excel_data,
            file_name=f"spark_trips_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col23:
        if st.button("🗑️ Clear All Data"):
            st.session_state.trips = []
            st.rerun()

else:
    st.info("Add some trips to see analytics and export options!")

# Footer
st.markdown("---")
st.markdown("**🚀 Spark Driver Tracker** - Built for drivers, by drivers. Track every trip, maximize every dollar!")