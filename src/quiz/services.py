from quiz.models import Quiz


class QuizService:
    def get_quiz_result(self, quiz: Quiz, available_answers: dict[int, str]) -> int:
        total = 0
        correct = 0
        for question in quiz.questions.all():
            total += 1
            correct += int(
                question.check_answer(available_answers.get(question.id, None))
            )
        return int(float(correct) / total * 100)
