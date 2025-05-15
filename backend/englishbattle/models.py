from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from books.models import Book
import uuid

class Sentence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    japanese = models.TextField()
    english = models.TextField()

    class Meta:
        unique_together = ('book', 'number')

    def __str__(self):
        return f"{self.number}: {self.japanese} / {self.english}"

class QuizSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="無題のセッション")
    question_count = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='sessions')

    def __str__(self):
        return f"{self.title} by {self.host.username} ({self.created_at})"

class QuestionAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    order = models.IntegerField()

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(QuestionAssignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
