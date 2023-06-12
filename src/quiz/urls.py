from rest_framework.routers import DefaultRouter

from quiz.views import QuizViewSet, QuestionViewSet

router = DefaultRouter()
router.register("quiz", QuizViewSet, basename="quiz")
router.register("question", QuestionViewSet, basename="question")

urlpatterns = router.urls
