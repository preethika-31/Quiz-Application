from django.shortcuts import render, redirect
from .models import Question, Score, Topic
from django.core.paginator import Paginator
import time


# ================= HOME =================



def index(request):
    topics = Topic.objects.all()   # DB la irukkura ella topics
    return render(request, "index.html", {"topics": topics})



# ================= START QUIZ =================


def start_quiz(request):
    if request.method == "POST":
        username = request.POST.get("username")
        topic_id = request.POST.get("topic")

        request.session["username"] = username
        request.session["topic_id"] = topic_id
        request.session["answers"] = {}
        request.session["quiz_active"] = True

        # TIMER
        request.session["quiz_start_time"] = time.time()
        request.session["quiz_duration"] = 120

        return redirect("/quiz/1/")

    return redirect("/")



# ================= QUIZ QUESTION =================
def quiz_question(request, qno):
    if not request.session.get("quiz_active"):
        return redirect("/")

    # TIMER CALC
    start_time = request.session.get("quiz_start_time")
    duration = request.session.get("quiz_duration")
    elapsed = time.time() - start_time
    remaining = int(duration - elapsed)

    if remaining <= 0:
        return redirect("/quiz/submit/")

    topic_id = request.session.get("topic_id")
    questions = list(Question.objects.filter(topic_id=topic_id))
    total = len(questions)

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

    topic_id = request.session.get("topic_id")
    username = request.session.get("username")
    answers = request.session.get("answers", {})

    if not topic_id or not username:
        return redirect("/")

    questions = Question.objects.filter(topic_id=topic_id)

    score = 0
    for q in questions:
        selected_answer = answers.get(str(q.id))
        if selected_answer and selected_answer.strip() == q.answer.strip():
            score += 1

    total = questions.count()
    percentage = round((score / total) * 100, 2) if total > 0 else 0

    # Get topic name for saving
    topic_name = questions.first().topic.name if questions.exists() else ""

    # SAVE TO DB
    Score.objects.create(
        username=username,
        topic=topic_name,
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
