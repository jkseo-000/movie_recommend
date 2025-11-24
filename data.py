"""
더미 데이터셋: 노래와 영화 목록
"""

from typing import List, Dict, Any


# 노래 데이터 (20개 이상)
SONGS: List[Dict[str, Any]] = [
    {
        "id": "song_001",
        "title": "Spring Day",
        "artist_or_director": "BTS",
        "genre": "K-Pop",
        "mood_tags": ["위로", "감성", "잔잔함", "사색"],
        "energy": 3,
        "valence": 4,
        "description": "따뜻한 위로와 그리움을 담은 감성 발라드",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_002",
        "title": "Dynamite",
        "artist_or_director": "BTS",
        "genre": "K-Pop",
        "mood_tags": ["밝음", "에너지", "즐거움", "자신감"],
        "energy": 9,
        "valence": 9,
        "description": "신나는 디스코 팝으로 기분을 업시켜주는 곡",
        "image_url": "https://i.scdn.co/image/ab67616d0000b273f4a4bbf5b095c8ab3c19c6ea"
    },
    {
        "id": "song_003",
        "title": "Blinding Lights",
        "artist_or_director": "The Weeknd",
        "genre": "Pop",
        "mood_tags": ["에너지", "강렬함", "밤감성", "자신감"],
        "energy": 8,
        "valence": 6,
        "description": "강렬한 신스팝으로 에너지를 불어넣는 곡",
        "image_url": "https://i.scdn.co/image/ab67616d0000b27334dbde5d47a8ce6e26a8c1b0"
    },
    {
        "id": "song_004",
        "title": "Someone Like You",
        "artist_or_director": "Adele",
        "genre": "Pop Ballad",
        "mood_tags": ["감성", "위로", "슬픔", "잔잔함"],
        "energy": 2,
        "valence": 2,
        "description": "깊은 감성과 위로를 전하는 파워 발라드",
        "image_url": "https://i.scdn.co/image/ab67616d0000b273a919c463f2b5756fa0fe44a3"
    },
    {
        "id": "song_005",
        "title": "Shape of You",
        "artist_or_director": "Ed Sheeran",
        "genre": "Pop",
        "mood_tags": ["에너지", "로맨틱", "즐거움", "밝음"],
        "energy": 7,
        "valence": 8,
        "description": "경쾌한 비트와 로맨틱한 멜로디",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_006",
        "title": "비 오는 날 듣기 좋은",
        "artist_or_director": "볼빨간사춘기",
        "genre": "Indie Pop",
        "mood_tags": ["감성", "잔잔함", "사색", "편안함"],
        "energy": 3,
        "valence": 5,
        "description": "비 오는 날 듣기 좋은 감성 인디 팝",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_007",
        "title": "좋은 날",
        "artist_or_director": "IU",
        "genre": "K-Pop",
        "mood_tags": ["밝음", "즐거움", "에너지", "행복"],
        "energy": 6,
        "valence": 8,
        "description": "밝고 경쾌한 기분을 만들어주는 곡",
        "image_url": "https://i.scdn.co/image/ab67616d0000b273a68c7ceb0d3177f2f5f364a7"
    },
    {
        "id": "song_008",
        "title": "Stay",
        "artist_or_director": "The Kid LAROI & Justin Bieber",
        "genre": "Pop",
        "mood_tags": ["감성", "로맨틱", "에너지", "사색"],
        "energy": 6,
        "valence": 5,
        "description": "감성적인 멜로디와 현대적인 비트의 조화",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_009",
        "title": "좋아",
        "artist_or_director": "잔나비",
        "genre": "Rock",
        "mood_tags": ["에너지", "자신감", "강렬함", "밝음"],
        "energy": 8,
        "valence": 7,
        "description": "강렬한 록 사운드로 에너지를 불어넣는 곡",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_010",
        "title": "밤편지",
        "artist_or_director": "IU",
        "genre": "K-Pop Ballad",
        "mood_tags": ["잔잔함", "편안함", "사색", "밤감성"],
        "energy": 2,
        "valence": 6,
        "description": "잠들기 전 듣기 좋은 잔잔한 발라드",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_011",
        "title": "Watermelon Sugar",
        "artist_or_director": "Harry Styles",
        "genre": "Pop",
        "mood_tags": ["밝음", "에너지", "즐거움", "여름감성"],
        "energy": 7,
        "valence": 9,
        "description": "신나고 밝은 여름 감성 팝",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_012",
        "title": "All Too Well",
        "artist_or_director": "Taylor Swift",
        "genre": "Country Pop",
        "mood_tags": ["감성", "사색", "위로", "잔잔함"],
        "energy": 3,
        "valence": 3,
        "description": "깊은 감성과 서정적인 가사가 돋보이는 곡",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_013",
        "title": "좋은 밤 좋은 꿈",
        "artist_or_director": "로꼬",
        "genre": "Hip-Hop",
        "mood_tags": ["편안함", "잔잔함", "밤감성", "위로"],
        "energy": 4,
        "valence": 6,
        "description": "편안하게 잠들 수 있게 해주는 힙합 발라드",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_014",
        "title": "Bad Guy",
        "artist_or_director": "Billie Eilish",
        "genre": "Alternative Pop",
        "mood_tags": ["강렬함", "에너지", "자신감", "밤감성"],
        "energy": 7,
        "valence": 4,
        "description": "독특하고 강렬한 분위기의 얼터너티브 팝",
        "image_url": "https://i.scdn.co/image/ab67616d0000b27303b8933dcef7a99e423b449a"
    },
    {
        "id": "song_015",
        "title": "좋다고 말해",
        "artist_or_director": "볼빨간사춘기",
        "genre": "Indie Pop",
        "mood_tags": ["로맨틱", "따뜻함", "밝음", "행복"],
        "energy": 5,
        "valence": 8,
        "description": "따뜻하고 로맨틱한 감성을 담은 인디 팝",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_016",
        "title": "Levitating",
        "artist_or_director": "Dua Lipa",
        "genre": "Pop",
        "mood_tags": ["에너지", "즐거움", "밝음", "자신감"],
        "energy": 8,
        "valence": 8,
        "description": "신나는 디스코 팝으로 기분을 최고조로 올려주는 곡",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_017",
        "title": "Rain",
        "artist_or_director": "태연",
        "genre": "K-Pop Ballad",
        "mood_tags": ["감성", "위로", "잔잔함", "사색"],
        "energy": 2,
        "valence": 4,
        "description": "비 오는 날 듣기 좋은 감성 발라드",
        "image_url": "https://i.scdn.co/image/ab67616d0000b2734fb043195e8d07e72ed02241"
    },
    {
        "id": "song_018",
        "title": "좋아해줘",
        "artist_or_director": "청하",
        "genre": "K-Pop",
        "mood_tags": ["로맨틱", "밝음", "에너지", "행복"],
        "energy": 6,
        "valence": 8,
        "description": "밝고 경쾌한 로맨틱 팝",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_019",
        "title": "Circles",
        "artist_or_director": "Post Malone",
        "genre": "Pop Rock",
        "mood_tags": ["감성", "사색", "에너지", "밤감성"],
        "energy": 5,
        "valence": 5,
        "description": "감성적이면서도 에너지 있는 팝 록",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_020",
        "title": "좋은 날",
        "artist_or_director": "아이유",
        "genre": "K-Pop",
        "mood_tags": ["밝음", "즐거움", "에너지", "행복"],
        "energy": 7,
        "valence": 9,
        "description": "하루를 밝게 시작할 수 있게 해주는 곡",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_021",
        "title": "Midnight City",
        "artist_or_director": "M83",
        "genre": "Electronic",
        "mood_tags": ["밤감성", "에너지", "강렬함", "사색"],
        "energy": 7,
        "valence": 6,
        "description": "밤 도시의 분위기를 담은 일렉트로닉",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_022",
        "title": "좋아하는 사람이 생겼어요",
        "artist_or_director": "선미",
        "genre": "K-Pop",
        "mood_tags": ["로맨틱", "밝음", "행복", "즐거움"],
        "energy": 6,
        "valence": 8,
        "description": "사랑의 설렘을 담은 밝은 팝",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_023",
        "title": "Starboy",
        "artist_or_director": "The Weeknd",
        "genre": "R&B",
        "mood_tags": ["에너지", "자신감", "밤감성", "강렬함"],
        "energy": 8,
        "valence": 5,
        "description": "강렬한 에너지와 자신감을 주는 R&B",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_024",
        "title": "좋은 사람",
        "artist_or_director": "정승환",
        "genre": "Ballad",
        "mood_tags": ["위로", "감성", "잔잔함", "따뜻함"],
        "energy": 2,
        "valence": 6,
        "description": "따뜻한 위로를 전하는 감성 발라드",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    },
    {
        "id": "song_025",
        "title": "좋아",
        "artist_or_director": "윤하",
        "genre": "K-Pop",
        "mood_tags": ["로맨틱", "밝음", "행복", "에너지"],
        "energy": 5,
        "valence": 8,
        "description": "밝고 로맨틱한 감성을 담은 팝",
        "image_url": "https://via.placeholder.com/300x300?text=No+Image"
    }
]


