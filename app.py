import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- AUTHENTICATION ---
st.set_page_config(layout="wide")
PASSWORD = "msba"
password = st.text_input("Enter password:", type="password")
if password != PASSWORD:
    st.warning("Access Denied.")
    st.stop()

# --- LOAD DATA FROM GITHUB ---
csv_url = "https://raw.githubusercontent.com/your-username/your-repo/main/road_traffic_data.csv"  # replace this
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"❌ Failed to load data. Error: {e}")
    st.stop()

st.title("📊 Road Traffic Injury & Death Analysis (WHO)")

# --- 4 VISUALIZATIONS IN A 2x2 GRID ---
col1, col2 = st.columns(2)

# --- Chart 1: Avg Death & Injury Rates by Gender ---
with col1:
    st.markdown("### 1. Avg Death & Injury Rates by Gender")
    gender_group = df.groupby("Gender")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean()
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    gender_group.plot(kind="bar", stacked=True, ax=ax1, color=["skyblue", "navy"])
    ax1.set_ylabel("Rate per 100k")
    ax1.set_xlabel("Gender")
    ax1.legend(["Injury", "Death"], loc="upper right")
    st.pyplot(fig1)

# --- Chart 2: Trends over Years ---
with col2:
    st.markdown("### 2. Yearly Trends in Death & Injury Rates")
    year_group = df.groupby("Year")[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean()
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.plot(year_group.index, year_group["Death_Rate_per_100k"], label="Death Rate", color="red", marker="o")
    ax2.plot(year_group.index, year_group["Injury_Rate_per_100k"], label="Injury Rate", color="blue", marker="o")
    ax2.set_ylabel("Rate per 100k")
    ax2.set_xlabel("Year")
    ax2.legend(loc="upper right")
    st.pyplot(fig2)

col3, col4 = st.columns(2)

# --- Chart 3: Vehicle Type Distribution ---
with col3:
    st.markdown("### 3. Vehicle Type Distribution")
    vehicle_counts = df["Vehicle_Type"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.pie(vehicle_counts, labels=vehicle_counts.index, autopct='%1.1f%%', startangle=140)
    ax3.axis("equal")
    st.pyplot(fig3)

# --- Chart 4: Age × Gender Death & Injury ---
with col4:
    st.markdown("### 4. Death & Injury Rates by Age × Gender")
    grouped = df.groupby(["Age_Group", "Gender"])[["Death_Rate_per_100k", "Injury_Rate_per_100k"]].mean().unstack()
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    age_labels = grouped.index
    width = 0.2
    x = range(len(age_labels))
    
    ax4.bar([i - 1.5*width for i in x], grouped["Death_Rate_per_100k"]["Female"], width=width, label="Death Rate (F)", color='red')
    ax4.bar([i - 0.5*width for i in x], grouped["Death_Rate_per_100k"]["Male"], width=width, label="Death Rate (M)", color='green')
    ax4.bar([i + 0.5*width for i in x], grouped["Injury_Rate_per_100k"]["Female"], width=width, label="Injury Rate (F)", color='skyblue')
    ax4.bar([i + 1.5*width for i in x], grouped["Injury_Rate_per_100k"]["Male"], width=width, label="Injury Rate (M)", color='orange')

    ax4.set_xticks(list(x))
    ax4.set_xticklabels(age_labels, rotation=45, ha="right")
    ax4.set_ylabel("Rate per 100k")
    ax4.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig4)

