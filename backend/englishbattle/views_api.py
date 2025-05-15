# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Sentence
from .serializers import SentenceSerializer
import random

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
