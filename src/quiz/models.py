from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    answer = models.CharField(max_length=100)

    class Meta:
        order_with_respect_to = "quiz"
