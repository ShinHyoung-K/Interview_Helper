import tkinter as tk
from tkinter import messagebox
import json
import time

# 질문 JSON 파일 예시
questions_json = '''
[
    "자기소개를 해주세요.",
    "이 회사에 지원한 이유는 무엇인가요?",
    "본인의 장점과 단점을 말씀해주세요.",
    "앞으로의 커리어 계획은 어떻게 되나요?",
    "어려운 상황에서 극복했던 경험을 말씀해주세요."
]
'''

# JSON 형식의 질문을 파싱
questions = json.loads(questions_json)

class InterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("면접 준비 프로그램")
        self.root.geometry("600x400")

        # 초기 설정
        self.current_question = 0
        self.answer_times = []
        self.question_start_time = None
        self.total_start_time = time.time()
        self.total_time_limit = 600  # 10분 제한

        # 인터페이스 생성
        self.create_widgets()

        # 키보드 이벤트 바인딩
        self.root.bind("<space>", self.toggle_timer_key)  # Space 키로 타이머 시작/정지
        self.root.bind("<Return>", self.next_question_key)  # Enter 키로 다음 질문

    def create_widgets(self):
        # 질문 표시 레이블
        self.question_label = tk.Label(self.root, text="질문이 여기에 표시됩니다.", font=("Arial", 16), wraplength=500)
        self.question_label.pack(pady=20)

        # 답변 시간 표시 레이블
        self.answer_time_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.answer_time_label.pack(pady=10)

        # 남은 시간 표시
        self.time_label = tk.Label(self.root, text="남은 시간: 10:00", font=("Arial", 14))
        self.time_label.pack(pady=10)

        # 시작 페이지 설정
        self.show_question()

        # 타이머 업데이트
        self.update_total_timer()

    def show_question(self):
        """현재 질문을 화면에 표시."""
        if self.current_question < len(questions):
            self.question_label.config(text=f"질문 {self.current_question + 1}: {questions[self.current_question]}")
            self.answer_time_label.config(text="답변 시간: 0.00초")
        else:
            self.finish_interview()

    def toggle_timer(self):
        """답변 타이머 시작/정지."""
        if self.question_start_time is None:
            # 타이머 시작
            self.question_start_time = time.time()
            self.answer_time_label.config(text="답변 시간: 0.00초")
            self.update_answer_timer()
        else:
            # 타이머 멈춤
            elapsed_time = time.time() - self.question_start_time
            self.answer_times.append(elapsed_time)
            self.question_start_time = None
            self.answer_time_label.config(text=f"최종 답변 시간: {elapsed_time:.2f}초")
            messagebox.showinfo("답변 완료", f"답변 시간: {elapsed_time:.2f}초")

    def update_answer_timer(self):
        """답변 시간 표시 업데이트 (타이머 작동 중일 때)."""
        if self.question_start_time is not None:
            elapsed_time = time.time() - self.question_start_time
            self.answer_time_label.config(text=f"답변 시간: {elapsed_time:.2f}초")
            self.root.after(100, self.update_answer_timer)

    def toggle_timer_key(self, event):
        """Space 키로 타이머 시작/정지."""
        self.toggle_timer()

    def next_question(self):
        """다음 질문으로 이동."""
        if self.question_start_time is not None:
            messagebox.showwarning("타이머 실행 중", "타이머를 멈춘 후 다음 질문으로 이동하세요.")
            return

        if self.current_question < len(questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.finish_interview()

    def next_question_key(self, event):
        """Enter 키로 다음 질문으로 이동."""
        self.next_question()

    def update_total_timer(self):
        """전체 타이머 업데이트."""
        elapsed_time = time.time() - self.total_start_time
        remaining_time = self.total_time_limit - elapsed_time

        if remaining_time <= 0:
            self.finish_interview()
        else:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            self.time_label.config(text=f"남은 시간: {minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_total_timer)

    def finish_interview(self):
        """면접 종료 후 결과 표시."""
        total_elapsed_time = time.time() - self.total_start_time

        # 결과 페이지로 이동
        self.clear_widgets()
        result_text = "--- 면접 결과 ---\n"
        for i, time_taken in enumerate(self.answer_times, 1):
            result_text += f"질문 {i}: {questions[i - 1]}\n답변 시간: {time_taken:.2f}초\n\n"
        result_text += f"총 소요 시간: {total_elapsed_time:.2f}초"

        result_label = tk.Label(self.root, text=result_text, font=("Arial", 14), justify="left")
        result_label.pack(pady=20)

        close_button = tk.Button(self.root, text="종료", font=("Arial", 14), command=self.root.quit)
        close_button.pack(pady=10)

    def clear_widgets(self):
        """화면의 모든 위젯 제거."""
        for widget in self.root.winfo_children():
            widget.destroy()


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewApp(root)
    root.mainloop()
