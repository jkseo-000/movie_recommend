"""
TMDB API 클라이언트 모듈
감정 프로필에 따라 TMDB에서 영화를 가져옵니다.
"""

import os
import requests
from typing import Dict, List, Any, Optional
import streamlit as st

# TMDB API 기본 설정
TMDB_API_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_API_KEY = "e8493ed080934f8fca578cc289faf8bf"  # 하드코딩된 API 키 (환경변수 우선)


def get_tmdb_api_key() -> Optional[str]:
    """
    TMDB API 키를 가져옵니다.
    환경변수 TMDB_API_KEY를 우선 확인하고, 없으면 하드코딩된 키를 사용합니다.
    
    Returns:
        API 키 문자열 또는 None
    """
    api_key = os.environ.get("TMDB_API_KEY")
    if api_key:
        return api_key
    return TMDB_API_KEY if TMDB_API_KEY else None


def map_emotion_to_tmdb_genres(emotion_profile: Dict[str, Any]) -> List[int]:
    """
    감정 프로필을 TMDB 장르 ID로 매핑합니다.
    
    Args:
        emotion_profile: 감정 프로필 딕셔너리
    
    Returns:
        TMDB 장르 ID 리스트
    """
    tags = emotion_profile.get("tags", [])
    happiness = emotion_profile.get("happiness", 5)
    energy = emotion_profile.get("energy", 5)
    
    # TMDB 장르 ID 매핑
    # 28: Action, 12: Adventure, 16: Animation, 35: Comedy, 80: Crime,
    # 99: Documentary, 18: Drama, 10751: Family, 14: Fantasy, 36: History,
    # 27: Horror, 10402: Music, 9648: Mystery, 10749: Romance, 878: Science Fiction,
    # 10770: TV Movie, 53: Thriller, 10752: War, 37: Western
    
    genre_ids = []
    
    # 태그 기반 매핑
    if any(tag in ["에너지", "강렬함", "동기부여", "자신감"] for tag in tags):
        genre_ids.extend([28, 12, 35])  # Action, Adventure, Comedy
    
    if any(tag in ["로맨틱", "따뜻함", "행복"] for tag in tags):
        genre_ids.extend([10749, 18, 35])  # Romance, Drama, Comedy
    
    if any(tag in ["위로", "감성", "잔잔함", "사색"] for tag in tags):
        genre_ids.extend([18, 14, 10402])  # Drama, Fantasy, Music
    
    if any(tag in ["밤감성", "긴장", "집중"] for tag in tags):
        genre_ids.extend([53, 9648, 878])  # Thriller, Mystery, Sci-Fi
    
    if any(tag in ["밝음", "즐거움", "행복"] for tag in tags):
        genre_ids.extend([16, 35, 10751])  # Animation, Comedy, Family
    
    # 행복도와 에너지 기반 매핑
    if happiness >= 7 and energy >= 7:
        genre_ids.extend([35, 16, 12])  # Comedy, Animation, Adventure
    elif happiness <= 3 and energy <= 3:
        genre_ids.extend([18, 99, 36])  # Drama, Documentary, History
    elif energy >= 7:
        genre_ids.extend([28, 12, 53])  # Action, Adventure, Thriller
    
    # 중복 제거
    genre_ids = list(set(genre_ids))
    
    # 최소 1개 장르는 보장
    if not genre_ids:
        genre_ids = [18]  # 기본값: Drama
    
    return genre_ids[:3]  # 최대 3개 장르만 사용


