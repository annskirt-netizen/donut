import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # openDt 문자열 변환 및 genre 대표 장르 추출 (첫 번째 장르만 사용)
    df["openDt"] = df["openDt"].astype(str)
    df["genre"] = df["genre"].astype(str).str.split("|").str[0]

    return df


df = load_data()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 차트)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 빈도수 계산
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 비율",
    hover_data=["count"],
)

fig_donut.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}",
)

st.plotly_chart(fig_donut, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "박스오피스 상위권에 진입한 영화 중 특정 대표 장르가 차지하는 비중을 직관적으로 확인할 수 있습니다."
)
st.divider()

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 및 영화별 총 관객수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포 (트리맵)")

# Plotly 트리맵 생성 (계층 구조: 장르 -> 영화명, 크기: 총 관객수)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수",
    hover_data={"total_audi": ":,d"},
)

fig_treemap.update_traces(
    hovertemplate="<b>영화명:</b> %{label}<br><b>총 관객수:</b> %{value:,}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "각 장르 내에서 어떤 영화가 전체 관객수에서 큰 비중을 차지했는지 계층적으로 비교·알아볼 수 있습니다."
)
st.divider()

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객수 히스토그램
# -------------------------------------------------------------------
st.subheader("3. 총 관객수 분포 (히스토그램)")

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객수 분포",
    labels={"total_audi": "총 관객수"},
)

fig_hist.update_traces(
    hovertemplate="<b>관객수 구간:</b> %{x:,}명<br><b>영화 수:</b> %{y}편<extra></extra>"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 관객수가 많은 영화 정보 계산
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_title = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    f"대부분의 영화가 총 관객수 하위 구간에 집중되어 분포하며, "
    f"가장 관객이 많은 영화는 **'{top_movie_title}'** (총 {top_movie_audi:,}명)입니다."
)
st.divider()

# -------------------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수와 총 관객수의 관계 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

# Plotly 산점도 생성
fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",  # 장르별로 점 색상 구분
    hover_name="movieNm",  # 마우스를 올렸을 때 영화명 표시
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre": "장르",
    },
)

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "개봉 첫날 확보한 스크린수가 많을수록 최종 총 관객수도 증가하는 경향(양의 상관관계)이 있는지 파악할 수 있으며, 장르별 스크린 확보 규모와 흥행 성적의 관계를 알아볼 수 있습니다."
)
st.divider()

# -------------------------------------------------------------------
# 다섯 번째 그래프: 영화 10편 이상 장르의 총 관객수 상자 그림 (박스플롯)
# -------------------------------------------------------------------
st.subheader("5. 장르별 총 관객수 분포 비교 (박스플롯)")

# 영화가 10편 이상인 장르 필터링
genre_counts_series = df["genre"].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered_genres = df[df["genre"].isin(top_genres)]

# Plotly 박스플롯 생성 (points='outliers'로 이상치 표시, hover_name 설정)
fig_box = px.box(
    df_filtered_genres,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",  # 상자 밖 이상치 표시
    hover_name="movieNm",  # 마우스 오버 시 영화명 표시
    title="주요 장르별 총 관객수 분포 (영화 10편 이상 장르)",
    labels={"genre": "장르", "total_audi": "총 관객수"},
)

fig_box.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>총 관객수:</b> %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_box, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "영화 수가 일정 규모 이상인 장르 간 중앙값과 분포 범위를 비교할 수 있으며, 상자 밖의 점을 통해 흥행 대박을 터뜨린 아웃라이어(이상치) 영화들을 확인할 수 있습니다."
)
st.divider()

# -------------------------------------------------------------------
# 여섯 번째 그래프: 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린수 vs 총 관객수 (첫 주 관객수 크기 - 버블 차트)")

# Plotly 버블 차트 생성 (size="first_week_audi" 추가)
fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",  # 첫 주 관객수를 원 크기로 반영
    color="genre",
    hover_name="movieNm",
    size_max=40,  # 원의 최대 크기 조절
    title="개봉일 스크린수 vs 총 관객수 (원의 크기 = 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "첫 주 관객수",
        "genre": "장르",
    },
    custom_data=["first_week_audi"],
)

fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{customdata[0]:,}명<extra></extra>"
)

st.plotly_chart(fig_bubble, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "개봉일 스크린수와 총 관객수의 관계뿐만 아니라 원의 크기(첫 주 관객수)를 함께 봄으로써, 초반 흥행 기세가 최종 관객수로 어떻게 이어졌는지 3가지 차원의 요소를 동시에 비교·해석할 수 있습니다."
)
st.divider()

# -------------------------------------------------------------------
# 일곱 번째 그래프: 제작 국가별 - 장르별 영화 편수 (선버스트 차트)
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트)")

# 계층별 영화 편수 계산을 위한 카운트 열 추가
df_sunburst = df.copy()
df_sunburst["movie_count"] = 1

# Plotly 선버스트 생성 (계층 구조: nation -> genre, 크기: 영화 편수)
fig_sunburst = px.sunburst(
    df_sunburst,
    path=["nation", "genre"],
    values="movie_count",
    title="제작 국가별 장르 구성 비율 (칸 크기 = 영화 편수)",
    color="nation",
)

fig_sunburst.update_traces(
    hovertemplate="<b>구분:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>비율:</b> %{percentParent:.1%} (상위 항목 대비)<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "주요 제작 국가별로 어떤 장르의 영화가 주로 개봉하고 흥행했는지 제작 국가와 장르 간의 계층적 구성 비율을 시각적으로 파악할 수 있습니다."
)
st.divider()

# -------------------------------------------------------------------
# 여덟 번째 그래프: 박스오피스 롱런과 최종 관객수의 관계
# -------------------------------------------------------------------
st.subheader("8. 박스오피스 '롱런(Long-run)' 영화는 진정한 흥행 보증수표일까?")

# Plotly 산점도/버블차트 생성
fig_longrun = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    size="first_scrn",  # 원 크기로 개봉일 스크린수 반영
    size_max=30,
    hover_name="movieNm",
    title="박스오피스 '롱런(Long-run)' 영화는 진정한 흥행 보증수표일까?",
    labels={
        "days_in_top10": "10위권 진입 일수 (일)",
        "total_audi": "총 관객수",
        "genre": "장르",
        "first_scrn": "개봉일 스크린수",
    },
    custom_data=["first_scrn"],
)

fig_longrun.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>10위권 체류: %{x}일<br>총 관객수: %{y:,}명<br>개봉일 스크린수: %{customdata[0]:,}개<extra></extra>"
)

st.plotly_chart(fig_longrun, use_container_width=True)

# 시각화 해석 영역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.write(
    "10위권에 오래 머무른(days_in_top10이 큰) 영화일수록 대체로 총 관객수도 높은 강력한 양의 상관관계를 보이며, 초기 스크린수(점 크기)가 적었더라도 입소문으로 오랜 기간 상위권을 유지하며 대박을 터뜨린 실질적 롱런 흥행작을 식별할 수 있습니다."
)
st.divider()
