"""
핵심 로직 함수들: 감정 분석, 콘텐츠 추천, 추천 이유 설명
"""

from typing import Dict, List, Any, Tuple
import data
import utils
import streamlit as st
import tmdb_client


def analyze_emotion(
    text_input: str,
    emoji: str,
    happiness: int,
    energy: int,
    situation: str
) -> Dict[str, Any]:
    """
    사용자 입력을 종합하여 감정 프로필을 분석합니다.
    
    Args:
        text_input: 자유 텍스트 입력
        emoji: 선택한 이모지
        happiness: 행복도 슬라이더 값 (0-10)
        energy: 에너지 슬라이더 값 (0-10)
        situation: 선택한 상황
    
    Returns:
        감정 프로필 딕셔너리:
        {
            "label": str,           # 감정 레이블
            "happiness": int,        # 최종 행복도 (0-10)
            "energy": int,           # 최종 에너지 (0-10)
            "tags": List[str],       # 감정 태그 리스트
            "summary": str           # 자연어 요약
        }
    
    TODO: 나중에 LLM이나 감정 분석 모델로 대체 가능하도록 구조화
    """
    # 이모지로부터 기본 감정 정보 가져오기
    emoji_emotion = utils.get_emoji_emotion(emoji)
    
    # 상황으로부터 바이어스 가져오기
    situation_bias = utils.get_situation_bias(situation)
    
    # 텍스트 입력에서 키워드 분석 (간단한 규칙 기반)
    text_tags = _extract_emotion_from_text(text_input)
    
    # 최종 행복도 계산 (이모지 바이어스 + 상황 바이어스 + 사용자 입력)
    final_happiness = happiness + emoji_emotion["happiness_bias"] + situation_bias["happiness_bias"]
    final_happiness = utils.normalize_value(final_happiness, 0, 10)
    
    # 최종 에너지 계산
    final_energy = energy + emoji_emotion["energy_bias"] + situation_bias["energy_bias"]
    final_energy = utils.normalize_value(final_energy, 0, 10)
    
    # 태그 통합
    all_tags = list(set(
        emoji_emotion["tags"] +
        situation_bias["tags"] +
        text_tags
    ))
    
    # 감정 레이블 생성
    emotion_label = _generate_emotion_label(
        emoji_emotion["label"],
        final_happiness,
        final_energy,
        text_input
    )
    
    # 자연어 요약 생성
    summary = _generate_emotion_summary(
        emotion_label,
        final_happiness,
        final_energy,
        all_tags,
        situation
    )
    
    return {
        "label": emotion_label,
        "happiness": final_happiness,
        "energy": final_energy,
        "tags": all_tags,
        "summary": summary
    }


def _extract_emotion_from_text(text: str) -> List[str]:
    """텍스트에서 감정 키워드를 추출 (간단한 규칙 기반)"""
    if not text:
        return []
    
    text_lower = text.lower()
    extracted_tags = []
    
    # 키워드 매핑
    keyword_mapping = {
        "슬프": ["슬픔", "위로", "감성"],
        "행복": ["행복", "밝음", "즐거움"],
        "피곤": ["피곤", "편안함", "휴식"],
        "화나": ["분노", "에너지", "해소"],
        "불안": ["불안", "긴장", "안정"],
        "평온": ["평온", "편안함", "잔잔함"],
        "사랑": ["로맨틱", "따뜻함", "행복"],
        "고민": ["사색", "위로", "잔잔함"],
        "자신감": ["자신감", "에너지", "밝음"],
        "위로": ["위로", "감성", "잔잔함"],
        "에너지": ["에너지", "강렬함", "동기부여"],
        "집중": ["집중", "에너지", "동기부여"],
        "밤": ["밤감성", "사색", "잔잔함"],
        "비": ["감성", "사색", "잔잔함"],
    }
    
    for keyword, tags in keyword_mapping.items():
        if keyword in text_lower:
            extracted_tags.extend(tags)
    
    return list(set(extracted_tags))


def _generate_emotion_label(
    emoji_label: str,
    happiness: int,
    energy: int,
    text_input: str
) -> str:
    """감정 레이블 생성"""
    # 행복도와 에너지에 따른 기본 레이블
    if happiness >= 7:
        base_label = "행복"
    elif happiness >= 4:
        base_label = "평온"
    elif happiness >= 2:
        base_label = "지침"
    else:
        base_label = "우울"
    
    # 에너지에 따른 수식어
    if energy >= 7:
        modifier = " + 높은 에너지"
    elif energy <= 3:
        modifier = " + 낮은 에너지"
    else:
        modifier = ""
    
    # 이모지 레이블과 결합
    if emoji_label != "중립":
        return f"{emoji_label} ({base_label}{modifier})"
    else:
        return f"{base_label}{modifier}"


def _generate_emotion_summary(
    label: str,
    happiness: int,
    energy: int,
    tags: List[str],
    situation: str
) -> str:
    """감정 프로필의 자연어 요약 생성"""
    tag_str = " ".join([f"#{tag}" for tag in tags[:5]])
    
    if happiness >= 7 and energy >= 7:
        mood_desc = "매우 밝고 활기찬 기분"
    elif happiness >= 7:
        mood_desc = "밝고 평온한 기분"
    elif happiness <= 3 and energy <= 3:
        mood_desc = "지치고 우울한 기분"
    elif energy >= 7:
        mood_desc = "에너지가 넘치는 기분"
    else:
        mood_desc = "차분하고 잔잔한 기분"
    
    return f"{situation}에 있는 당신은 {mood_desc}입니다. {tag_str}"


