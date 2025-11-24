"""
공유 유틸리티 함수들
"""

from typing import Dict, List, Optional, Any
import requests
import streamlit as st


# 이모지 → 기본 감정 매핑
EMOJI_TO_EMOTION: Dict[str, Dict[str, any]] = {
    "😂": {"label": "행복", "happiness_bias": 2, "energy_bias": 1, "tags": ["즐거움", "웃음", "밝음"]},
    "😢": {"label": "슬픔", "happiness_bias": -3, "energy_bias": -2, "tags": ["위로", "감성", "잔잔함"]},
    "😡": {"label": "분노", "happiness_bias": -2, "energy_bias": 2, "tags": ["강렬함", "에너지", "해소"]},
    "😴": {"label": "피곤", "happiness_bias": -1, "energy_bias": -3, "tags": ["편안함", "잔잔함", "휴식"]},
    "😱": {"label": "불안", "happiness_bias": -2, "energy_bias": 1, "tags": ["긴장", "집중", "안정"]},
    "😌": {"label": "평온", "happiness_bias": 1, "energy_bias": 0, "tags": ["평온", "편안함", "잔잔함"]},
    "😍": {"label": "사랑", "happiness_bias": 3, "energy_bias": 1, "tags": ["로맨틱", "따뜻함", "감성"]},
    "🤔": {"label": "고민", "happiness_bias": -1, "energy_bias": -1, "tags": ["사색", "잔잔함", "위로"]},
    "😎": {"label": "자신감", "happiness_bias": 2, "energy_bias": 2, "tags": ["에너지", "자신감", "밝음"]},
    "🥺": {"label": "애잔함", "happiness_bias": -1, "energy_bias": -1, "tags": ["감성", "위로", "잔잔함"]},
}


# 상황 → 감정 바이어스 매핑
SITUATION_TO_BIAS: Dict[str, Dict[str, any]] = {
    "퇴근길 지하철": {"happiness_bias": -1, "energy_bias": -2, "tags": ["위로", "편안함", "하루의 마무리"]},
    "잠들기 전": {"happiness_bias": 0, "energy_bias": -3, "tags": ["편안함", "잔잔함", "휴식"]},
    "비 오는 날": {"happiness_bias": -1, "energy_bias": -1, "tags": ["감성", "사색", "잔잔함"]},
    "주말 아침 카페": {"happiness_bias": 2, "energy_bias": 1, "tags": ["편안함", "밝음", "여유"]},
    "업무 중 집중 모드": {"happiness_bias": 0, "energy_bias": 1, "tags": ["집중", "에너지", "동기부여"]},
    "운동 중": {"happiness_bias": 1, "energy_bias": 3, "tags": ["에너지", "강렬함", "동기부여"]},
    "데이트": {"happiness_bias": 3, "energy_bias": 1, "tags": ["로맨틱", "따뜻함", "행복"]},
    "여행 중": {"happiness_bias": 3, "energy_bias": 2, "tags": ["밝음", "에너지", "즐거움"]},
}


def get_emoji_emotion(emoji: str) -> Dict[str, any]:
    """이모지로부터 기본 감정 정보를 반환"""
    return EMOJI_TO_EMOTION.get(emoji, {"label": "중립", "happiness_bias": 0, "energy_bias": 0, "tags": []})


def get_situation_bias(situation: str) -> Dict[str, any]:
    """상황으로부터 감정 바이어스를 반환"""
    return SITUATION_TO_BIAS.get(situation, {"happiness_bias": 0, "energy_bias": 0, "tags": []})


def normalize_value(value: int, min_val: int = 0, max_val: int = 10) -> int:
    """값을 min_val과 max_val 사이로 정규화"""
    return max(min_val, min(max_val, value))


def calculate_emotion_score(item_tags: List[str], target_tags: List[str]) -> float:
    """아이템의 태그와 타겟 태그 간의 유사도 점수 계산"""
    if not item_tags or not target_tags:
        return 0.0
    
    common_tags = set(item_tags) & set(target_tags)
    return len(common_tags) / max(len(target_tags), 1)


def calculate_energy_match(item_energy: int, target_energy: int) -> float:
    """에너지 레벨 매칭 점수 계산 (차이가 작을수록 높은 점수)"""
    diff = abs(item_energy - target_energy)
    return max(0.0, 1.0 - (diff / 10.0))


