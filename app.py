import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------- AUTHENTICATION ----------------------
PASSWORD = "msba"
st.title("Road Traffic Injury Analytics Dashboard")

password = st.text_input("Enter password:", type="password")
if password != PASSWORD:
    st.error("Incorrect password")
    st.stop()

# ---------------------- DATA LOADING ----------------------
DATA_URL = "https://raw.githubusercontent.com/sja47/road-traffic-injury-analytics/main/road_traffic_injuries_sample.csv"

try:
    df = pd.read_csv(DATA_URL)
except Exception as e:
    st.error(f"❌ Failed to load data. Error: {e}")
    st.stop()

# ---------------------- VISUALS ----------------------

st.markdown("### 1 & 2. Rates by Gender and Over Time")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Death & Injury Rates by Gender")
    gender_df = df.groupby('Gender')[['Death_Rate_per_100k', 'Injury_Rate_per_100k']].mean().reset_index()
    fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))
    ax1.bar(gender_df['Gender'], gender_df['Injury_Rate_per_100k'], label='Injury Rate', color='skyblue')
    ax1.bar(gender_df['Gender'], gender_df['Death_Rate_per_100k'], bottom=gender_df['Injury_Rate_per_100k'], label='Death Rate', color='navy')
    ax1.set_ylabel('Rate per 100k')
    ax1.legend()
    st.pyplot(fig1)

with col2:
    st.markdown("#### Death & Injury Rates Over Time")
    time_df = df.groupby('Year')[['Death_Rate_per_100k', 'Injury_Rate_per_100k']].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
    ax2.plot(time_df['Year'], time_df['Death_Rate_per_100k'], label='Death Rate', color='red', marker='o')
    ax2.plot(time_df['Year'], time_df['Injury_Rate_per_100k'], label='Injury Rate', color='blue', marker='o')
    ax2.set_ylabel('Rate per 100k')
    ax2.set_xlabel('Year')
    ax2.legend()
    st.pyplot(fig2)

st.markdown("### 3 & 4. Vehicle Type and Age × Gender")
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Vehicle Type Distribution")
    fig3, ax3 = plt.subplots(figsize=(3.5, 3.5))
    df['Vehicle_Type'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3)
    ax3.set_ylabel("")
    st.pyplot(fig3)

with col4:
    st.markdown("#### Death & Injury Rates by Age × Gender")
    age_gender_df = df.groupby(['Age_Group', 'Gender'])[['Death_Rate_per_100k', 'Injury_Rate_per_100k']].mean().unstack()
    fig4, ax4 = plt.subplots(figsize=(3.5, 3.5))
    age_gender_df.plot(kind='bar', ax=ax4, width=0.8)
    ax4.set_ylabel("Rate per 100k")
    ax4.legend(title='')
    st.pyplot(fig4)
