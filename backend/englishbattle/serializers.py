# serializers.py
from rest_framework import serializers
from .models import Sentence, PracticeRecord

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'japanese', 'english', 'number']


class PracticeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeRecord
        fields = ['id', 'user', 'sentence', 'input_text', 'is_correct', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']