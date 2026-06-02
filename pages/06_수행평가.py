from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="전국 호텔 조회",
    page_icon="🏨",
    layout="centered"
)

@st.cache_data
def load_data():
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "문화체육관광부_전국호텔현황_20230405.csv"
    )

    try:
        return pd.read_csv(csv_path, encoding="utf-8")
    except:
        return pd.read_csv(csv_path, encoding="cp949")


df = load_data()

st.title("🏨 전국 호텔 조회")
st.caption("지역과 등급을 선택해 호텔 정보를 확인하세요.")

regions = sorted(df["지역"].dropna().unique())
selected_region = st.selectbox("📍 지역 선택", regions)

grades = sorted(df["결정 등급"].dropna().unique())
selected_grade = st.selectbox("⭐ 등급 선택", grades)

filtered_df = df[
    (df["지역"] == selected_region)
    & (df["결정 등급"] == selected_grade)
]

st.divider()

if filtered_df.empty:
    st.warning("검색 결과가 없습니다.")

else:
    hotel_names = filtered_df["호텔명"].tolist()

    selected_hotel = st.selectbox(
        "🏨 호텔 선택",
        hotel_names
    )

    hotel = filtered_df[
        filtered_df["호텔명"] == selected_hotel
    ].iloc[0]

    st.subheader(hotel["호텔명"])

    st.write(f"📍 주소 : {hotel['주소']}")
    st.write(f"🛏️ 객실 수 : {hotel['객실수']}개")
    st.write(f"📞 전화번호 : {hotel['전화번호']}")

    homepage = str(hotel["홈페이지"])

    if homepage != "nan" and homepage.strip():

        if not homepage.startswith(("http://", "https://")):
            homepage = "https://" + homepage

        st.markdown(
            f"🌐 [호텔 홈페이지 방문하기]({homepage})"
        )

    st.markdown(
        f"📸 [호텔 사진 검색하기](https://www.google.com/search?tbm=isch&q={selected_hotel})"
    )
