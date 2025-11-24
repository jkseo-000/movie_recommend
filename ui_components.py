"""
UI 컴포넌트 렌더링 헬퍼 함수들
"""

import streamlit as st
from typing import Dict, List, Any, Tuple
from datetime import datetime
import data
import utils
import tmdb_client


def render_emotion_input() -> Dict[str, Any]:
    """
    감정 입력 UI를 렌더링하고 사용자 입력값을 반환합니다.
    
    Returns:
        {
            "text": str,
            "emoji": str,
            "happiness": int,
            "energy": int,
            "situation": str,
            "mode": str
        }
    """
    st.sidebar.header("🎭 감정 입력")
    
    # 텍스트 입력
    text_input = st.sidebar.text_area(
        "지금 기분을 자유롭게 적어보세요",
        height=100,
        placeholder="예: 오늘 하루가 힘들었어요...",
        key="emotion_text"
    )
    
    st.sidebar.markdown("---")
    
    # 이모지 선택
    st.sidebar.subheader("이모지로 표현하기")
    emoji_options = ["😂", "😢", "😡", "😴", "😱", "😌", "😍", "🤔", "😎", "🥺"]
    emoji = st.sidebar.radio(
        "지금 기분에 가장 가까운 이모지를 선택하세요",
        emoji_options,
        horizontal=True,
        key="emoji_selection"
    )
    
    st.sidebar.markdown("---")
    
    # 슬라이더
    st.sidebar.subheader("감정 수치")
    happiness = st.sidebar.slider(
        "행복도 (Happiness)",
        min_value=0,
        max_value=10,
        value=5,
        step=1,
        key="happiness_slider",
        help="0: 매우 슬픔, 10: 매우 행복"
    )
    
    energy = st.sidebar.slider(
        "에너지 (Energy)",
        min_value=0,
        max_value=10,
        value=5,
        step=1,
        key="energy_slider",
        help="0: 매우 피곤함, 10: 매우 활기찬"
    )
    
    st.sidebar.markdown("---")
    
    # 상황 선택
    st.sidebar.subheader("상황 선택")
    situation_options = [
        "퇴근길 지하철",
        "잠들기 전",
        "비 오는 날",
        "주말 아침 카페",
        "업무 중 집중 모드",
        "운동 중",
        "데이트",
        "여행 중"
    ]
    situation = st.sidebar.selectbox(
        "지금 어떤 상황인가요?",
        situation_options,
        key="situation_select"
    )
    
    st.sidebar.markdown("---")
    
    # 추천 타입은 영화만
    mode = "영화"
    mode_code = "movie"
    
    st.sidebar.markdown("---")
    
    # 분석 및 추천 실행 버튼
    analyze_button = st.sidebar.button(
        "🎯 분석 및 추천 실행",
        type="primary",
        use_container_width=True,
        key="analyze_button"
    )
    
    return {
        "text": text_input,
        "emoji": emoji,
        "happiness": happiness,
        "energy": energy,
        "situation": situation,
        "mode": mode_code,
        "mode_display": mode,
        "analyze_clicked": analyze_button
    }


