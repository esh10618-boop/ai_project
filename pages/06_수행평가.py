from pathlib import Path
import pandas as pd
import streamlit as st

# 페이지 설정

st.set_page_config(
page_title="전국 호텔 조회",
page_icon="🏨",
layout="centered"
)

# 데이터 불러오기

@st.cache_data
def load_data():

```
csv_path = (
    Path(__file__).resolve().parent.parent
    / "문화체육관광부_전국호텔현황_20230405.csv"
)

if not csv_path.exists():
    st.error(f"CSV 파일을 찾을 수 없습니다.\n{csv_path}")
    st.stop()

try:
    df = pd.read_csv(csv_path, encoding="utf-8")
except:
    df = pd.read_csv(csv_path, encoding="cp949")

return df
```

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
(df["지역"] == selected_region)
& (df["결정 등급"] == selected_grade)
]

st.divider()

st.subheader("🔎 검색 결과")

if filtered_df.empty:

```
st.warning("검색 결과가 없습니다.")
```

else:

```
st.success(f"총 {len(filtered_df)}개 호텔이 검색되었습니다.")

hotel_list = filtered_df["호텔명"].tolist()

selected_hotel = st.selectbox(
    "🏨 호텔 선택",
    hotel_list
)

hotel_info = filtered_df[
    filtered_df["호텔명"] == selected_hotel
].iloc[0]

st.markdown("### 🏨 " + str(hotel_info["호텔명"]))

st.write(f"📍 주소 : {hotel_info['주소']}")
st.write(f"🛏️ 객실 수 : {hotel_info['객실수']}개")
st.write(f"📞 전화번호 : {hotel_info['전화번호']}")

homepage = str(hotel_info["홈페이지"])

if homepage and homepage != "nan":

    if not homepage.startswith(("http://", "https://")):
        homepage = "https://" + homepage

    st.markdown(
        f"🌐 [호텔 홈페이지 방문하기]({homepage})"
    )

    st.markdown(
        f"📸 [호텔 사진 검색하기](https://www.google.com/search?tbm=isch&q={selected_hotel})"
    )

else:

    st.write("🌐 홈페이지 정보 없음")
    st.markdown(
        f"📸 [호텔 사진 검색하기](https://www.google.com/search?tbm=isch&q={selected_hotel})"
    )
```
