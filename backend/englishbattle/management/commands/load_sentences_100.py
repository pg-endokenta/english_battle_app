from django.core.management.base import BaseCommand
from englishbattle.models import Sentence
from books.models import Book

class Command(BaseCommand):
    help = '100件の英作文問題をDBに登録（自動生成）'

    def handle(self, *args, **kwargs):

        book, _ = Book.objects.update_or_create(
            title="テスト問題集",
        )

        problems = [
            { "number": 1, "japanese": "私は学生です", "english": "I am a student" },
            { "number": 2, "japanese": "私は先生です", "english": "I am a teacher" },
            { "number": 3, "japanese": "私は医者です", "english": "I am a doctor" },
            { "number": 4, "japanese": "私はエンジニアです", "english": "I am an engineer" },
            { "number": 5, "japanese": "私は歌手です", "english": "I am a singer" },
            { "number": 6, "japanese": "私は料理をします", "english": "I cook" },
            { "number": 7, "japanese": "私はピアノを弾きます", "english": "I play the piano" },
            { "number": 8, "japanese": "私は毎日走ります", "english": "I run every day" },
            { "number": 9, "japanese": "私はテレビを見ます", "english": "I watch TV" },
            { "number": 10, "japanese": "私はサッカーが好きです", "english": "I like soccer" },
            { "number": 11, "japanese": "彼は学生です", "english": "He is a student" },
            { "number": 12, "japanese": "彼は先生です", "english": "He is a teacher" },
            { "number": 13, "japanese": "彼は医者です", "english": "He is a doctor" },
            { "number": 14, "japanese": "彼はエンジニアです", "english": "He is an engineer" },
            { "number": 15, "japanese": "彼は歌手です", "english": "He is a singer" },
            { "number": 16, "japanese": "彼は料理をします", "english": "He cooks" },
            { "number": 17, "japanese": "彼はピアノを弾きます", "english": "He plays the piano" },
            { "number": 18, "japanese": "彼は毎日走ります", "english": "He runs every day" },
            { "number": 19, "japanese": "彼はテレビを見ます", "english": "He watches TV" },
            { "number": 20, "japanese": "彼はサッカーが好きです", "english": "He likes soccer" },
            { "number": 21, "japanese": "彼女は学生です", "english": "She is a student" },
            { "number": 22, "japanese": "彼女は先生です", "english": "She is a teacher" },
            { "number": 23, "japanese": "彼女は医者です", "english": "She is a doctor" },
            { "number": 24, "japanese": "彼女はエンジニアです", "english": "She is an engineer" },
            { "number": 25, "japanese": "彼女は歌手です", "english": "She is a singer" },
            { "number": 26, "japanese": "彼女は料理をします", "english": "She cooks" },
            { "number": 27, "japanese": "彼女はピアノを弾きます", "english": "She plays the piano" },
            { "number": 28, "japanese": "彼女は毎日走ります", "english": "She runs every day" },
            { "number": 29, "japanese": "彼女はテレビを見ます", "english": "She watches TV" },
            { "number": 30, "japanese": "彼女はサッカーが好きです", "english": "She likes soccer" },
            { "number": 31, "japanese": "私たちは学生です", "english": "We are students" },
            { "number": 32, "japanese": "私たちは先生です", "english": "We are teachers" },
            { "number": 33, "japanese": "私たちは医者です", "english": "We are doctors" },
            { "number": 34, "japanese": "私たちはエンジニアです", "english": "We are engineers" },
            { "number": 35, "japanese": "私たちは歌手です", "english": "We are singers" },
            { "number": 36, "japanese": "私たちは料理をします", "english": "We cook" },
            { "number": 37, "japanese": "私たちはピアノを弾きます", "english": "We play the piano" },
            { "number": 38, "japanese": "私たちは毎日走ります", "english": "We run every day" },
            { "number": 39, "japanese": "私たちはテレビを見ます", "english": "We watch TV" },
            { "number": 40, "japanese": "私たちはサッカーが好きです", "english": "We like soccer" },
            { "number": 41, "japanese": "あなたは学生です", "english": "You are students" },
            { "number": 42, "japanese": "あなたは先生です", "english": "You are teachers" },
            { "number": 43, "japanese": "あなたは医者です", "english": "You are doctors" },
            { "number": 44, "japanese": "あなたはエンジニアです", "english": "You are engineers" },
            { "number": 45, "japanese": "あなたは歌手です", "english": "You are singers" },
            { "number": 46, "japanese": "あなたは料理をします", "english": "You cook" },
            { "number": 47, "japanese": "あなたはピアノを弾きます", "english": "You play the piano" },
            { "number": 48, "japanese": "あなたは毎日走ります", "english": "You run every day" },
            { "number": 49, "japanese": "あなたはテレビを見ます", "english": "You watch TV" },
            { "number": 50, "japanese": "あなたはサッカーが好きです", "english": "You like soccer" },
            { "number": 51, "japanese": "彼らは学生です", "english": "They are students" },
            { "number": 52, "japanese": "彼らは先生です", "english": "They are teachers" },
            { "number": 53, "japanese": "彼らは医者です", "english": "They are doctors" },
            { "number": 54, "japanese": "彼らはエンジニアです", "english": "They are engineers" },
            { "number": 55, "japanese": "彼らは歌手です", "english": "They are singers" },
            { "number": 56, "japanese": "彼らは料理をします", "english": "They cook" },
            { "number": 57, "japanese": "彼らはピアノを弾きます", "english": "They play the piano" },
            { "number": 58, "japanese": "彼らは毎日走ります", "english": "They run every day" },
            { "number": 59, "japanese": "彼らはテレビを見ます", "english": "They watch TV" },
            { "number": 60, "japanese": "彼らはサッカーが好きです", "english": "They like soccer" },
        ]

        for p in problems:
            Sentence.objects.update_or_create(
                book=book,
                number=p["number"],
                defaults={
                    "japanese": p["japanese"],
                    "english": p["english"],
                }
            )

        self.stdout.write(self.style.SUCCESS(f'{len(problems)} 件のSentenceを保存しました。'))
