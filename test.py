# main.py

import streamlit as st
import random
import time


def main():
    st.title("문장의 행위 주체 맞추기 테스트 / Test to fit the action subject of a sentence")
    st.write("문장을 읽고, 해당 문장의 행위 주체를 선택하세요. / Read the sentence, and choose the actor in that sentence.")
    st.write("---")

    # 언어 선택
    if 'language' not in st.session_state:
        st.session_state.language = None

    if st.session_state.language is None:
        language = st.radio("사용할 언어를 선택하세요:", ["한국어", "English"])
        if st.button("선택 완료"):
            st.session_state.language = language
            st.session_state.current_question = 0  # 초기화
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.start_time = None
    else:
        st.write(f"**선택된 언어:** {st.session_state.language}")
        st.write("---")

        # 문제 데이터 (한국어 및 영어)
        korean_active = [
            {"sentence": "제프리가 그 사람을 죽였다.", "subject": "사람", "options": ["제프리", "사람"]},
            {"sentence": "농부가 옥수수를 창고에 저장한다.", "subject": "농부", "options": ["농부", "옥수수"]},
            {"sentence": "경찰이 도둑을 잡았다.", "subject": "경찰", "options": ["경찰", "도둑"]},
            {"sentence": "그 책들은 마틸다를 새로운 세계로 데려가 주었다.", "subject": "책", "options": ["책", "마틸다"]},
            {"sentence": "선생님은 학생들에 영감을 주었으며, 큰 꿈을 꾸도록 격려했다", "subject": "선생님", "options": ["학생", "선생님"]},
            {"sentence": "저기 파란 정장을 입은 남자가 저 일꾼들을 고용했다.", "subject": "남자", "options": ["남자", "일꾼"]},
            {"sentence": "아이들이 공원에서 놀고 있다.", "subject": "아이", "options": ["아이", "공원"]},
            {"sentence": "그녀가 케이크를 만들었다.", "subject": "그녀", "options": ["그녀", "케이크"]},
        ]

        korean_passive = [
            {"sentence": "그 사람이 제프리에게 죽었다.", "subject": "사람", "options": ["사람", "제프리"]},
            {"sentence": "옥수수가 농부에 의해 창고에 저장된다.", "subject": "농부", "options": ["옥수수", "농부"]},
            {"sentence": "도둑이 경찰에게 잡혔다.", "subject": "경찰", "options": ["도둑", "경찰"]},
            {"sentence": "마틸다는 그 책을 통해 새로운 세계로 이끌렸다.", "subject": "책", "options": ["책", "마틸다"]},
            {"sentence": "학생들은 선생님에게 영감을 받았고, 큰 꿈을 꾸도록 격려받았다.", "subject": "선생님", "options": ["학생", "선생님"]},
            {"sentence": "저 일꾼들은 저기 파란 정장을 입은 남자에게 고용됐다.", "subject": "남자", "options": ["일꾼", "남자"]},
            {"sentence": "공원이 아이들에 의해 놀이터로 변했다.", "subject": "아이", "options": ["아이", "공원"]},
            {"sentence": "케이크가 그녀에 의해 만들어졌다.", "subject": "그녀", "options": ["케이크", "그녀"]},
        ]

        english_active = [
            {"sentence": "Jeffery killed him.", "subject": "He", "options": ["He", "Jeffery"]},
            {"sentence": "Farmer stores corn in the storage.", "subject": "Farmer", "options": ["Farmer", "Corn"]},
            {"sentence": "Police caught thief.", "subject": "Police", "options": ["Police", "Thief"]},
            {"sentence": "The books transported Matilda into new worlds.", "subject": "Book", "options": ["Matilda", "Book"]},
            {"sentence": "The teacher inspired her students and encouraged them to dream big.", "subject": "Teacher", "options": ["Student", "Teacher"]},
            {"sentence": "That man in the blue suit hired those workers.", "subject": "Man", "options": ["Man", "Worker"]},
            {"sentence": "She made a cake.", "subject": "She", "options": ["She", "Cake"]},
            {"sentence": "The teacher gave the students an assignment.", "subject": "Teacher", "options": ["Teacher", "Students"]},
        ]

        english_passive = [
            {"sentence": "He was killed by Jeffery.", "subject": "He", "options": ["He", "Jeffery"]},
            {"sentence": "Corn is stored in storage by farmer.", "subject": "Farmer", "options": ["Farmer", "Corn"]},
            {"sentence": "Thief was caught by police.", "subject": "Police", "options": ["Police", "Thief"]},
            {"sentence": "Matilda was transported into new worlds by the books.", "subject": "Book", "options": ["Matilda", "Book"]},
            {"sentence": "The students were inspired by the teacher and encouraged to dream big.", "subject": "Teacher", "options": ["Student", "Teacher"]},
            {"sentence": "Those workers were hired by that man in the blue suit.", "subject": "Man", "options": ["Man", "Worker"]},
            {"sentence": "The assignment was given to the students by teacher.", "subject": "Teacher", "options": ["Teacher", "Students"]},
            {"sentence": "The cake was made by her.", "subject": "She", "options": ["She", "Cake"]},
        ]

        if st.session_state.language == "한국어":
            active_sentences = korean_active
            passive_sentences = korean_passive
        else:
            active_sentences = english_active
            passive_sentences = english_passive

        # 문제 섞기 및 초기화 (능동태 5개 + 수동태 5개)
        if 'shuffled_sentences' not in st.session_state:
            active_sample = random.sample(active_sentences, 5)
            passive_sample = random.sample(passive_sentences, 5)
            st.session_state.shuffled_sentences = random.sample(active_sample + passive_sample, 10)

        # 현재 문항 진행
        if st.session_state.current_question < len(st.session_state.shuffled_sentences):
            idx = st.session_state.current_question
            item = st.session_state.shuffled_sentences[idx]

            # 시간 기록 시작
            if st.session_state.start_time is None:
                st.session_state.start_time = time.perf_counter()

            st.write(f"**문제 {idx + 1}.** {item['sentence']}")
            user_choice = st.radio("문장의 행위의 주체는 누구일까요?/Who is the subject of the action of the sentence?", item['options'], key=f"radio_{idx}")

            # 제출 버튼 클릭 시 상태 업데이트
            if st.button("제출", key=f"button_{idx}"):
                elapsed_time = time.perf_counter() - st.session_state.start_time  # 초 단위로 기록
                st.session_state.answers.append({
                    '문제': item['sentence'],
                    '답변': user_choice,
                    '정답': item['subject'],
                    '소요 시간 (초)': elapsed_time
                })

                # 점수 계산
                if user_choice == item['subject']:
                    st.session_state.score += 1

                # 다음 문제로 이동
                st.session_state.current_question += 1
                st.session_state.start_time = None  # 다음 문제를 위해 초기화

        else:
            # 결과 출력
            st.write("---")
            st.write("### 테스트가 종료되었습니다.")
            st.write(f"총 {len(st.session_state.shuffled_sentences)}문제 중 {st.session_state.score}문제를 맞추셨습니다.")
            percentage = (st.session_state.score / len(st.session_state.shuffled_sentences)) * 100
            st.write(f"**정답률: {percentage:.1f}%**")

            # 상세 결과 출력
            st.write("---")
            st.write("#### 상세 결과")
            for i, answer in enumerate(st.session_state.answers):
                st.write(f"**문제 {i + 1}.** {answer['문제']}")
                st.write(f"- 당신의 답변: {answer['답변']}")
                st.write(f"- 정답: {answer['정답']}")
                st.write(f"- 소요 시간: {answer['소요 시간 (초)']:.6f}초")  # 소수점 6자리까지 출력
                st.write("---")

            # 다시 시작 버튼
            if st.button("다시 시작"):
                st.session_state.language = None  # 언어 선택부터 다시 시작
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.start_time = None
                del st.session_state.shuffled_sentences  # 초기화


if __name__ == "__main__":
    main()
