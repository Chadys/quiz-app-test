import re
from django.db import models

from src.common.utils import convert_to_ascii


class Quiz(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    answer = models.CharField(max_length=100)

    def normalise_answer(self, answer: str):
        return re.sub(
            r"\s+",
            " ",
            re.sub(r"[-_.?,!;'\"()]", " ", convert_to_ascii(answer).lower()),
        ).strip()

    def check_answer(self, answer: str) -> bool:
        if answer is None:
            return False
        return self.normalise_answer(answer) == self.normalise_answer(self.answer)

    class Meta:
        order_with_respect_to = "quiz"
