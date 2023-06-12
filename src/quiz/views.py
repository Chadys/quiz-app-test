from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from quiz.models import Quiz, Question
from quiz.serializers import (
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
    AnswerResultSerializer,
)

from quiz.services import QuizService


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all().prefetch_related("questions")
    serializer_class = QuizSerializer

    @extend_schema(
        request=AnswerSerializer(many=True),
        responses={
            200: AnswerResultSerializer(),
            400: OpenApiTypes.OBJECT,
        },
    )
    @action(detail=True, pagination_class=None, methods=["POST"])
    def check_answers(self, request, *args, **kwargs):
        """
        Send the list of answer for each question of this quiz
        and you'll get back the success percentage
        """
        instance = self.get_object()
        serializer = AnswerSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        available_answers = {
            answer["question"]: answer["answer"] for answer in serializer.data
        }
        result = QuizService().get_quiz_result(instance, available_answers)

        serializer = AnswerResultSerializer(instance={"result_percentage": result})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