def recommend_content(
    emotion_profile: Dict[str, Any],
    mode: str,
    n_items: int = 5,
    excluded_movie_ids: List[int] = None
) -> List[Dict[str, Any]]:
    """
    감정 프로필을 기반으로 콘텐츠를 추천합니다.
    
    Args:
        emotion_profile: analyze_emotion()의 결과
        mode: "movie" (노래 기능 제거)
        n_items: 추천할 아이템 수
        excluded_movie_ids: 제외할 영화 ID 리스트 (TMDB ID)
    
    Returns:
        추천 아이템 리스트, 각 아이템은 원본 데이터 + "score" 필드를 포함
    """
    target_happiness = emotion_profile["happiness"]
    target_energy = emotion_profile["energy"]
    target_tags = emotion_profile["tags"]
    
    recommendations = []
    
    if excluded_movie_ids is None:
        excluded_movie_ids = []
    
    if mode == "movie" or mode == "both":
        # TMDB API를 사용하여 감정 프로필에 맞는 영화 가져오기
        tmdb_movies = []
        try:
            # 제외할 영화가 있으면 다른 페이지 사용 (새로운 영화를 위해)
            import random
            page = random.randint(1, 5) if excluded_movie_ids else 1
            
            tmdb_movies = tmdb_client.discover_movies_by_mood(
                emotion_profile=emotion_profile,
                n_items=50,  # 충분한 수의 영화를 가져와서 필터링
                excluded_movie_ids=excluded_movie_ids,
                page=page
            )
        except Exception:
            # TMDB API 호출 실패 시 빈 리스트
            tmdb_movies = []
        
        # 제외할 영화 필터링
        filtered_movies = []
        for movie in tmdb_movies:
            tmdb_id = movie.get("tmdb_id")
            if tmdb_id and tmdb_id not in excluded_movie_ids:
                filtered_movies.append(movie)
        
        # TMDB 영화가 있으면 사용, 없으면 기존 더미 데이터로 fallback
        if filtered_movies:
            for movie in filtered_movies:
                score = _calculate_recommendation_score(
                    movie, target_happiness, target_energy, target_tags
                )
                movie_copy = movie.copy()
                movie_copy["score"] = score
                movie_copy["type"] = "movie"
                recommendations.append(movie_copy)
        else:
            # Fallback: 기존 더미 영화 데이터 사용
            movies = data.get_all_movies()
            for movie in movies:
                score = _calculate_recommendation_score(
                    movie, target_happiness, target_energy, target_tags
                )
                movie_copy = movie.copy()
                movie_copy["score"] = score
                movie_copy["type"] = "movie"
                recommendations.append(movie_copy)
    
    # 점수 순으로 정렬하고 상위 n_items개 반환
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:n_items]


def _calculate_recommendation_score(
    item: Dict[str, Any],
    target_happiness: int,
    target_energy: int,
    target_tags: List[str]
) -> float:
    """아이템의 추천 점수 계산"""
    item_tags = item.get("mood_tags", [])
    item_energy = item.get("energy", 5)
    item_valence = item.get("valence", 5)
    
    # 태그 매칭 점수 (40%)
    tag_score = utils.calculate_emotion_score(item_tags, target_tags) * 0.4
    
    # 에너지 매칭 점수 (30%)
    energy_score = utils.calculate_energy_match(item_energy, target_energy) * 0.3
    
    # 밸런스(긍정성) 매칭 점수 (30%)
    valence_score = utils.calculate_valence_match(item_valence, target_happiness) * 0.3
    
    total_score = tag_score + energy_score + valence_score
    
    return total_score


def summarize_reason(item: Dict[str, Any], emotion_profile: Dict[str, Any]) -> str:
    """
    왜 이 콘텐츠를 추천했는지 자연어로 설명합니다.
    
    Args:
        item: 추천된 아이템 (노래 또는 영화)
        emotion_profile: 감정 프로필
    
    Returns:
        추천 이유 설명 (한국어)
    """
    item_tags = item.get("mood_tags", [])
    item_energy = item.get("energy", 5)
    item_valence = item.get("valence", 5)
    item_type = "노래" if item.get("type") == "song" else "영화"
    
    target_tags = emotion_profile["tags"]
    target_energy = emotion_profile["energy"]
    target_happiness = emotion_profile["happiness"]
    
    # 공통 태그 찾기
    common_tags = set(item_tags) & set(target_tags)
    
    reasons = []
    
    # 태그 기반 이유
    if common_tags:
        tag_list = ", ".join(list(common_tags)[:3])
        reasons.append(f"당신의 감정 태그({tag_list})와 잘 맞습니다")
    
    # 에너지 기반 이유
    energy_diff = abs(item_energy - target_energy)
    if energy_diff <= 2:
        if item_energy >= 7:
            reasons.append("높은 에너지로 활력을 불어넣어줍니다")
        elif item_energy <= 3:
            reasons.append("잔잔한 분위기로 마음을 진정시켜줍니다")
        else:
            reasons.append("적당한 에너지로 기분을 조절해줍니다")
    
    # 밸런스 기반 이유
    valence_diff = abs(item_valence - target_happiness)
    if valence_diff <= 2:
        if item_valence >= 7:
            reasons.append("밝고 긍정적인 분위기로 기분을 좋게 만들어줍니다")
        elif item_valence <= 3:
            reasons.append("감성적이고 위로가 되는 분위기입니다")
    
    # 장르 기반 이유
    genre = item.get("genre", "")
    if genre:
        reasons.append(f"{genre} 장르의 특색이 당신의 현재 기분과 잘 어울립니다")
    
    # 기본 이유 (위 이유가 없을 경우)
    if not reasons:
        reasons.append("당신의 현재 감정 상태와 잘 맞는 콘텐츠입니다")
    
    # 최종 문장 구성
    reason_text = " ".join(reasons[:2])  # 최대 2개 이유만 사용
    
    return f"이 {item_type}을(를) 추천한 이유: {reason_text}."