# 영화 데이터 (15개 이상)
MOVIES: List[Dict[str, Any]] = [
    {
        "id": "movie_001",
        "title": "기생충",
        "artist_or_director": "봉준호",
        "genre": "스릴러/드라마",
        "mood_tags": ["긴장", "사색", "강렬함", "집중"],
        "energy": 7,
        "valence": 4,
        "description": "사회적 계급을 날카롭게 풍자한 스릴러",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_002",
        "title": "어바웃 타임",
        "artist_or_director": "리처드 커티스",
        "genre": "로맨스/코미디",
        "mood_tags": ["로맨틱", "따뜻함", "행복", "위로"],
        "energy": 5,
        "valence": 9,
        "description": "시간 여행을 통한 따뜻한 가족과 사랑 이야기",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_003",
        "title": "라라랜드",
        "artist_or_director": "데미안 셔젤",
        "genre": "뮤지컬/로맨스",
        "mood_tags": ["로맨틱", "감성", "밝음", "에너지"],
        "energy": 6,
        "valence": 7,
        "description": "꿈과 사랑을 그린 아름다운 뮤지컬",
        "image_url": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"
    },
    {
        "id": "movie_004",
        "title": "인터스텔라",
        "artist_or_director": "크리스토퍼 놀란",
        "genre": "SF/드라마",
        "mood_tags": ["사색", "감성", "집중", "강렬함"],
        "energy": 6,
        "valence": 5,
        "description": "우주를 배경으로 한 감동적인 아버지와 딸의 이야기",
        "image_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
    },
    {
        "id": "movie_005",
        "title": "위플래시",
        "artist_or_director": "데미안 셔젤",
        "genre": "드라마",
        "mood_tags": ["에너지", "강렬함", "집중", "동기부여"],
        "energy": 9,
        "valence": 6,
        "description": "음악에 대한 열정과 집착을 그린 강렬한 드라마",
        "image_url": "https://image.tmdb.org/t/p/w500/lIv1QinFqz4dlp5U4lQ6HaiskOZ.jpg"
    },
    {
        "id": "movie_006",
        "title": "레옹",
        "artist_or_director": "뤽 베송",
        "genre": "액션/드라마",
        "mood_tags": ["강렬함", "감성", "위로", "밤감성"],
        "energy": 7,
        "valence": 5,
        "description": "킬러와 소녀의 특별한 우정을 그린 액션 드라마",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_007",
        "title": "노트북",
        "artist_or_director": "닉 카사베티스",
        "genre": "로맨스/드라마",
        "mood_tags": ["로맨틱", "감성", "위로", "따뜻함"],
        "energy": 4,
        "valence": 7,
        "description": "시간을 초월한 영원한 사랑 이야기",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_008",
        "title": "인셉션",
        "artist_or_director": "크리스토퍼 놀란",
        "genre": "SF/스릴러",
        "mood_tags": ["집중", "사색", "강렬함", "긴장"],
        "energy": 8,
        "valence": 5,
        "description": "꿈 속 꿈을 다룬 복잡하고 강렬한 SF 스릴러",
        "image_url": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"
    },
    {
        "id": "movie_009",
        "title": "토이 스토리 4",
        "artist_or_director": "조시 쿨리",
        "genre": "애니메이션/코미디",
        "mood_tags": ["밝음", "즐거움", "행복", "위로"],
        "energy": 6,
        "valence": 9,
        "description": "따뜻하고 유쾌한 가족 애니메이션",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_010",
        "title": "헤어질 결심",
        "artist_or_director": "박찬욱",
        "genre": "로맨스/스릴러",
        "mood_tags": ["감성", "사색", "로맨틱", "밤감성"],
        "energy": 4,
        "valence": 4,
        "description": "아름답고 미묘한 감정을 그린 로맨틱 스릴러",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_011",
        "title": "위대한 쇼맨",
        "artist_or_director": "마이클 그레이시",
        "genre": "뮤지컬/드라마",
        "mood_tags": ["에너지", "밝음", "자신감", "동기부여"],
        "energy": 8,
        "valence": 8,
        "description": "꿈을 향한 열정을 담은 화려한 뮤지컬",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_012",
        "title": "파리, 텍사스",
        "artist_or_director": "빔 벤더스",
        "genre": "드라마",
        "mood_tags": ["사색", "감성", "잔잔함", "위로"],
        "energy": 2,
        "valence": 4,
        "description": "조용하고 깊이 있는 감성을 담은 드라마",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_013",
        "title": "어벤져스: 엔드게임",
        "artist_or_director": "루소 형제",
        "genre": "액션/SF",
        "mood_tags": ["에너지", "강렬함", "자신감", "동기부여"],
        "energy": 9,
        "valence": 7,
        "description": "강렬한 액션과 감동을 담은 슈퍼히어로 영화",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_014",
        "title": "이터널 선샤인",
        "artist_or_director": "미셸 공드리",
        "genre": "로맨스/드라마",
        "mood_tags": ["로맨틱", "감성", "사색", "위로"],
        "energy": 4,
        "valence": 6,
        "description": "기억을 지우는 과정을 통해 본 사랑의 의미",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_015",
        "title": "위대한 개츠비",
        "artist_or_director": "배즈 루어만",
        "genre": "로맨스/드라마",
        "mood_tags": ["로맨틱", "감성", "밤감성", "사색"],
        "energy": 5,
        "valence": 5,
        "description": "1920년대를 배경으로 한 화려하고 감성적인 로맨스",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_016",
        "title": "셰임",
        "artist_or_director": "스티브 맥퀸",
        "genre": "드라마",
        "mood_tags": ["감성", "사색", "잔잔함", "위로"],
        "energy": 3,
        "valence": 3,
        "description": "깊이 있는 감정과 인간관계를 그린 드라마",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_017",
        "title": "매트릭스",
        "artist_or_director": "워쇼스키 형제",
        "genre": "SF/액션",
        "mood_tags": ["강렬함", "집중", "사색", "에너지"],
        "energy": 8,
        "valence": 5,
        "description": "현실과 가상의 경계를 다룬 혁명적인 SF 액션",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    },
    {
        "id": "movie_018",
        "title": "업",
        "artist_or_director": "피트 닥터",
        "genre": "애니메이션/드라마",
        "mood_tags": ["따뜻함", "위로", "행복", "감성"],
        "energy": 5,
        "valence": 8,
        "description": "따뜻한 감동과 모험을 담은 픽사 애니메이션",
        "image_url": "https://via.placeholder.com/300x450?text=No+Image"
    }
]


