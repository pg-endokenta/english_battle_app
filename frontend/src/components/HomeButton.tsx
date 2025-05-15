export default function HomeButton() {
  const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL;
  return (
    <div className="mt-6">
      <a href={`${BACKEND_BASE_URL}/home`} className="text-blue-600 underline">
        ホームに戻る
      </a>
    </div>
  );
}