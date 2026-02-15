from django.db import models

class Question(models.Model):
    topic = models.CharField(max_length=50)
    question = models.TextField()
    opt1 = models.CharField(max_length=100)
    opt2 = models.CharField(max_length=100)
    opt3 = models.CharField(max_length=100)
    opt4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.topic} - {self.question[:30]}"



class Score(models.Model):
    username = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    score = models.IntegerField()
    total = models.IntegerField()
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.score}/{self.total}"
