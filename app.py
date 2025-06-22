import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PASSWORD PROTECTION
# ---------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "msba":
            st.session_state["authenticated"] = True
        else:
            st.error("❌ Wrong password")
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.text_input("🔐 Enter password to access the dashboard:", type="password", on_change=password_entered, key="password")
        st.stop()

check_password()

# ---------------------------
# LOAD DATA
# ---------------------------
csv_url = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"

try:
    df = pd.read_csv(csv_url)
except Exception:
    st.error("❌ Failed to load data. Please check the CSV URL.")
    st.stop()

# ---------------------------
# DASHBOARD HEADER
# ---------------------------
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------
# FILTERS
# ---------------------------
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    selected_gender = st.selectbox("Select Gender", options=["All"] + sorted(df["Gender"].dropna().unique().tolist()))
with col_filter2:
    selected_year = st.selectbox("Select Year", options=["All"] + sorted(df["Year"].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]

# ---------------------------
# PREPARE DATA
# ---------------------------
gender_avg = filtered_df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = filtered_df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = filtered_df["Vehicle_Type"].value_counts()
age_gender_avg = filtered_df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# ---------------------------
# VISUALS (2x2 Dashboard)
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Avg Death & Injury by Gender**")
    fig1, ax1 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"])
    ax1.set_ylabel("Rate per 100k", fontsize=6)
    ax1.set_xlabel("")
    ax1.legend(fontsize=5, loc="upper right")
    ax1.tick_params(axis='x', labelsize=5)
    ax1.tick_params(axis='y', labelsize=5)
    fig1.tight_layout(pad=0.5)
    st.pyplot(fig1)

with col2:
    st.markdown("**2. Yearly Death & Injury Trends**")
    fig2, ax2 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='red', label="Death")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='blue', label="Injury")
    ax2.set_ylabel("Rate per 100k", fontsize=6)
    ax2.set_xlabel("Year", fontsize=6)
    ax2.tick_params(axis='x', labelsize=5)
    ax2.tick_params(axis='y', labelsize=5)
    ax2.legend(fontsize=5, loc="upper left")
    fig2.tight_layout(pad=0.5)
    st.pyplot(fig2)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**3. Vehicle Type Distribution**")
    fig3, ax3 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 5})
    ax3.axis('equal')
    st.pyplot(fig3)

with col4:
    st.markdown("**4. Age × Gender Injury/Death Rates**")
    fig4, ax4 = plt.subplots(figsize=(4.5, 3.0), dpi=120)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.6)
    ax4.set_ylabel("Rate per 100k", fontsize=6)
    ax4.set_xlabel("Age Group", fontsize=6)
    ax4.tick_params(axis='x', labelsize=5, rotation=30)
    ax4.tick_params(axis='y', labelsize=5)
    ax4.legend(fontsize=5, loc="center left", bbox_to_anchor=(1, 0.5))  # ✅ updated position
    fig4.tight_layout(pad=0.5)
    st.pyplot(fig4)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("<div style='text-align: center;'>© 2025 | Road Safety Analytics | MSBA Healthcare Analytics</div>", unsafe_allow_html=True)
