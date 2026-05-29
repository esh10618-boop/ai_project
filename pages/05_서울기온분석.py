# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df = pd.read_csv('seoul.csv', encoding='euc-kr')

# 날짜 변환
df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')

# 날짜 오류 제거
df = df.dropna(subset=['날짜'])

# 연도, 월, 일 컬럼 생성
df['연도'] = df['날짜'].dt.year
df['월'] = df['날짜'].dt.month
df['일'] = df['날짜'].dt.day

# 제목
st.title("서울 날짜별 기온 분석")

# 월/일 선택
month = st.selectbox("월 선택", range(1, 13))
day = st.selectbox("일 선택", range(1, 32))

# 데이터 필터링
filtered = df[(df['월'] == month) & (df['일'] == day)]

# 결측치 제거
filtered = filtered.dropna(subset=['최고기온(℃)', '최저기온(℃)'])

# 그래프 생성
fig, ax = plt.subplots(figsize=(12, 6))

# 최고기온
ax.plot(
    filtered['연도'],
    filtered['최고기온(℃)'],
    color='hotpink',
    marker='o',
    label='최고기온'
)

# 최저기온
ax.plot(
    filtered['연도'],
    filtered['최저기온(℃)'],
    color='lightblue',
    marker='o',
    label='최저기온'
)

# 그래프 설정
ax.set_title(f"{month}월 {day}일 날짜별 기온분석")
ax.set_xlabel("연도")
ax.set_ylabel("온도(℃)")
ax.legend()
ax.grid(True)

# 출력
st.pyplot(fig)
