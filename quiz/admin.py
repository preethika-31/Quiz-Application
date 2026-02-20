from django.contrib import admin
from .models import Question, Score

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question', 'answer')
    search_fields = ('topic', 'question')
    list_filter = ('topic',)
    list_per_page = 10
    ordering = ('topic',)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('username', 'topic', 'score', 'total', 'percentage', 'created_at')
    search_fields = ('username', 'topic')
    list_filter = ('topic', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 10



admin.site.site_header = "Quiz Application Admin"
admin.site.site_title = "Quiz Dashboard"
admin.site.index_title = "Manage Quiz Data"
