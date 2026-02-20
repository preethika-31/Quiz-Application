from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("start/", views.start_quiz, name="start"),
    path("quiz/<int:qno>/", views.quiz_question, name="quiz_question"),
    path("quiz/submit/", views.final_submit, name="submit"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
