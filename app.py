import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------
# PASSWORD PROTECTION
# --------------------
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
        st.text_input("🔐 Enter password:", type="password", on_change=password_entered, key="password")
        st.stop()

check_password()

st.set_page_config(layout="wide")

# --------------------
# LOAD DATA
# --------------------
csv_url = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"
try:
    df = pd.read_csv(csv_url)
except:
    st.error("❌ Could not load CSV.")
    st.stop()

# --------------------
# PREPARE DATA
# --------------------
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = df["Vehicle_Type"].value_counts()
age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# --------------------
# HEADER
# --------------------
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

figsize = (3.2, 2.2)
fontsize = 7

# --------------------
# 2x2 DASHBOARD
# --------------------
col1, col2 = st.columns([1, 1])

# 1. Avg by Gender
with col1:
    st.subheader("1. Avg Death & Injury Rates by Gender")
    fig1, ax1 = plt.subplots(figsize=figsize)
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"], legend=False)
    ax1.set_ylabel("Rate per 100k", fontsize=fontsize)
    ax1.tick_params(labelsize=fontsize)
    st.pyplot(fig1)

# 2. Yearly Trends
with col2:
    st.subheader("2. Yearly Death & Injury Trends")
    fig2, ax2 = plt.subplots(figsize=figsize)
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='red', label="Death Rate")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='blue', label="Injury Rate")
    ax2.set_ylabel("Rate per 100k", fontsize=fontsize)
    ax2.set_xlabel("Year", fontsize=fontsize)
    ax2.tick_params(labelsize=fontsize)
    ax2.legend(fontsize=fontsize-1)
    st.pyplot(fig2)

col3, col4 = st.columns([1, 1])

# 3. Vehicle Pie
with col3:
    st.subheader("3. Vehicle Type Distribution")
    fig3, ax3 = plt.subplots(figsize=figsize)
    wedges, _, autotexts = ax3.pie(vehicle_counts, autopct='%1.0f%%', startangle=90, colors=plt.cm.Set3.colors, textprops={'fontsize': fontsize})
    ax3.axis('equal')
    ax3.legend(vehicle_counts.index, fontsize=fontsize-1, loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig3)

# 4. Age x Gender
with col4:
    st.subheader("4. Death & Injury by Age × Gender")
    fig4, ax4 = plt.subplots(figsize=figsize)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.7, legend=False)
    ax4.set_ylabel("Rate per 100k", fontsize=fontsize)
    ax4.set_xlabel("Age Group", fontsize=fontsize)
    ax4.tick_params(labelsize=fontsize)
    st.pyplot(fig4)
    st.caption("Legend: Colors represent combinations of Gender × Metric")

# --------------------
# FOOTER
# --------------------
st.markdown("---")
st.markdown("<div style='text-align: center;'>© 2025 | MSBA Healthcare Analytics</div>", unsafe_allow_html=True)
