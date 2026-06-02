from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "문화체육관광부_전국호텔현황_20230405.csv"
    )

    if not csv_path.exists():
        st.error(f"CSV 파일을 찾을 수 없습니다.\n{csv_path}")
        st.stop()

    return pd.read_csv(csv_path)

df = load_data()
