import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# === Load FED data ===
fed = pd.read_csv("FEDFUNDS.csv", parse_dates=["DATE"])
fed = fed.rename(columns={"DATE": "Date", "FEDFUNDS": "Rate"})
fed = fed.dropna()
fed = fed.sort_values("Date")

# === Load ECB data ===
ecb = pd.read_csv("ECB Data Portal_20250512175431.csv", skiprows=5)
ecb = ecb.rename(columns={"TIME_PERIOD": "Date", "OBS_VALUE": "Rate"})
ecb["Date"] = pd.to_datetime(ecb["Date"], errors="coerce")
ecb["Rate"] = pd.to_numeric(ecb["Rate"], errors="coerce")
ecb = ecb.dropna()
ecb = ecb.sort_values("Date")

# 🖼️ App title
st.title("📊 FED vs ECB Interest Rate Dashboard")

# 📅 Date selector
available_dates = pd.to_datetime(sorted(set(fed["Date"]).union(set(ecb["Date"]))))
selected_dates = st.multiselect(
    "📌 Select up to 4 specific dates to highlight",
    options=available_dates,
    default=[],
    help="Select up to 4 dates to view exact interest rates"
)

if len(selected_dates) > 4:
    st.warning("⚠️ You can only select up to 4 dates.")
    selected_dates = selected_dates[:4]

# 📈 Line Chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=fed["Date"], y=fed["Rate"], name="FED",
    line=dict(color="blue")
))

fig.add_trace(go.Scatter(
    x=ecb["Date"], y=ecb["Rate"], name="ECB",
    line=dict(color="orange")
))

# 🔍 Highlight selected dates
for date in selected_dates:
    fed_point = fed.loc[fed["Date"] == date]
    ecb_point = ecb.loc[ecb["Date"] == date]

    if not fed_point.empty:
        fig.add_trace(go.Scatter(
            x=[date], y=[fed_point["Rate"].values[0]],
            mode="markers+text",
            marker=dict(size=10, color="blue"),
            text=[f"{fed_point['Rate'].values[0]:.2f}%"],
            textposition="top center",
            name=f"FED {date.date()}"
        ))

    if not ecb_point.empty:
        fig.add_trace(go.Scatter(
            x=[date], y=[ecb_point["Rate"].values[0]],
            mode="markers+text",
            marker=dict(size=10, color="orange"),
            text=[f"{ecb_point['Rate'].values[0]:.2f}%"],
            textposition="bottom center",
            name=f"ECB {date.date()}"
        ))

fig.update_layout(
    title="📉 Interest Rate Trends: FED vs ECB",
    xaxis_title="Date",
    yaxis_title="Interest Rate (%)",
    legend_title="Institution",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
