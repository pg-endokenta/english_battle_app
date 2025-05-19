    import { useEffect, useState } from 'react';
import HomeButton from '../components/HomeButton';

    interface UserStats {
    username: string;
    total: number;
    correct: number;
    accuracy: number;
    }

    export default function PracticeStats() {
    const [stats, setStats] = useState<UserStats[]>([]);
    const [error, setError] = useState('');

    useEffect(() => {
        (async () => {
        try {
            const res = await fetch('/api/practice-stats/', {
            credentials: 'include',
            });
            if (!res.ok) throw new Error(await res.text());
            const data = await res.json();
            data.sort((a: UserStats, b: UserStats) => b.total - a.total);
            setStats(data);
        } catch (err) {
            setError('統計データの取得に失敗しました');
            console.error(err);
        }
        })();
    }, []);

    return (
        <>
        <div className="p-4 max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">全ユーザーの練習統計</h1>
        {error && <p className="text-red-500">{error}</p>}
        <table className="w-full border-collapse">
            <thead>
            <tr className="bg-gray-100">
                <th className="border p-2">ユーザー名</th>
                <th className="border p-2">総問題数</th>
                <th className="border p-2">正解数</th>
                <th className="border p-2">正答率 (%)</th>
            </tr>
            </thead>
            <tbody>
            {stats.map((user) => (
                <tr key={user.username}>
                <td className="border p-2">{user.username}</td>
                <td className="border p-2">{user.total}</td>
                <td className="border p-2">{user.correct}</td>
                <td className="border p-2">{user.accuracy}</td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
        <HomeButton />
        </>
    );
    }