def calculate_valence_match(item_valence: int, target_happiness: int) -> float:
    """밸런스(긍정성) 레벨 매칭 점수 계산"""
    diff = abs(item_valence - target_happiness)
    return max(0.0, 1.0 - (diff / 10.0))


# TMDB API 키
TMDB_API_KEY = "e8493ed080934f8fca578cc289faf8bf"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def get_movie_poster_url(movie_title: str) -> Optional[str]:
    """
    TMDB API를 사용하여 영화 포스터 URL을 가져옵니다.
    캐싱을 위해 session_state를 사용합니다.
    
    Args:
        movie_title: 영화 제목
    
    Returns:
        포스터 이미지 URL 또는 None
    """
    # 세션 상태에 캐시가 있으면 반환
    cache_key = f"tmdb_poster_{movie_title}"
    if "tmdb_cache" not in st.session_state:
        st.session_state["tmdb_cache"] = {}
    
    if cache_key in st.session_state["tmdb_cache"]:
        return st.session_state["tmdb_cache"][cache_key]
    
    try:
        # TMDB API로 영화 검색
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title,
            "language": "ko-KR"
        }
        
        response = requests.get(search_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                # 첫 번째 결과의 포스터 경로 가져오기
                poster_path = results[0].get("poster_path")
                if poster_path:
                    poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                    # 캐시에 저장
                    st.session_state["tmdb_cache"][cache_key] = poster_url
                    return poster_url
        
        # 검색 실패 시 None 반환
        st.session_state["tmdb_cache"][cache_key] = None
        return None
        
    except Exception as e:
        # 에러 발생 시 None 반환
        st.session_state["tmdb_cache"][cache_key] = None
        return None


def get_popular_movies_from_tmdb(limit: int = 20) -> List[Dict[str, Any]]:
    """
    TMDB API를 사용하여 인기 영화 목록을 가져옵니다.
    
    Args:
        limit: 가져올 영화 개수
    
    Returns:
        영화 딕셔너리 리스트 (id, title, artist_or_director, genre, mood_tags, energy, valence, description, image_url 포함)
    """
    cache_key = "tmdb_popular_movies"
    if "tmdb_cache" not in st.session_state:
        st.session_state["tmdb_cache"] = {}
    
    # 캐시가 있고 1시간 이내라면 캐시 사용 (선택적)
    if cache_key in st.session_state["tmdb_cache"]:
        cached_data = st.session_state["tmdb_cache"][cache_key]
        if cached_data:
            return cached_data[:limit]
    
    try:
        # TMDB API로 인기 영화 가져오기
        popular_url = f"{TMDB_BASE_URL}/movie/popular"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
            "page": 1
        }
        
        response = requests.get(popular_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            movies = []
            for movie in results[:limit]:
                # TMDB 영화 데이터를 우리 형식으로 변환
                poster_path = movie.get("poster_path", "")
                poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None
                
                # 장르는 기본값 사용 (TMDB 장르 ID를 변환하는 것은 복잡하므로)
                genre = "드라마"  # 기본값
                
                # 감정 태그는 영화의 인기도와 평점을 기반으로 추정
                vote_average = movie.get("vote_average", 5.0)
                popularity = movie.get("popularity", 0)
                
                if vote_average >= 7.5:
                    mood_tags = ["인기", "평점높음", "추천"]
                    energy = 6
                    valence = 7
                elif vote_average >= 6.5:
                    mood_tags = ["인기", "추천"]
                    energy = 5
                    valence = 6
                else:
                    mood_tags = ["다양함"]
                    energy = 4
                    valence = 5
                
                movie_dict = {
                    "id": f"tmdb_{movie.get('id')}",
                    "title": movie.get("title", "제목 없음"),
                    "artist_or_director": "TMDB 인기 영화",  # 감독 정보는 별도 API 호출 필요
                    "genre": genre,
                    "mood_tags": mood_tags,
                    "energy": energy,
                    "valence": valence,
                    "description": movie.get("overview", "설명 없음")[:100] + "...",
                    "image_url": poster_url or "https://via.placeholder.com/300x450?text=No+Image",
                    "tmdb_id": movie.get("id")
                }
                movies.append(movie_dict)
            
            # 캐시에 저장
            st.session_state["tmdb_cache"][cache_key] = movies
            return movies[:limit]
        
        return []
        
    except Exception as e:
        # 에러 발생 시 빈 리스트 반환
        return []

