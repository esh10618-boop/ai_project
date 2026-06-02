import urllib.parse

# 결과 출력
st.subheader("🔎 검색 결과")

if filtered_df.empty:
    st.warning("검색 결과가 없습니다.")

else:

    st.success(f"총 {len(filtered_df)}개 호텔이 검색되었습니다.")

    for _, row in filtered_df.iterrows():

        hotel_name = str(row.get("호텔명", "-"))
        room_count = row.get("객실수", "-")
        phone = row.get("전화번호", "-")
        homepage = row.get("홈페이지", "")
        address = row.get("주소", "-")

        image_search_url = (
            "https://www.google.com/search?tbm=isch&q="
            + urllib.parse.quote(hotel_name)
        )

        with st.expander(f"🏨 {hotel_name}"):

            st.markdown(
                f"📸 **[호텔 사진 보기]({image_search_url})**"
            )

            st.write(f"📍 주소 : {address}")
            st.write(f"🛏️ 객실 수 : {room_count}개")
            st.write(f"📞 전화번호 : {phone}")

            if pd.notna(homepage) and str(homepage).strip():

                homepage = str(homepage).strip()

                if not homepage.startswith(("http://", "https://")):
                    homepage = "https://" + homepage

                st.markdown(
                    f"🌐 [호텔 홈페이지 방문하기]({homepage})"
                )

            else:
                st.write("🌐 홈페이지 정보 없음")
