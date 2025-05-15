// src/components/WhoAmI.tsx
import React, { useEffect, useState } from 'react';

const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL

type UserInfo = {
  username: string;
};

export const WhoAmI: React.FC = () => {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND_BASE_URL}/users/whoami/`, {
      method: 'GET',
      credentials: 'include', // セッションクッキーを送信するために必須
    })
      .then((res) => {
        if (!res.ok) throw new Error('Not logged in');
        return res.json();
      })
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch(() => {
        setUser(null);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {user ? (
        <p>Logged in as: <strong>{user.username}</strong></p>
      ) : (
        <p>You are not logged in.</p>
      )}
    </div>
  );
};
