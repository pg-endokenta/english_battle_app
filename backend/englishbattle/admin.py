from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import QuizSession, Sentence, QuestionAssignment, Answer

admin.site.register([
    QuizSession,
    Sentence,
    QuestionAssignment,
    Answer
])

    