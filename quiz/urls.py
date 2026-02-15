from django.urls import path
from . import views

urlpatterns = [

    # Home
    path("", views.index, name="index"),

    # Start quiz
    path("start/", views.start_quiz, name="start_quiz"),

    # 🔥 IMPORTANT: submit FIRST
    path("quiz/submit/", views.final_submit, name="final_submit"),

    # 🔥 IMPORTANT: qno MUST be int and MUST be AFTER submit
    path("quiz/<int:qno>/", views.quiz_question, name="quiz_question"),

    # Leaderboard
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
