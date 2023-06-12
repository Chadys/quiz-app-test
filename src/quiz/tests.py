from pytest_mock import MockerFixture
from quiz.models import Question

from quiz.services import QuizService


class TestQuestion:
    def test_check_answer(self):
        assert Question(answer="étais-tu la").check_answer("etais TU là")
        assert Question(answer="étais-tu la").check_answer("étais;.   tu   la!(?")
        assert not Question(answer="étais-tu la").check_answer("àtais-tu la")


class TestQuizService:
    def test_get_quiz_result(self, mocker: MockerFixture):
        service = QuizService()
        quiz = mocker.MagicMock(
            **{
                "questions.all.return_value": [
                    Question(id=1, answer="OK1"),
                    Question(id=2, answer="OK2"),
                    Question(id=3, answer="OK3"),
                    Question(id=4, answer="OK4"),
                    Question(id=5, answer="OK5"),
                    Question(id=6, answer="OK6"),
                ],
            }
        )
        available_answers = {
            1: "OK1",
            2: "OK2",
            3: "OK3",
            4: "KO4",
            5: "OK5",
            7: "KO7",
        }
        assert service.get_quiz_result(quiz, available_answers) == 66
