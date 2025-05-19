// React Frontend (TypeScript) using fetch
import { useEffect, useState, useRef } from 'react';

const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || '';

interface Sentence {
  id: string;
  japanese: string;
  english: string;
}

interface Book {
  id: string;
  title: string;
}

function highlightDifferences(input: string, answer: string): [string, string] {
  const inputWords = input.split(' ');
  const answerWords = answer.split(' ');
  const maxLength = Math.max(inputWords.length, answerWords.length);

  const highlightedInput = [];
  const highlightedAnswer = [];

  for (let i = 0; i < maxLength; i++) {
    const userWord = inputWords[i] || '';
    const correctWord = answerWords[i] || '';
    if (userWord.toLowerCase() === correctWord.toLowerCase()) {
      highlightedInput.push(userWord);
      highlightedAnswer.push(correctWord);
    } else {
      highlightedInput.push(`<span class='bg-red-200'>${userWord}</span>`);
      highlightedAnswer.push(`<span class='bg-green-200'>${correctWord}</span>`);
    }
  }

  return [highlightedInput.join(' '), highlightedAnswer.join(' ')];
}

function BookSelector({ bookId, setBookId, books }: { bookId: string, setBookId: (id: string) => void, books: Book[] }) {
  return (
    <label className="block mb-2">
      出題する本:
      <select
        className="border p-1 ml-2"
        value={bookId}
        onChange={(e) => setBookId(e.target.value)}
      >
        {books.map((book) => (
          <option key={book.id} value={book.id}>{book.title}</option>
        ))}
      </select>
    </label>
  );
}

function AnswerResult({ label, html }: { label: string; html: string }) {
  return (
    <div>
      <p className="text-gray-500">{label}</p>
      <p dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}

function PreviousAnswer({ sentence, result, inputHTML, answerHTML }: {
  sentence: Sentence & { number?: number },
  result: string,
  inputHTML: string,
  answerHTML: string
}) {
  return (
    <div className="mt-6 p-4 border rounded bg-gray-50">
      <p className="text-sm text-gray-600">前の問題: {sentence.number ? `No.${sentence.number}` : ''}</p>
      <p className="text-md">{sentence.japanese}</p>
      <p className={`font-semibold ${result === 'correct' ? 'text-green-600' : 'text-red-600'}`}>{result === 'correct' ? '正解！' : '不正解'}</p>
      <div className="mt-2 text-sm grid grid-cols-2 gap-4">
        <AnswerResult label="あなたの解答" html={inputHTML} />
        <AnswerResult label="正解" html={answerHTML} />
      </div>
    </div>
  );
}

export default function TranslatePractice() {
  const [bookId, setBookId] = useState('');
  const [books, setBooks] = useState<Book[]>([]);
  const [sentence, setSentence] = useState<Sentence | null>(null);
  const [userInput, setUserInput] = useState('');
  const [previousSentence, setPreviousSentence] = useState<Sentence | null>(null);
  const [previousResult, setPreviousResult] = useState<string | null>(null);
  const [previousUserInput, setPreviousUserInput] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${BACKEND_BASE_URL}/api/books/`, { credentials: 'include' });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        setBooks(data);
        if (data.length > 0) setBookId(data[0].id);
      } catch (error) {
        console.error('本の取得エラー:', error);
      }
    })();
  }, []);

  useEffect(() => {
    if (bookId) fetchNextSentence();
  }, [bookId]);

  const fetchNextSentence = async () => {
    try {
      const res = await fetch(`${BACKEND_BASE_URL}/api/sentences/random/?book_id=${bookId}`, {
        credentials: 'include'
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setSentence(data);
      setUserInput('');
      inputRef.current?.focus();
    } catch (error) {
      console.error('出題取得エラー:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!sentence) return;
    const isCorrect = userInput.trim().toLowerCase() === sentence.english.trim().toLowerCase();
    setPreviousResult(isCorrect ? 'correct' : 'incorrect');
    setPreviousUserInput(userInput);
    setPreviousSentence(sentence);
    if (isCorrect) {
      fetchNextSentence();
    } else {
      setUserInput('');
      inputRef.current?.focus();
    }
  };

  const [highlightedInputHTML, highlightedAnswerHTML] = previousSentence
    ? highlightDifferences(previousUserInput, previousSentence.english)
    : ['', ''];

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">英語翻訳練習</h1>

      <BookSelector bookId={bookId} setBookId={setBookId} books={books} />

      {previousSentence && previousResult && (
        <PreviousAnswer
          sentence={previousSentence}
          result={previousResult}
          inputHTML={highlightedInputHTML}
          answerHTML={highlightedAnswerHTML}
        />
      )}

      {sentence && (
        <div className="mt-4">
          <p className="text-lg font-medium">{sentence.japanese}</p>
          <form onSubmit={handleSubmit} className="mt-2">
            <input
              ref={inputRef}
              className="border px-2 py-1 w-full"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="英語で答えてください"
            />
          </form>
        </div>
      )}
    </div>
  );
}
