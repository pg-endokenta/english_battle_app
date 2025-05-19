from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .models import Sentence, PracticeRecord
from .serializers import SentenceSerializer, PracticeRecordSerializer
import random
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
def random_sentence(request):
    book_id = request.query_params.get('book_id')
    if not book_id:
        return Response({'error': 'book_id is required'}, status=400)

    sentences = Sentence.objects.filter(book_id=book_id)
    if not sentences.exists():
        return Response({'error': 'No sentences found for this book_id'}, status=404)

    sentence = random.choice(sentences)
    serializer = SentenceSerializer(sentence)
    return Response(serializer.data)


class PracticeRecordViewSet(viewsets.ModelViewSet):
    queryset = PracticeRecord.objects.all()
    serializer_class = PracticeRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
def practice_stats(request):
    """
    ユーザーごとの練習統計を取得するAPIエンドポイント
    """
    users = User.objects.all()

    data = []
    for user in users:
        total = PracticeRecord.objects.filter(user=user).count()
        correct = PracticeRecord.objects.filter(user=user, is_correct=True).count()
        accuracy = (correct / total) * 100 if total > 0 else 0.0

        data.append({
            'username': user.username,
            'total': total,
            'correct': correct,
            'accuracy': round(accuracy, 2),
        })

    return Response(data)