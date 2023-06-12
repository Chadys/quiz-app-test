from rest_framework import viewsets
from quiz.models import Quiz, Question
from quiz.serializers import QuizSerializer, QuestionSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
