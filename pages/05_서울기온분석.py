# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# -----------------------------
# 데이터 불러오기
# -----------------------------
df = pd.read_csv("seoul.csv", encoding="euc-kr")

# 날짜 처리
df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
df = df.dropna(subset=['날짜'])

# 연/월/일 생성
df['연도'] = df['날짜'].dt.year
df['월'] = df['날짜'].dt.month
df['일'] = df['날짜'].dt.day

# 필요한 데이터 결측 제거
df = df.dropna(subset=['최고기온(℃)', '최저기온(℃)'])

# -----------------------------
# 제목
# -----------------------------
st.title("날짜별 기온분석")

# -----------------------------
# 사용자 입력
# -----------------------------
month = st.selectbox("월 선택", range(1, 13))
day = st.selectbox("일 선택", range(1, 32))

future_year = st.number_input(
    "예측할 미래 연도 입력",
    min_value=int(df['연도'].max()) + 1,
    value=int(df['연도'].max()) + 1
)

# -----------------------------
# 날짜 필터링
# -----------------------------
filtered = df[
    (df['월'] == month) &
    (df['일'] == day)
].copy()

# 데이터가 없는 경우
if filtered.empty:
    st.warning("선택한 날짜의 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 미래 예측 모델
# -----------------------------
X = filtered[['연도']]

# 최고기온 모델
y_max = filtered['최고기온(℃)']
model_max = LinearRegression()
model_max.fit(X, y_max)

pred_max = model_max.predict([[future_year]])[0]

# 최저기온 모델
y_min = filtered['최저기온(℃)']
model_min = LinearRegression()
model_min.fit(X, y_min)

pred_min = model_min.predict([[future_year]])[0]

# -----------------------------
# Plotly 그래프
# -----------------------------
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered['연도'],
        y=filtered['최고기온(℃)'],
        mode='lines+markers',
        name='최고기온',
        line=dict(color='hotpink'),
        marker=dict(size=7),
        hovertemplate=
        '연도: %{x}<br>' +
        '최고기온: %{y:.1f}℃<extra></extra>'
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered['연도'],
        y=filtered['최저기온(℃)'],
        mode='lines+markers',
        name='최저기온',
        line=dict(color='lightblue'),
        marker=dict(size=7),
        hovertemplate=
        '연도: %{x}<br>' +
        '최저기온: %{y:.1f}℃<extra></extra>'
    )
)

# 미래 최고기온 예측점
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode='markers',
        name='예측 최고기온',
        marker=dict(
            color='red',
            size=12,
            symbol='star'
        ),
        hovertemplate=
        '예측 연도: %{x}<br>' +
        '예측 최고기온: %{y:.1f}℃<extra></extra>'
    )
)

# 미래 최저기온 예측점
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode='markers',
        name='예측 최저기온',
        marker=dict(
            color='blue',
            size=12,
            symbol='star'
        ),
        hovertemplate=
        '예측 연도: %{x}<br>' +
        '예측 최저기온: %{y:.1f}℃<extra></extra>'
    )
)

# -----------------------------
# 그래프 설정
# -----------------------------
fig.update_layout(
    title=f"{month}월 {day}일 날짜별 기온분석",
    xaxis_title='연도',
    yaxis_title='온도(℃)',
    hovermode='x unified',
    legend_title='범례',
    height=600
)

# -----------------------------
# 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 예측 결과 출력
# -----------------------------
st.subheader(f"{future_year}년 예측 결과")

st.write(f"예상 최고기온: {pred_max:.2f}℃")
st.write(f"예상 최저기온: {pred_min:.2f}℃")
