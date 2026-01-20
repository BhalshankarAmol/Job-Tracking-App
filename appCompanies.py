import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# App setup
# -----------------------------
st.set_page_config(page_title="Job Tracking App", layout="wide")
st.title("💼 Job Tracking App")
st.markdown("Track your job applications, statuses, and follow-ups in one place.")

# -----------------------------
# Load dataset (CSV)
# -----------------------------
try:
    df = pd.read_csv("Companies_2026.csv")
except FileNotFoundError:
    st.error("❌ 'Companies_2026.csv' not found. Place it in the same folder as app.py.")
    st.stop()

# Normalize column names (strip spaces)
df.columns = [c.strip() for c in df.columns]

# -----------------------------
# Summary KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Companies", len(df))
with col2:
    st.metric("Applied", df[df["Status"] == "Applied"].shape[0])
with col3:
    st.metric("Pending", df[df["Status"] == "Pending"].shape[0])
with col4:
    st.metric("WFH Roles", df[df["WFH/WFO"] == "WFH"].shape[0])

st.divider()

# -----------------------------
# Charts
# -----------------------------
st.subheader("📊 Visual Insights")

colA, colB = st.columns(2)

with colA:
    status_count = df["Status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]
    fig1 = px.bar(
        status_count, x="Status", y="Count", color="Status",
        title="Applications by Status", text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    role_count = df["Roles"].value_counts().reset_index()
    role_count.columns = ["Role", "Count"]
    fig2 = px.pie(
        role_count, names="Role", values="Count",
        title="Roles Distribution (DA vs DS)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Packages histogram (keeps it simple—uses raw text values)
fig3 = px.histogram(
    df, x="Packages", color="Roles",
    title="Salary Packages Distribution"
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -----------------------------
# Interactive table (search)
# -----------------------------
st.subheader("🔍 Explore Companies")
search = st.text_input("Search by Company Name")
if search:
    filtered_df = df[df["Companies Name"].fillna("").str.contains(search, case=False)]
else:
    filtered_df = df.copy()

st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# Follow-up tracker
# -----------------------------
st.subheader("📅 Follow-up Status")
follow_cols = [
    "Companies Name", "Status",
    "Follow-up-1(24hrs)", "Follow-up-2(48hrs)", "Follow-up-3(100 HRS)"
]
# Show only columns that exist (prevents errors if headers change)
follow_cols = [c for c in follow_cols if c in df.columns]
st.dataframe(df[follow_cols], use_container_width=True)

st.success("✅ Dashboard loaded successfully! Use charts and search to track your job hunt.")