def discover_movies_by_mood(
    emotion_profile: Dict[str, Any],
    n_items: int = 10,
    excluded_movie_ids: List[int] = None,
    page: int = 1
) -> List[Dict[str, Any]]:
    """
    TMDB의 /discover/movie 엔드포인트를 사용하여 감정 프로필에 맞는 영화를 가져옵니다.
    
    Args:
        emotion_profile: 감정 프로필 딕셔너리
        n_items: 가져올 영화 개수
        excluded_movie_ids: 제외할 영화 ID 리스트 (TMDB ID)
        page: TMDB API 페이지 번호 (다른 영화를 가져오기 위해 사용)
    
    Returns:
        정규화된 영화 딕셔너리 리스트
    """
    if excluded_movie_ids is None:
        excluded_movie_ids = []
    api_key = get_tmdb_api_key()
    if not api_key:
        return []
    
    try:
        # 감정 프로필을 TMDB 쿼리 파라미터로 변환
        genre_ids = map_emotion_to_tmdb_genres(emotion_profile)
        happiness = emotion_profile.get("happiness", 5)
        energy = emotion_profile.get("energy", 5)
        
        # 정렬 기준 결정
        if energy >= 7:
            sort_by = "popularity.desc"
        elif happiness >= 7:
            sort_by = "vote_average.desc"
        else:
            sort_by = "popularity.desc"
        
        # TMDB API 호출
        discover_url = f"{TMDB_API_BASE_URL}/discover/movie"
        params = {
            "api_key": api_key,
            "language": "ko-KR",
            "sort_by": sort_by,
            "with_genres": ",".join(map(str, genre_ids)),
            "vote_count.gte": 50,  # 최소 50개 이상의 평점
            "page": page  # 페이지 번호 사용 (새로운 영화를 위해)
        }
        
        response = requests.get(discover_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            movies = []
            for movie in results:
                # 제외할 영화는 건너뛰기
                movie_id = movie.get("id")
                if movie_id in excluded_movie_ids:
                    continue
                
                # 포스터 URL 생성
                poster_path = movie.get("poster_path")
                image_url = None
                if poster_path:
                    image_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                else:
                    image_url = "https://via.placeholder.com/300x450?text=No+Image"
                
                # 장르 이름 가져오기 (선택적)
                genre_names = []
                genre_ids_movie = movie.get("genre_ids", [])
                # 간단한 장르 이름 매핑
                genre_map = {
                    28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디",
                    80: "범죄", 99: "다큐멘터리", 18: "드라마", 10751: "가족",
                    14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
                    9648: "미스터리", 10749: "로맨스", 878: "SF", 53: "스릴러",
                    10752: "전쟁", 37: "서부"
                }
                for gid in genre_ids_movie[:2]:
                    if gid in genre_map:
                        genre_names.append(genre_map[gid])
                
                genre_str = "/".join(genre_names) if genre_names else "드라마"
                
                # 감정 태그 재사용
                mood_tags = emotion_profile.get("tags", [])[:4]
                
                # 에너지와 밸런스 계산
                vote_avg = movie.get("vote_average", 5.0)
                energy_score = min(10, max(0, int((vote_avg / 10) * 10)))
                valence_score = min(10, max(0, int((vote_avg / 10) * 10)))
                
                # 감독 정보 가져오기
                movie_id = movie.get("id")
                director_name = "알 수 없음"
                if movie_id:
                    director = get_movie_director(movie_id)
                    if director:
                        director_name = director
                
                movie_dict = {
                    "id": f"tmdb_{movie.get('id')}",
                    "title": movie.get("title", "제목 없음"),
                    "artist_or_director": director_name,
                    "genre": genre_str,
                    "mood_tags": mood_tags,
                    "energy": energy_score,
                    "valence": valence_score,
                    "description": movie.get("overview", "설명 없음")[:150] + ("..." if len(movie.get("overview", "")) > 150 else ""),
                    "image_url": image_url,
                    "release_date": movie.get("release_date", ""),
                    "original_language": movie.get("original_language", ""),
                    "tmdb_id": movie.get("id")
                }
                movies.append(movie_dict)
                
                # 원하는 개수만큼 모으면 중단
                if len(movies) >= n_items:
                    break
            
            return movies
        
        return []
        
    except Exception as e:
        # 에러 발생 시 빈 리스트 반환 (fallback을 위해)
        return []


def get_movie_director(movie_id: int) -> Optional[str]:
    """
    TMDB API를 사용하여 영화의 감독 이름을 가져옵니다.
    캐싱을 위해 session_state를 사용합니다.
    
    Args:
        movie_id: TMDB 영화 ID
    
    Returns:
        감독 이름 또는 None
    """
    # 세션 상태에 캐시가 있으면 반환
    cache_key = f"tmdb_director_{movie_id}"
    if "tmdb_cache" not in st.session_state:
        st.session_state["tmdb_cache"] = {}
    
    if cache_key in st.session_state["tmdb_cache"]:
        return st.session_state["tmdb_cache"][cache_key]
    
    api_key = get_tmdb_api_key()
    if not api_key:
        return None
    
    try:
        # TMDB API로 영화 credits 가져오기
        credits_url = f"{TMDB_API_BASE_URL}/movie/{movie_id}/credits"
        params = {
            "api_key": api_key,
            "language": "ko-KR"
        }
        
        response = requests.get(credits_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            crew = data.get("crew", [])
            
            # 감독 찾기
            for person in crew:
                if person.get("job") == "Director":
                    director_name = person.get("name", "알 수 없음")
                    # 캐시에 저장
                    st.session_state["tmdb_cache"][cache_key] = director_name
                    return director_name
        
        # 감독을 찾지 못한 경우
        st.session_state["tmdb_cache"][cache_key] = None
        return None
        
    except Exception:
        # 에러 발생 시 None 반환
        st.session_state["tmdb_cache"][cache_key] = None
        return None


def get_director_id_from_movie(movie_id: int) -> Optional[int]:
    """
    영화 ID로부터 감독의 TMDB person ID를 가져옵니다.
    
    Args:
        movie_id: TMDB 영화 ID
    
    Returns:
        감독의 person ID 또는 None
    """
    api_key = get_tmdb_api_key()
    if not api_key:
        return None
    
    try:
        credits_url = f"{TMDB_API_BASE_URL}/movie/{movie_id}/credits"
        params = {
            "api_key": api_key,
            "language": "ko-KR"
        }
        
        response = requests.get(credits_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            crew = data.get("crew", [])
            
            # 감독 찾기
            for person in crew:
                if person.get("job") == "Director":
                    return person.get("id")
        
        return None
        
    except Exception:
        return None


def get_similar_movies(movie_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """
    TMDB API를 사용하여 유사한 영화 목록을 가져옵니다.
    
    Args:
        movie_id: TMDB 영화 ID
        limit: 가져올 영화 개수
    
    Returns:
        영화 딕셔너리 리스트
    """
    api_key = get_tmdb_api_key()
    if not api_key:
        return []
    
    cache_key = f"tmdb_similar_{movie_id}"
    if "tmdb_cache" not in st.session_state:
        st.session_state["tmdb_cache"] = {}
    
    if cache_key in st.session_state["tmdb_cache"]:
        return st.session_state["tmdb_cache"][cache_key][:limit]
    
    try:
        similar_url = f"{TMDB_API_BASE_URL}/movie/{movie_id}/similar"
        params = {
            "api_key": api_key,
            "language": "ko-KR",
            "page": 1
        }
        
        response = requests.get(similar_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            movies = []
            for movie in results[:limit * 2]:  # 충분히 가져와서 필터링
                # 포스터 URL 생성
                poster_path = movie.get("poster_path")
                image_url = None
                if poster_path:
                    image_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                else:
                    image_url = "https://via.placeholder.com/300x450?text=No+Image"
                
                # 장르 이름 가져오기
                genre_names = []
                genre_ids_movie = movie.get("genre_ids", [])
                genre_map = {
                    28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디",
                    80: "범죄", 99: "다큐멘터리", 18: "드라마", 10751: "가족",
                    14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
                    9648: "미스터리", 10749: "로맨스", 878: "SF", 53: "스릴러",
                    10752: "전쟁", 37: "서부"
                }
                for gid in genre_ids_movie[:2]:
                    if gid in genre_map:
                        genre_names.append(genre_map[gid])
                
                genre_str = "/".join(genre_names) if genre_names else "드라마"
                
                # 감독 정보 가져오기
                similar_movie_id = movie.get("id")
                director_name = "알 수 없음"
                if similar_movie_id:
                    director = get_movie_director(similar_movie_id)
                    if director:
                        director_name = director
                
                movie_dict = {
                    "id": f"tmdb_{similar_movie_id}",
                    "title": movie.get("title", "제목 없음"),
                    "artist_or_director": director_name,
                    "genre": genre_str,
                    "mood_tags": [],
                    "energy": 5,
                    "valence": 5,
                    "description": movie.get("overview", "설명 없음")[:100] + ("..." if len(movie.get("overview", "")) > 100 else ""),
                    "image_url": image_url,
                    "tmdb_id": similar_movie_id
                }
                movies.append(movie_dict)
                
                if len(movies) >= limit:
                    break
            
            # 캐시에 저장
            st.session_state["tmdb_cache"][cache_key] = movies
            return movies[:limit]
        
        return []
        
    except Exception:
        return []


def get_movies_by_director_id(director_id: int, exclude_movie_id: int = None, limit: int = 5) -> List[Dict[str, Any]]:
    """
    감독 ID로 해당 감독의 다른 영화 목록을 가져옵니다.
    
    Args:
        director_id: TMDB 감독(person) ID
        exclude_movie_id: 제외할 영화 ID
        limit: 가져올 영화 개수
    
    Returns:
        영화 딕셔너리 리스트
    """
    api_key = get_tmdb_api_key()
    if not api_key:
        return []
    
    cache_key = f"tmdb_director_movies_{director_id}"
    if "tmdb_cache" not in st.session_state:
        st.session_state["tmdb_cache"] = {}
    
    if cache_key in st.session_state["tmdb_cache"]:
        cached = st.session_state["tmdb_cache"][cache_key]
        # 제외할 영화 필터링
        filtered = [m for m in cached if m.get("tmdb_id") != exclude_movie_id]
        return filtered[:limit]
    
    try:
        # 감독의 영화 목록 가져오기
        person_url = f"{TMDB_API_BASE_URL}/person/{director_id}/movie_credits"
        params = {
            "api_key": api_key,
            "language": "ko-KR"
        }
        
        response = requests.get(person_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            crew = data.get("crew", [])  # 감독이 만든 영화
            
            # 감독으로 만든 영화만 필터링
            directed_movies = [m for m in crew if m.get("job") == "Director"]
            
            # 감독 이름 가져오기
            director_name = "알 수 없음"
            if directed_movies:
                # person 정보에서 감독 이름 가져오기
                person_info_url = f"{TMDB_API_BASE_URL}/person/{director_id}"
                person_params = {
                    "api_key": api_key,
                    "language": "ko-KR"
                }
                person_response = requests.get(person_info_url, params=person_params, timeout=5)
                if person_response.status_code == 200:
                    person_data = person_response.json()
                    director_name = person_data.get("name", "알 수 없음")
            
            movies = []
            for movie in directed_movies[:limit * 2]:  # 충분히 가져와서 필터링
                # 제외할 영화는 건너뛰기
                movie_id = movie.get("id")
                if exclude_movie_id and movie_id == exclude_movie_id:
                    continue
                
                # 포스터 URL 생성
                poster_path = movie.get("poster_path")
                image_url = None
                if poster_path:
                    image_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                else:
                    image_url = "https://via.placeholder.com/300x450?text=No+Image"
                
                # 장르 정보 가져오기 (간단한 매핑)
                genre_ids_movie = movie.get("genre_ids", [])
                genre_map = {
                    28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디",
                    80: "범죄", 99: "다큐멘터리", 18: "드라마", 10751: "가족",
                    14: "판타지", 36: "역사", 27: "공포", 10402: "음악",
                    9648: "미스터리", 10749: "로맨스", 878: "SF", 53: "스릴러",
                    10752: "전쟁", 37: "서부"
                }
                genre_names = []
                for gid in genre_ids_movie[:2]:
                    if gid in genre_map:
                        genre_names.append(genre_map[gid])
                genre_str = "/".join(genre_names) if genre_names else "드라마"
                
                movie_dict = {
                    "id": f"tmdb_{movie_id}",
                    "title": movie.get("title", "제목 없음"),
                    "artist_or_director": director_name,
                    "genre": genre_str,
                    "mood_tags": [],
                    "energy": 5,
                    "valence": 5,
                    "description": movie.get("overview", "설명 없음")[:100] + ("..." if len(movie.get("overview", "")) > 100 else ""),
                    "image_url": image_url,
                    "release_date": movie.get("release_date", ""),
                    "tmdb_id": movie_id
                }
                movies.append(movie_dict)
                
                if len(movies) >= limit:
                    break
            
            # 캐시에 저장
            st.session_state["tmdb_cache"][cache_key] = movies
            return movies[:limit]
        
        return []
        
    except Exception:
        return []


def get_movie_poster_url(movie_title: str) -> Optional[str]:
    """
    영화 제목으로 포스터 URL을 가져옵니다.
    
    Args:
        movie_title: 영화 제목
    
    Returns:
        포스터 이미지 URL 또는 None
    """
    api_key = get_tmdb_api_key()
    if not api_key:
        return None
    
    try:
        search_url = f"{TMDB_API_BASE_URL}/search/movie"
        params = {
            "api_key": api_key,
            "query": movie_title,
            "language": "ko-KR"
        }
        
        response = requests.get(search_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                poster_path = results[0].get("poster_path")
                if poster_path:
                    return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
        
        return None
        
    except Exception:
        return None

