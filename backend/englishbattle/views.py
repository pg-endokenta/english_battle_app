from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import QuizSession, Sentence, QuestionAssignment, Answer, AnswerEvaluation
import random
from django.utils import timezone
from django.shortcuts import get_object_or_404

from books.models import Book

from django.conf import settings

from .utils import get_vite_asset_path


@login_required
def create_session(request):
    if request.method == 'POST':
        title = request.POST.get('title', '無題のセッション')
        book_id = request.POST.get('book_id')
        question_count = int(request.POST.get('question_count', 30))

        book = get_object_or_404(Book, id=book_id)
        all_sentences = list(Sentence.objects.filter(book=book))
        question_count = min(question_count, len(all_sentences))

        session = QuizSession.objects.create(
            host=request.user,
            title=title,
            question_count=question_count,
            book=book
        )
        session.participants.add(request.user)

        questions = random.sample(all_sentences, question_count)
        for i, sentence in enumerate(questions):
            QuestionAssignment.objects.create(session=session, sentence=sentence, order=i)

        return redirect('home')

    books = Book.objects.all()
    return render(request, 'create_session.html', {
        'books': books
    })


@login_required
def join_session(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id)
    session.participants.add(request.user)
    return redirect('quiz', session_id=session.id)

@login_required
def quiz(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id)
    all_assignments = QuestionAssignment.objects.filter(session=session).order_by('order')

    # すでに解答済みの sentence を取得
    answered_sentence_ids = Answer.objects.filter(
        assignment__session=session, user=request.user
    ).values_list('assignment__sentence_id', flat=True)

    # 解答していない問題のみ表示
    assignments = all_assignments.exclude(sentence_id__in=answered_sentence_ids)

    if request.method == 'POST':
        from .gpt_utils import check_answer_with_gpt  # 仮: GPT判定用ユーティリティ
        from .models import AnswerEvaluation

        for assignment in assignments:
            user_answer = request.POST.get(f'answer_{assignment.id}', '').strip()
            is_correct = user_answer == assignment.sentence.english
            answer_obj = Answer.objects.create(
                assignment=assignment,
                user=request.user,
                answer_text=user_answer,
                is_correct=is_correct,
                answered_at=timezone.now(),
            )
            if not is_correct and user_answer:
                # ChatGPTで正誤判定
                gpt_result = check_answer_with_gpt(assignment.sentence.japanese, user_answer)
                AnswerEvaluation.objects.create(
                    answer=answer_obj,
                    is_correct=gpt_result["is_correct"],
                    explanation=gpt_result["explanation"],
                    checked_at=timezone.now(),
                )
        return redirect('results', session_id=session.id)

    return render(request, 'quiz.html', {
        'session': session,
        'assignments': assignments,
    })


@login_required
def results(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id)
    participants = session.participants.all()
    assignments = QuestionAssignment.objects.filter(session=session).order_by('order')

    # 各問題ごとに全ユーザーの解答を集約
    rows = []
    user_scores = {}  # ユーザーごとの正答数
    for assignment in assignments:
        sentence = assignment.sentence
        row = {
            'japanese': sentence.japanese,
            'english': sentence.english,
            'answers': []
        }
        for user in participants:
            answer = Answer.objects.filter(assignment=assignment, user=user).first()
            is_correct = answer.is_correct if answer else False
            if user.username not in user_scores:
                user_scores[user.username] = 0
            if is_correct:
                user_scores[user.username] += 1

            gpt_says_correct = None
            if not is_correct and hasattr(answer, 'answerevaluation_set'):
                first_evaluation = answer.answerevaluation_set.first()
                if first_evaluation:
                    gpt_says_correct = first_evaluation.is_correct

            
            row['answers'].append({
                'username': user.username,
                'text': answer.answer_text if answer else '未回答',
                'is_correct': is_correct,
                'gpt_says_correct': gpt_says_correct
            })
        rows.append(row)
        
    evaluations = AnswerEvaluation.objects.filter(answer__assignment__session=session)
    ev = []
    for evaluation in evaluations:
        ev.append({
            'username': evaluation.answer.user.username,
            'japanese': evaluation.answer.assignment.sentence.japanese,
            'sentence': evaluation.answer.answer_text,
            'is_correct': evaluation.is_correct,
            'explanation': evaluation.explanation,
        })
    # usernameでソート
    ev.sort(key=lambda x: x['username'])


    max_score = max(user_scores.values()) if user_scores else 0
    top_users = [name for name, score in user_scores.items() if score == max_score]


    return render(request, 'results.html', {
        'session': session,
        'participants': participants,
        'rows': rows,
        'user_scores': user_scores,
        'max_score': max_score,
        'top_users': top_users,
        'total_questions': session.question_count,
        'evaluations': ev,
    })



@login_required
def available_sessions(request):
    sessions = QuizSession.objects.exclude(participants=request.user)
    return render(request, 'available_sessions.html', {'sessions': sessions})


from django.db.models import Count

@login_required
def home(request):
    user = request.user

    available_sessions_raw = QuizSession.objects.exclude(participants=user).order_by('-created_at')

    available_sessions = []
    for session in available_sessions_raw:
        answered_user_count = Answer.objects.filter(
            assignment__session=session
        ).values('user').distinct().count()

        available_sessions.append({
            'session': session,
            'answered_user_count': answered_user_count,
        })

    joined_sessions = QuizSession.objects.filter(participants=user).order_by('-created_at')

    answered_sessions = []
    unanswered_sessions = []

    for session in joined_sessions:
        user_answers = Answer.objects.filter(assignment__session=session, user=user)
        answered_count = user_answers.count()

        # このセッションで回答したユーザー数（重複なし）
        answered_user_count = Answer.objects.filter(
            assignment__session=session
        ).values('user').distinct().count()

        if session.question_count == 0 or answered_count >= session.question_count:
            correct = user_answers.filter(is_correct=True).count()

            top_score = 0
            top_users = []
            for participant in session.participants.all():
                participant_correct = Answer.objects.filter(
                    assignment__session=session, user=participant, is_correct=True
                ).count()
                if participant_correct > top_score:
                    top_score = participant_correct
                    top_users = [participant.username]
                elif participant_correct == top_score:
                    top_users.append(participant.username)

            answered_sessions.append({
                'session': session,
                'correct': correct,
                'total': session.question_count,
                'top_users': top_users,
                'top_score': top_score,
                'answered_user_count': answered_user_count,
            })
        else:
            unanswered_sessions.append({
                'session': session,
                'answered_user_count': answered_user_count,
            })

    return render(request, 'home.html', {
        'available_sessions': available_sessions,
        'unanswered_sessions': unanswered_sessions,
        'answered_sessions': answered_sessions,
    })



@login_required
def sentence_list(request):
    book_id = request.GET.get("book_id")
    books = Book.objects.all()

    if book_id:
        book = get_object_or_404(Book, id=book_id)
        sentences = Sentence.objects.filter(book=book).order_by("number")
    else:
        sentences = Sentence.objects.all().order_by("number")

    return render(request, 'sentence_list.html', {
        'sentences': sentences,
        'books': books,
        'selected_book_id': book_id,
    })


@login_required
def react_index(request):
    js_path = get_vite_asset_path('index.html')
    return render(request, 'react_index.html', { 'js_path': js_path })