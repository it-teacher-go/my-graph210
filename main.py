import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 타이틀 및 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 다양한 변화를 탐색합니다.")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 문자열 변환 후 datetime으로 변경 (YYYYMMDD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 변환
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바: 데이터 요약 정보
with st.sidebar:
    st.header("📌 데이터 정보")
    st.info(f"총 {len(df):,}개의 일별 박스오피스 기록이 로드되었습니다.")
    st.markdown(f"- **기간**: {df['날짜'].min().strftime('%Y-%m-%d')} ~ {df['날짜'].max().strftime('%Y-%m-%d')}")
    st.markdown(f"- **포함 영화 수**: {df['영화명'].nunique():,}개")

# ==========================================
# [구역 1] 개별 영화의 일별 관객수 추이
# ==========================================
st.divider()
st.header("1. 영화별 일별 관객수 추이")

# 누적 관객수가 높은 순서대로 드롭다운 목록 정렬
top_movies = df.groupby('영화명')['일관객'].sum().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("영화를 선택하세요:", top_movies, index=0)

if selected_movie:
    # 선택한 영화 데이터 필터링
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

    # Plotly 선 그래프 생성
    fig = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"'{selected_movie}' 날짜별 일관객 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객수(명)'},
        markers=True
    )

    # 마우스 호버(Hover) 툴팁 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>",
        line=dict(width=2.5, color='#E50914')
    )

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객 수 (명)",
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # '이 그래프로 알 수 있는 것' 문구 작성 위치
    st.caption("💡 **이 그래프로 알 수 있는 것**")
    st.info("*(여기에 분석 문구를 직접 입력하세요)*")

# ==========================================
# [구역 2] 추후 그래프 추가 구역 (예시)
# ==========================================
# st.divider()
# st.header("2. 다음 분석 그래프 제목")
# ...
