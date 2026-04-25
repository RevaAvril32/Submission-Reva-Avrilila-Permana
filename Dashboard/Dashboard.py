import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan data historis")


# Load Data
@st.cache_data
def load_data():
    day_url = "https://raw.githubusercontent.com/RevaAvril32/Bike-sharing-dataset-analisis/refs/heads/main/day.csv"
    hour_url = "https://raw.githubusercontent.com/RevaAvril32/Bike-sharing-dataset-analisis/refs/heads/main/hour.csv"
    
    day_df = pd.read_csv(
        day_url,
        sep=',',
        encoding='latin1',
        on_bad_lines='skip'
    )
    
    hour_df = pd.read_csv(
        hour_url,
        sep=',',
        encoding='latin1',
        on_bad_lines='skip'
    )
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

st.sidebar.header("🔍 Filter Data")

year = st.sidebar.selectbox(
    "Pilih Tahun",
    options=day_df['yr'].unique()
)

season = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

filtered_day = day_df[
    (day_df['yr'] == year) &
    (day_df['season'].isin(season))
]

filtered_hour = hour_df[hour_df['yr'] == year]


st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_day['cnt'].sum()))
col2.metric("Rata-rata Harian", round(filtered_day['cnt'].mean(), 2))
col3.metric("Max Rentals", int(filtered_day['cnt'].max()))

st.subheader("📈 Trend Penyewaan")

fig, ax = plt.subplots()
filtered_day.groupby('dteday')['cnt'].sum().plot(ax=ax)
st.pyplot(fig)

col4, col5 = st.columns(2)

with col4:
    st.subheader("🌤️ Penyewaan per Musim")
    fig, ax = plt.subplots()
    filtered_day.groupby('season')['cnt'].mean().plot(kind='bar', ax=ax)
    st.pyplot(fig)

with col5:
    st.subheader("🕒 Jam Sibuk")
    fig, ax = plt.subplots()
    filtered_hour.groupby('hr')['cnt'].mean().plot(ax=ax)
    st.pyplot(fig)

st.subheader("👥 Casual vs Registered")
st.bar_chart(filtered_day[['casual','registered']].sum())

st.markdown("---")
st.caption("Dashboard by You 🚀")

