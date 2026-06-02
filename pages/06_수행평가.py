import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="전국 호텔 조회",
    page_icon="🏨",
    layout="centered"
)

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv(
        "문화체육관광부_전국호텔현황_20230405.csv",
        encoding="utf-8"
    )
    return df

df = load_data()

# 제목
st.title("🏨 전국 호텔 조회")
st.caption("지역과 호텔 등급을 선택하면 호텔 정보를 확인할 수 있습니다.")

st.divider()

# 지역 선택
regions = sorted(df["지역"].dropna().unique())

selected_region = st.selectbox(
    "📍 지역 선택",
    regions
)

# 등급 선택
grades = sorted(df["결정 등급"].dropna().unique())

selected_grade = st.selectbox(
    "⭐ 호텔 등급 선택",
    grades
)

# 필터링
filtered_df = df[
    (df["지역"] == selected_region) &
    (df["결정 등급"] == selected_grade)
]

st.divider()

# 결과 표시
st.subheader("🔎 조회 결과")

if filtered_df.empty:
    st.warning("검색 결과가 없습니다.")
else:
    st.success(f"총 {len(filtered_df)}개 호텔이 검색되었습니다.")

    for _, row in filtered_df.iterrows():

        hotel_name = row.get("호텔명", "-")
        homepage = row.get("홈페이지", "")
        room_count = row.get("객실수", "-")
        phone = row.get("전화번호", "-")
        address = row.get("주소", "-")

        with st.container(border=True):

            st.markdown(f"### 🏨 {hotel_name}")

            st.write(f"📍 주소 : {address}")
            st.write(f"🛏️ 객실 수 : {room_count}개")
            st.write(f"📞 전화번호 : {phone}")

            if pd.notna(homepage) and str(homepage).strip():
                st.markdown(
                    f"🌐 [홈페이지 바로가기]({homepage})"
                )
            else:
                st.write("🌐 홈페이지 정보 없음")