def render_emotion_summary(emotion_profile: Dict[str, Any]) -> None:
    """
    감정 프로필 요약 카드를 렌더링합니다.
    """
    st.markdown("### 🎭 감정 분석 결과")
    
    # 카드 스타일
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
        ">
            <h3 style="margin-top: 0; color: white;">{emotion_profile['label']}</h3>
            <p style="font-size: 16px; margin-bottom: 10px;">{emotion_profile['summary']}</p>
            <div style="margin-top: 15px;">
                <strong>행복도:</strong> {emotion_profile['happiness']}/10 &nbsp;&nbsp;
                <strong>에너지:</strong> {emotion_profile['energy']}/10
            </div>
            <div style="margin-top: 10px;">
                {' '.join([f'<span style="background: rgba(255,255,255,0.3); padding: 5px 10px; border-radius: 15px; margin-right: 5px; display: inline-block;">#{tag}</span>' for tag in emotion_profile['tags'][:8]])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_single_recommendation(item: Dict[str, Any], idx: int) -> None:
    """
    단일 추천 아이템을 카드 형태로 렌더링합니다.
    
    Args:
        item: 추천 아이템 딕셔너리
        idx: 아이템 인덱스
    """
    item_id = item.get("id", f"item_{idx}")
    item_type = item.get("type", "movie")
    is_song = False  # 노래 기능 제거
    
    # 데이터 추출
    title = item.get("title", "제목 없음")
    image_url = item.get("image_url", "").strip()
    
    # 영화 포스터 가져오기
    if not image_url or image_url == "" or "placeholder" in image_url or not image_url.startswith("http"):
        tmdb_poster = tmdb_client.get_movie_poster_url(title)
        if tmdb_poster:
            image_url = tmdb_poster
        else:
            image_url = "https://via.placeholder.com/300x450?text=No+Image"
    
    artist_or_director = item.get("artist_or_director", "알 수 없음")
    genre = item.get("genre", "알 수 없음")
    description = item.get("description", "설명 없음")
    mood_tags = item.get("mood_tags", [])
    
    # 콘텐츠 타입 아이콘 (영화만)
    type_icon = "🎬"
    type_label = "MOVIE"
    
    # 카드 컨테이너
    with st.container():
        # 2열 레이아웃: 이미지 왼쪽, 콘텐츠 오른쪽
        col_img, col_content = st.columns([1, 2])
        
        # 왼쪽 컬럼: 이미지
        with col_img:
            # 콘텐츠 타입 표시
            st.markdown(f"**[{type_label}]**")
            
            # 이미지 표시
            try:
                st.image(
                    image_url,
                    use_container_width=True,
                    output_format="auto"
                )
            except Exception:
                # 이미지 로드 실패 시 placeholder
                st.image(
                    "https://via.placeholder.com/300x300?text=No+Image",
                    use_container_width=True
                )
        
        # 오른쪽 컬럼: 콘텐츠 정보
        with col_content:
            # 제목 영역 (아이콘 포함)
            st.markdown(f"### {type_icon} {title}")
            
            # 보조 정보 (감독)
            st.caption(f"감독: {artist_or_director}")
            
            st.markdown("")  # 여백
            
            # 장르 및 태그 영역 (배지 스타일)
            # 장르는 코드 블록 스타일, mood_tags는 해시태그 스타일
            genre_badge = f"`{genre}`"
            tags_display = " ".join([f"**#{tag}**" for tag in mood_tags[:6]]) if mood_tags else ""
            
            if tags_display:
                st.markdown(f"{genre_badge}  {tags_display}")
            else:
                st.markdown(genre_badge)
            
            st.markdown("")  # 여백
            
            # 설명
            st.markdown(description)
            
            st.markdown("")  # 여백
            
            # 관련 작품 표시 (같은 감독의 다른 영화 또는 유사한 영화)
            tmdb_id = item.get("tmdb_id")
            
            if tmdb_id:
                # TMDB 영화인 경우
                import tmdb_client
                
                # 같은 감독의 다른 영화 가져오기
                director_id = tmdb_client.get_director_id_from_movie(tmdb_id)
                director_movies = []
                if director_id:
                    director_movies = tmdb_client.get_movies_by_director_id(
                        director_id=director_id,
                        exclude_movie_id=tmdb_id,
                        limit=3
                    )
                
                # 유사한 영화 가져오기
                similar_movies = tmdb_client.get_similar_movies(
                    movie_id=tmdb_id,
                    limit=3
                )
                
                # 같은 감독의 다른 영화 표시
                if director_movies:
                    st.markdown("**🎬 같은 감독의 다른 영화**")
                    for related_item in director_movies:
                        related_title = related_item.get("title", "제목 없음")
                        related_year = related_item.get("release_date", "")[:4] if related_item.get("release_date") else ""
                        year_text = f" ({related_year})" if related_year else ""
                        st.markdown(f"- {related_title}{year_text}")
                
                # 유사한 영화 표시
                if similar_movies:
                    st.markdown("**🎭 유사한 영화**")
                    for similar_item in similar_movies:
                        similar_title = similar_item.get("title", "제목 없음")
                        similar_year = similar_item.get("release_date", "")[:4] if similar_item.get("release_date") else ""
                        year_text = f" ({similar_year})" if similar_year else ""
                        st.markdown(f"- {similar_title}{year_text}")
            else:
                # 더미 데이터인 경우 기존 로직 사용
                related_items = data.get_movies_by_director(artist_or_director, exclude_id=item_id)
                if related_items:
                    st.markdown("**🎬 같은 감독의 다른 영화**")
                    for related_item in related_items[:3]:  # 최대 3개만 표시
                        related_title = related_item.get("title", "제목 없음")
                        st.markdown(f"- {related_title}")
            
            st.markdown("")  # 여백
            
            # 버튼 영역 (카드 하단)
            st.caption("이 추천이 어땠는지 알려주세요 👇")
            
            col_like, col_dislike = st.columns(2)
            
            with col_like:
                like_key = f"like_{item_id}"
                if st.button("👍 마음에 들어요", key=like_key, use_container_width=True):
                    if "feedback" not in st.session_state:
                        st.session_state["feedback"] = {}
                    st.session_state["feedback"][item_id] = "like"
                    
                    # 좋아한 영화 목록에 추가 (중복 방지)
                    if "liked_movies" not in st.session_state:
                        st.session_state["liked_movies"] = []
                    
                    # 이미 추가된 영화인지 확인
                    movie_already_liked = any(
                        liked_movie.get("id") == item_id 
                        for liked_movie in st.session_state["liked_movies"]
                    )
                    
                    if not movie_already_liked:
                        # 영화 정보 복사하여 저장
                        movie_copy = item.copy()
                        movie_copy["liked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state["liked_movies"].append(movie_copy)
                    
                    st.rerun()
            
            with col_dislike:
                dislike_key = f"dislike_{item_id}"
                if st.button("👎 별로예요", key=dislike_key, use_container_width=True):
                    if "feedback" not in st.session_state:
                        st.session_state["feedback"] = {}
                    st.session_state["feedback"][item_id] = "dislike"
                    st.rerun()
            
            # 피드백 표시
            if "feedback" in st.session_state and item_id in st.session_state["feedback"]:
                feedback = st.session_state["feedback"][item_id]
                if feedback == "like":
                    st.success("👍 마음에 들어요로 표시되었습니다!")
                elif feedback == "dislike":
                    st.info("👎 별로예요로 표시되었습니다.")


def render_recommendation_list(
    recommendations: List[Dict[str, Any]],
    mode_display: str
) -> None:
    """
    추천 리스트를 카드 형태로 렌더링합니다.
    각 아이템은 render_single_recommendation 함수를 통해 렌더링됩니다.
    
    Args:
        recommendations: 추천 아이템 리스트
        mode_display: 추천 타입 표시 문자열 (예: "영화")
    """
    if not recommendations:
        st.warning("추천할 콘텐츠가 없습니다.")
        return
    
    # 헤더와 새로 추천 받기 버튼
    col_header, col_button = st.columns([3, 1])
    
    with col_header:
        st.markdown(f"### 🎬 추천 {mode_display}")
        st.caption(f"총 {len(recommendations)}개의 콘텐츠를 추천합니다.")
    
    with col_button:
        st.markdown("")  # 정렬을 위한 여백
        if st.button("🔄 새로 추천 받기", use_container_width=True, type="primary", key="refresh_recommendations"):
            # 같은 감정 프로필로 다시 추천 받기 (현재 추천된 영화 제외)
            if "current_emotion_profile" in st.session_state and "current_mode" in st.session_state:
                emotion_profile = st.session_state["current_emotion_profile"]
                current_mode = st.session_state["current_mode"]
                
                # 현재 추천된 영화의 ID 목록 가져오기 (제외용)
                excluded_movie_ids = []
                if "current_recommendations" in st.session_state:
                    for item in st.session_state["current_recommendations"]:
                        tmdb_id = item.get("tmdb_id")
                        if tmdb_id:
                            excluded_movie_ids.append(tmdb_id)
                
                # 다시 추천 받기
                import logic
                new_recommendations = logic.recommend_content(
                    emotion_profile=emotion_profile,
                    mode=current_mode,
                    n_items=5,
                    excluded_movie_ids=excluded_movie_ids
                )
                
                # 세션 상태 업데이트 (명시적으로 업데이트)
                if new_recommendations:
                    st.session_state["current_recommendations"] = new_recommendations
                    # 플래그 설정하여 app.py에서 재생성하지 않도록 함
                    st.session_state["refresh_clicked"] = True
                    st.rerun()
                else:
                    st.warning("새로운 추천을 가져올 수 없습니다. 잠시 후 다시 시도해주세요.")
            else:
                st.warning("감정 프로필이 없습니다. 먼저 감정을 입력해주세요.")
    
    st.markdown("")  # 여백
    
    # 세션 상태 초기화
    if "feedback" not in st.session_state:
        st.session_state["feedback"] = {}
    
    # 각 추천 아이템을 카드로 표시
    for idx, item in enumerate(recommendations):
        render_single_recommendation(item, idx)
        
        # 카드 간 구분선 (마지막 아이템이 아닌 경우)
        if idx < len(recommendations) - 1:
            st.markdown("---")
            st.markdown("")  # 여백


def render_feedback_summary() -> None:
    """
    피드백 통계를 요약하여 표시합니다.
    """
    if "feedback" not in st.session_state or not st.session_state["feedback"]:
        return
    
    st.markdown("### 📊 My Vibe Stats")
    
    feedback_data = st.session_state["feedback"]
    likes = [k for k, v in feedback_data.items() if v == "like"]
    dislikes = [k for k, v in feedback_data.items() if v == "dislike"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("총 피드백", len(feedback_data))
    
    with col2:
        st.metric("👍 마음에 들어요", len(likes))
    
    with col3:
        st.metric("👎 별로예요", len(dislikes))
    
    # 장르별 선호도 분석 (간단한 버전)
    if likes:
        st.markdown("#### 선호하는 콘텐츠")
        st.info(f"총 {len(likes)}개의 콘텐츠를 좋아하셨습니다!")


def render_liked_movies_page() -> None:
    """
    좋아한 영화 목록 페이지를 렌더링합니다.
    """
    st.title("❤️ 내가 좋아한 영화")
    
    liked_movies = st.session_state.get("liked_movies", [])
    
    if not liked_movies:
        st.info("아직 좋아한 영화가 없습니다. 메인 페이지에서 영화를 추천받고 '👍 마음에 들어요'를 눌러보세요!")
        return
    
    st.markdown(f"**총 {len(liked_movies)}개의 영화를 좋아하셨습니다.**")
    st.markdown("---")
    
    # 좋아한 영화 목록 표시
    st.markdown("### 📋 좋아한 영화 목록")
    
    for idx, movie in enumerate(liked_movies):
        with st.container():
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                image_url = movie.get("image_url")
                if image_url and image_url != "https://via.placeholder.com/300x450?text=No+Image":
                    st.image(image_url, use_container_width=True)
                else:
                    # 포스터 URL 가져오기 시도
                    tmdb_id = movie.get("tmdb_id")
                    if tmdb_id:
                        poster_url = tmdb_client.get_movie_poster_url(movie.get("title", ""))
                        if poster_url:
                            st.image(poster_url, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
            
            with col_info:
                title = movie.get("title", "제목 없음")
                director = movie.get("artist_or_director", "알 수 없음")
                genre = movie.get("genre", "장르 없음")
                description = movie.get("description", "설명 없음")
                liked_at = movie.get("liked_at", "")
                
                st.markdown(f"### {title}")
                st.markdown(f"**감독:** {director}")
                st.markdown(f"**장르:** `{genre}`")
                if liked_at:
                    st.caption(f"좋아요 표시: {liked_at}")
                st.markdown(description[:200] + ("..." if len(description) > 200 else ""))
                
                # 좋아요 취소 버튼
                if st.button("❌ 좋아요 취소", key=f"unlike_{movie.get('id')}_{idx}"):
                    st.session_state["liked_movies"] = [
                        m for m in st.session_state["liked_movies"] 
                        if m.get("id") != movie.get("id")
                    ]
                    # 피드백도 업데이트
                    if "feedback" in st.session_state:
                        item_id = movie.get("id")
                        if item_id in st.session_state["feedback"]:
                            del st.session_state["feedback"][item_id]
                    st.rerun()
        
        if idx < len(liked_movies) - 1:
            st.markdown("---")
    
    st.markdown("---")
    
    # 유사한 영화 추천
    st.markdown("### 🎬 당신의 취향에 맞는 영화 추천")
    
    if st.button("🔄 추천 새로고침", key="refresh_similar_movies"):
        st.rerun()
    
    # 좋아한 영화들을 기반으로 유사한 영화 추천
    similar_recommendations = _get_similar_movies_from_liked(liked_movies)
    
    if similar_recommendations:
        st.markdown(f"**좋아하신 영화들을 기반으로 {len(similar_recommendations)}개의 영화를 추천합니다.**")
        st.markdown("")
        
        for idx, movie in enumerate(similar_recommendations):
            render_single_recommendation(movie, idx)
            if idx < len(similar_recommendations) - 1:
                st.markdown("---")
                st.markdown("")
    else:
        st.info("추천할 영화를 찾지 못했습니다. 더 많은 영화를 좋아요 표시해보세요!")


def _get_similar_movies_from_liked(liked_movies: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
    """
    좋아한 영화들을 기반으로 유사한 영화를 추천합니다.
    
    Args:
        liked_movies: 좋아한 영화 목록
        limit: 추천할 영화 개수
    
    Returns:
        추천 영화 리스트
    """
    if not liked_movies:
        return []
    
    # 좋아한 영화들의 TMDB ID 수집
    liked_tmdb_ids = []
    for movie in liked_movies:
        tmdb_id = movie.get("tmdb_id")
        if tmdb_id:
            liked_tmdb_ids.append(tmdb_id)
    
    if not liked_tmdb_ids:
        return []
    
    # 각 좋아한 영화의 유사 영화를 가져와서 종합
    all_similar_movies = []
    seen_movie_ids = set(liked_tmdb_ids)  # 이미 좋아한 영화는 제외
    
    for movie in liked_movies:
        tmdb_id = movie.get("tmdb_id")
        if not tmdb_id:
            continue
        
        # 유사한 영화 가져오기
        similar_movies = tmdb_client.get_similar_movies(tmdb_id, limit=10)
        
        for similar_movie in similar_movies:
            similar_tmdb_id = similar_movie.get("tmdb_id")
            if similar_tmdb_id and similar_tmdb_id not in seen_movie_ids:
                # 이미 추가된 영화인지 확인
                if not any(m.get("tmdb_id") == similar_tmdb_id for m in all_similar_movies):
                    all_similar_movies.append(similar_movie)
                    seen_movie_ids.add(similar_tmdb_id)
    
    # 장르 기반 추천도 추가 (좋아한 영화들의 장르를 종합)
    if all_similar_movies:
        # 장르별로 정렬하여 다양성 확보
        return all_similar_movies[:limit]
    
    # 유사 영화가 없으면 장르 기반으로 추천
    # 좋아한 영화들의 장르를 종합
    genres = {}
    for movie in liked_movies:
        genre = movie.get("genre", "")
        if genre:
            genre_parts = genre.split("/")
            for g in genre_parts:
                genres[g] = genres.get(g, 0) + 1
    
    # 가장 많이 좋아한 장르 찾기
    if genres:
        top_genre = max(genres.items(), key=lambda x: x[1])[0]
        
        # 장르 기반 감정 프로필 생성
        emotion_profile = {
            "label": f"{top_genre} 선호",
            "happiness": 6,
            "energy": 5,
            "tags": [top_genre, "추천"]
        }
        
        # TMDB에서 장르 기반 영화 가져오기
        try:
            import logic
            recommendations = logic.recommend_content(
                emotion_profile=emotion_profile,
                mode="movie",
                n_items=limit,
                excluded_movie_ids=liked_tmdb_ids
            )
            return recommendations
        except Exception:
            return []
    
    return []


def render_emotion_history(history: List[Dict[str, Any]]) -> None:
    """
    감정 히스토리를 차트로 표시합니다.
    """
    if not history or len(history) < 2:
        return
    
    st.markdown("### 📈 감정 변화 히스토리")
    
    # 최근 10개만 표시
    recent_history = history[-10:]
    
    # 데이터 준비
    timestamps = [f"#{i+1}" for i in range(len(recent_history))]
    happiness_values = [h["emotion_profile"]["happiness"] for h in recent_history]
    energy_values = [h["emotion_profile"]["energy"] for h in recent_history]
    
    # 차트 데이터
    import pandas as pd
    chart_data = pd.DataFrame({
        "행복도": happiness_values,
        "에너지": energy_values
    }, index=timestamps)
    
    st.line_chart(chart_data)
    
    # 최근 3개 감정 레이블 표시
    st.markdown("#### 최근 감정 기록")
    for i, record in enumerate(recent_history[-3:], 1):
        st.markdown(
            f"""
            **{i}.** {record['emotion_profile']['label']} 
            (행복도: {record['emotion_profile']['happiness']}, 
            에너지: {record['emotion_profile']['energy']})
            """
        )

