import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="FED vs ECB Dashboard", layout="wide")

# === Load FED data ===
fed = pd.read_csv("fed.csv")
fed.columns = fed.columns.str.strip().str.replace('\ufeff', '')  # clean column names
fed["Date"] = pd.to_datetime(fed["Date"])
fed = fed.rename(columns={"Interest Rate": "Rate"})
fed = fed.dropna()
fed = fed.sort_values("Date")

# === Load ECB data ===
ecb = pd.read_csv("ecb.csv")
ecb.columns = ecb.columns.str.strip().str.replace('\ufeff', '')
ecb["Date"] = pd.to_datetime(ecb["Date"])
ecb = ecb.rename(columns={"Interest Rate": "Rate"})
ecb = ecb.dropna()
ecb = ecb.sort_values("Date")

# === App Title ===
st.title("📊 FED vs ECB Interest Rate Dashboard")

# === Date Selector ===
available_dates = pd.to_datetime(sorted(set(fed["Date"]).union(set(ecb["Date"]))))
selected_dates = st.multiselect(
    "📌 Select up to 4 specific dates to highlight",
    options=available_dates,
    default=[],
    help="Highlight FED and ECB interest rates on selected dates"
)

if len(selected_dates) > 4:
    st.warning("⚠️ You can only select up to 4 dates.")
    selected_dates = selected_dates[:4]

# === Plot Chart ===
fig = go.Figure()

# FED line
fig.add_trace(go.Scatter(
    x=fed["Date"], y=fed["Rate"],
    mode="lines", name="FED",
    line=dict(color="blue")
))

# ECB line
fig.add_trace(go.Scatter(
    x=ecb["Date"], y=ecb["Rate"],
    mode="lines", name="ECB",
    line=dict(color="orange")
))

# Highlight selected points
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

# Chart layout
fig.update_layout(
    title="📉 Interest Rate Trends: FED vs ECB",
    xaxis_title="Date",
    yaxis_title="Interest Rate (%)",
    hovermode="x unified",
    legend_title="Institution"
)

st.plotly_chart(fig, use_container_width=True)

# Optional: Display selected date comparison table
if selected_dates:
    st.subheader("📋 Selected Date Comparison")
    table_data = []
    for date in selected_dates:
        fed_val = fed.loc[fed["Date"] == date, "Rate"]
        ecb_val = ecb.loc[ecb["Date"] == date, "Rate"]
        table_data.append({
            "Date": date.date(),
            "FED Rate": fed_val.values[0] if not fed_val.empty else "—",
            "ECB Rate": ecb_val.values[0] if not ecb_val.empty else "—"
        })

    st.table(pd.DataFrame(table_data))
