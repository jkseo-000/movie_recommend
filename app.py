"""
Vibe Recommender - 감정 기반 노래/영화 추천 앱
메인 Streamlit 앱
"""

import streamlit as st
import logic
import ui_components
from typing import Dict, Any
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Vibe Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if "emotion_history" not in st.session_state:
    st.session_state["emotion_history"] = []

if "current_recommendations" not in st.session_state:
    st.session_state["current_recommendations"] = []

if "current_emotion_profile" not in st.session_state:
    st.session_state["current_emotion_profile"] = None

if "feedback" not in st.session_state:
    st.session_state["feedback"] = {}

if "liked_movies" not in st.session_state:
    st.session_state["liked_movies"] = []  # 좋아한 영화 목록 저장

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "main"  # 페이지 네비게이션


def main():
    """메인 앱 함수"""
    
    # 사이드바: 사용자 이름 (선택적)
    st.sidebar.title("🎵 Vibe Recommender")
    user_name = st.sidebar.text_input(
        "이름 (선택사항)",
        placeholder="당신의 이름을 입력하세요",
        key="user_name"
    )
    
    if user_name:
        st.sidebar.success(f"안녕하세요, {user_name}님! 👋")
    
    st.sidebar.markdown("---")
    
    # 페이지 네비게이션
    page = st.sidebar.radio(
        "메뉴",
        ["🏠 메인", "❤️ 내가 좋아한 영화"],
        key="page_navigation"
    )
    
    if page == "❤️ 내가 좋아한 영화":
        st.session_state["current_page"] = "liked_movies"
    else:
        st.session_state["current_page"] = "main"
    
    st.sidebar.markdown("---")
    
    # 메인 페이지인 경우에만 감정 입력 UI 렌더링
    if st.session_state["current_page"] == "main":
        input_data = ui_components.render_emotion_input()
    else:
        # 좋아한 영화 페이지에서는 더미 데이터
        input_data = {"mode": "movie", "mode_display": "영화"}
    
    # 페이지별 렌더링
    if st.session_state["current_page"] == "liked_movies":
        # 좋아한 영화 페이지
        ui_components.render_liked_movies_page()
    else:
        # 메인 페이지
        # 메인 영역
        st.title("🎬 Vibe Recommender – 감정 기반 영화 추천")
        st.markdown(
            """
            <div style="background: #f0f2f6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin: 0; color: #555;">
                    현재 감정을 입력하면, 당신의 기분에 맞는 영화를 추천해드립니다!<br>
                    텍스트, 이모지, 슬라이더, 상황을 종합하여 분석합니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 분석 및 추천 실행 (새로 추천 받기 버튼이 눌리지 않았을 때만)
        if input_data.get("analyze_clicked") and not st.session_state.get("refresh_clicked", False):
            # 감정 분석
            emotion_profile = logic.analyze_emotion(
                text_input=input_data["text"],
                emoji=input_data["emoji"],
                happiness=input_data["happiness"],
                energy=input_data["energy"],
                situation=input_data["situation"]
            )
            
            # 추천 콘텐츠 가져오기
            recommendations = logic.recommend_content(
                emotion_profile=emotion_profile,
                mode=input_data["mode"],
                n_items=5
            )
            
            # 세션 상태 업데이트
            st.session_state["current_emotion_profile"] = emotion_profile
            st.session_state["current_recommendations"] = recommendations
            st.session_state["current_mode"] = input_data["mode"]  # 모드 저장
            st.session_state["current_mode_display"] = input_data["mode_display"]  # 모드 표시 문자열 저장
            
            # 히스토리에 추가
            st.session_state["emotion_history"].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "emotion_profile": emotion_profile,
                "mode": input_data["mode_display"],
                "situation": input_data["situation"]
            })
            # refresh 플래그 리셋
            st.session_state["refresh_clicked"] = False
        
        # refresh 버튼이 눌렸다면 플래그 리셋
        if st.session_state.get("refresh_clicked", False):
            st.session_state["refresh_clicked"] = False
        
        # 감정 프로필이 있으면 표시
        if st.session_state["current_emotion_profile"]:
            emotion_profile = st.session_state["current_emotion_profile"]
            ui_components.render_emotion_summary(emotion_profile)
            
            # 추천 리스트 표시
            if st.session_state["current_recommendations"]:
                recommendations = st.session_state["current_recommendations"]
                # mode_display는 세션 상태에서 가져오기 (버튼 클릭 시에도 유지)
                mode_display = st.session_state.get("current_mode_display", input_data.get("mode_display", "콘텐츠"))
                ui_components.render_recommendation_list(
                    recommendations,
                    "영화"
                )
            else:
                st.info("추천할 콘텐츠가 없습니다. 다른 조건으로 시도해보세요.")
        else:
            # 초기 화면: 사용 안내
            st.info("👈 왼쪽 사이드바에서 감정을 입력하고 '분석 및 추천 실행' 버튼을 눌러주세요!")
            
            # 예시 표시
            with st.expander("💡 사용 예시 보기"):
                st.markdown("""
                ### 예시 1: 피곤한 퇴근길
                - **텍스트**: "오늘 하루가 정말 힘들었어요"
                - **이모지**: 😴
                - **행복도**: 3
                - **에너지**: 2
                - **상황**: 퇴근길 지하철
                - **추천 타입**: 영화
                
                ### 예시 2: 신나는 주말
                - **텍스트**: "주말이 너무 기대돼요!"
                - **이모지**: 😂
                - **행복도**: 9
                - **에너지**: 8
                - **상황**: 주말 아침 카페
                - **추천 타입**: 영화
                """)
        
        # 피드백 통계 표시
        if st.session_state.get("feedback"):
            st.markdown("---")
            ui_components.render_feedback_summary()
        
        # 감정 히스토리 표시
        if len(st.session_state["emotion_history"]) > 1:
            st.markdown("---")
            ui_components.render_emotion_history(st.session_state["emotion_history"])
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888; padding: 20px;">
            <p>Vibe Recommender | 감정 기반 콘텐츠 추천 시스템</p>
            <p style="font-size: 12px;">
                💡 향후 LLM 및 외부 API 연동 예정
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

