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
# LOAD DATA FROM GITHUB
# ---------------------------
csv_url = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error("❌ Failed to load data. Please check the CSV URL.")
    st.stop()

# ---------------------------
# TITLE
# ---------------------------
st.markdown("<h1 style='text-align: center;'>🚦 Road Traffic Injury Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------
# FILTER WIDGETS
# ---------------------------
genders = df["Gender"].unique().tolist()
years = sorted(df["Year"].unique())

col_f1, col_f2 = st.columns(2)
with col_f1:
    selected_gender = st.selectbox("Select Gender", options=["All"] + genders)
with col_f2:
    selected_year = st.selectbox("Select Year", options=["All"] + years)

# Apply filters
filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

# ---------------------------
# AGGREGATE DATA
# ---------------------------
gender_avg = filtered_df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = filtered_df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = filtered_df["Vehicle_Type"].value_counts()
age_gender_avg = filtered_df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# ---------------------------
# DASHBOARD VISUALS (2x2)
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Avg Death & Injury by Gender**")
    fig1, ax1 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"])
    ax1.set_ylabel("Rate per 100k", fontsize=6)
    ax1.set_xlabel("")
    ax1.tick_params(axis='x', labelsize=5)
    ax1.tick_params(axis='y', labelsize=5)
    ax1.legend(["Injury", "Death"], fontsize=5, loc='center left', bbox_to_anchor=(1, 0.5))
    fig1.tight_layout(pad=0.2)
    st.pyplot(fig1, clear_figure=True)

with col2:
    st.markdown("**2. Yearly Death & Injury Trends**")
    fig2, ax2 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', color='red', label="Death")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', color='blue', label="Injury")
    ax2.set_ylabel("Rate per 100k", fontsize=6)
    ax2.set_xlabel("Year", fontsize=6)
    ax2.tick_params(axis='x', labelsize=5)
    ax2.tick_params(axis='y', labelsize=5)
    ax2.legend(fontsize=5, loc="center left", bbox_to_anchor=(1, 0.5))
    fig2.tight_layout(pad=0.2)
    st.pyplot(fig2, clear_figure=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**3. Vehicle Type Distribution**")
    fig3, ax3 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    wedges, texts, autotexts = ax3.pie(vehicle_counts, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors, textprops={'fontsize': 5})
    ax3.axis('equal')
    ax3.legend(vehicle_counts.index, fontsize=5, loc="center left", bbox_to_anchor=(1, 0.5))
    fig3.tight_layout(pad=0.2)
    st.pyplot(fig3, clear_figure=True)

with col4:
    st.markdown("**4. Age × Gender Injury/Death Rates**")
    fig4, ax4 = plt.subplots(figsize=(2.0, 1.8), dpi=120)
    age_gender_avg.plot(kind="bar", ax=ax4, width=0.7)
    ax4.set_ylabel("Rate per 100k", fontsize=6)
    ax4.set_xlabel("Age Group", fontsize=6)
    ax4.tick_params(axis='x', labelsize=5)
    ax4.tick_params(axis='y', labelsize=5)
    ax4.legend(fontsize=5, loc="center left", bbox_to_anchor=(1, 0.5))
    fig4.tight_layout(pad=0.2)
    st.pyplot(fig4, clear_figure=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("<div style='text-align: center; font-size: small;'>© 2025 | Road Safety Analytics | MSBA Healthcare Analytics</div>", unsafe_allow_html=True)
