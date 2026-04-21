import { useState, useEffect } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE;

function AdminPanel() {
  const [jokes, setJokes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function fetchJokes() {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/admin/jokes`, {
        credentials: 'include',
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const body = await res.json();
      setJokes(body.data.jokes);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchJokes(); }, []);

  async function handleFlag(jokeId, currentFlagged) {
    await fetch(`${API_BASE}/admin/jokes/${jokeId}/flag`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ flagged: !currentFlagged }),
    });
    fetchJokes();  // re-fetch to reflect change
  }

  async function handleDelete(jokeId) {
    await fetch(`${API_BASE}/admin/jokes/${jokeId}`, {
      method: 'DELETE',
      credentials: 'include',
    });
    fetchJokes();  // re-fetch to reflect deletion
  }

  if (loading) return <p>Loading admin panel...</p>;
  if (error) return <p style={{ color: 'red' }}>Admin error: {error}</p>;

  return (
    <div>
      <h2>Admin Panel — The Inner Circle</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Text</th>
            <th>Author</th>
            <th>Flagged</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {jokes.map(joke => (
            <tr key={joke.id} style={joke.flagged ? { backgroundColor: '#ffe0e0' } : {}}>
              <td>{joke.id}</td>
              <td>{joke.text}</td>
              <td>{joke.author}</td>
              <td>{joke.flagged ? '🚩' : '—'}</td>
              <td>
                <button onClick={() => handleFlag(joke.id, joke.flagged)}>
                  {joke.flagged ? 'Unflag' : 'Flag'}
                </button>
                <button onClick={() => handleDelete(joke.id)}
                        style={{ marginLeft: '4px', color: 'red' }}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPanel;

