import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PASSWORD PROTECTION
# ---------------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "MSBA":  # ← Change this
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
# TITLE
# ---------------------------
st.title("🚦 Road Traffic Injury Analytics Dashboard")

# ---------------------------
# CSV UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")
if uploaded_file is None:
    st.warning("Please upload a CSV file.")
    st.stop()

df = pd.read_csv(uploaded_file)

# ---------------------------
# ANALYTICS PREP
# ---------------------------
gender_avg = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
yearly_avg = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().reset_index()
vehicle_counts = df["Vehicle_Type"].value_counts()
age_gender_avg = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()

# ------------------ ROW 1 -------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("1. Avg Rates by Gender")
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    gender_avg.plot(x="Gender", kind="bar", stacked=True, ax=ax1, color=["skyblue", "blue"])
    ax1.set_ylabel("Rate per 100k")
    st.pyplot(fig1, use_container_width=True)

with row1_col2:
    st.subheader("2. Yearly Trends")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.plot(yearly_avg["Year"], yearly_avg["Death_Rate_per_100k"], marker='o', label="Death Rate")
    ax2.plot(yearly_avg["Year"], yearly_avg["Injury_Rate_per_100k"], marker='o', label="Injury Rate")
    ax2.legend()
    ax2.set_ylabel("Rate per 100k")
    st.pyplot(fig2, use_container_width=True)

# ------------------ ROW 2 -------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("3. Vehicle Type Distribution")
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=90)
    ax3.axis('equal')
    st.pyplot(fig3, use_container_width=True)

with row2_col2:
    st.subheader("4. Age × Gender Rates")
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    age_gender_avg.plot(kind="bar", ax=ax4)
    ax4.set_ylabel("Rate per 100k")
    st.pyplot(fig4, use_container_width=True)

# ---------------------------
# HIDE STREAMLIT DEFAULT UI
# ---------------------------
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