def get_all_songs() -> List[Dict[str, Any]]:
    """모든 노래 데이터 반환"""
    return SONGS


def get_all_movies() -> List[Dict[str, Any]]:
    """모든 영화 데이터 반환"""
    return MOVIES


def get_song_by_id(song_id: str) -> Dict[str, Any] | None:
    """ID로 노래 찾기"""
    for song in SONGS:
        if song.get("id") == song_id:
            return song
    return None


def get_movie_by_id(movie_id: str) -> Dict[str, Any] | None:
    """ID로 영화 찾기"""
    for movie in MOVIES:
        if movie.get("id") == movie_id:
            return movie
    return None


def get_songs_by_artist(artist_name: str, exclude_id: str = None) -> List[Dict[str, Any]]:
    """
    아티스트 이름으로 노래 목록을 반환합니다 (현재 노래 제외).
    
    Args:
        artist_name: 아티스트 이름
        exclude_id: 제외할 노래 ID
    
    Returns:
        해당 아티스트의 다른 노래 리스트
    """
    result = []
    for song in SONGS:
        if song.get("artist_or_director") == artist_name:
            if exclude_id and song.get("id") == exclude_id:
                continue
            song_copy = song.copy()
            song_copy["type"] = "song"
            result.append(song_copy)
    return result


def get_movies_by_director(director_name: str, exclude_id: str = None) -> List[Dict[str, Any]]:
    """
    감독 이름으로 영화 목록을 반환합니다 (현재 영화 제외).
    
    Args:
        director_name: 감독 이름
        exclude_id: 제외할 영화 ID
    
    Returns:
        해당 감독의 다른 영화 리스트
    """
    result = []
    for movie in MOVIES:
        if movie.get("artist_or_director") == director_name:
            if exclude_id and movie.get("id") == exclude_id:
                continue
            movie_copy = movie.copy()
            movie_copy["type"] = "movie"
            result.append(movie_copy)
    return result

