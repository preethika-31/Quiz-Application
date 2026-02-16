from django.shortcuts import render, redirect
from .models import Question, Score
from django.core.paginator import Paginator
import time


# ================= HOME =================
def index(request):
    return render(request, "index.html")


# ================= START QUIZ =================
def start_quiz(request):
    if request.method == "POST":
        username = request.POST.get("username")
        topic = request.POST.get("topic")

        # Validation
        if not username or not topic:
            return redirect("/")

        # Check if questions exist for topic
        if Question.objects.filter(topic=topic).count() == 0:
            return redirect("/")

        # Session setup
        request.session["username"] = username
        request.session["topic"] = topic
        request.session["answers"] = {}
        request.session["quiz_active"] = True
        request.session["quiz_start_time"] = time.time()
        request.session["quiz_duration"] = 120  # seconds

        return redirect("/quiz/1/")

    return redirect("/")


# ================= QUIZ QUESTION =================
def quiz_question(request, qno):
    if not request.session.get("quiz_active"):
        return redirect("/")

    start_time = request.session.get("quiz_start_time")
    duration = request.session.get("quiz_duration")

    # Safety check
    if not start_time or not duration:
        return redirect("/")

    elapsed = time.time() - start_time
    remaining = int(duration - elapsed)

    if remaining <= 0:
        return redirect("/quiz/submit/")

    topic = request.session.get("topic")
    if not topic:
        return redirect("/")

    questions = list(Question.objects.filter(topic=topic))
    total = len(questions)

    if total == 0:
        return redirect("/")

    if qno < 1 or qno > total:
        return redirect("/quiz/1/")

    question = questions[qno - 1]

    options = [
        question.opt1,
        question.opt2,
        question.opt3,
        question.opt4,
    ]

    progress = int((qno / total) * 100)

    if request.method == "POST":
        ans = request.POST.get("answer")

        answers = request.session.get("answers", {})
        answers[str(question.id)] = ans
        request.session["answers"] = answers

        if qno < total:
            return redirect(f"/quiz/{qno + 1}/")
        else:
            return redirect("/quiz/submit/")

    return render(request, "one_question.html", {
        "question": question,
        "options": options,
        "qno": qno,
        "total": total,
        "remaining": remaining,
        "progress": progress,
    })


# ================= FINAL SUBMIT =================
def final_submit(request):
    if not request.session.get("quiz_active"):
        return redirect("/")

    topic = request.session.get("topic")
    username = request.session.get("username")
    answers = request.session.get("answers", {})

    if not topic or not username:
        return redirect("/")

    questions = Question.objects.filter(topic=topic)

    total = questions.count()
    if total == 0:
        return redirect("/")

    score = 0
    for q in questions:
        if answers.get(str(q.id)) == q.answer:
            score += 1

    percentage = round((score / total) * 100, 2)

    # Save score
    Score.objects.create(
        username=username,
        topic=topic,
        score=score,
        total=total,
        percentage=percentage,
    )

    # Clear session
    request.session.flush()

    return render(request, "result.html", {
        "username": username,
        "score": score,
        "total": total,
        "percentage": percentage,
    })


# ================= LEADERBOARD =================
def leaderboard(request):
    selected_topic = request.GET.get("topic")

    base_qs = Score.objects.all()
    score_qs = base_qs.order_by("-percentage", "-score", "created_at")

    if selected_topic:
        score_qs = score_qs.filter(topic=selected_topic)

    paginator = Paginator(score_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    topics = (
        base_qs.values_list("topic", flat=True)
        .distinct()
        .order_by("topic")
    )

    return render(request, "leaderboard.html", {
        "page_obj": page_obj,
        "topics": topics,
        "selected_topic": selected_topic,
    })
