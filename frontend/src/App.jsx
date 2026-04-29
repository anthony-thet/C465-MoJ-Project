// App.jsx — MoJ root component (ICEX 11: live data)
//
// CHANGED from ICEX 10:
//   - Hardcoded JOKES array → fetch() to Flask API
//   - Added useEffect for data loading on mount
//   - Added three-state rendering: loading → data → error
//
// UNCHANGED from ICEX 10:
//   - JokeList and JokeCount components (they receive props, they don't
//     know or care where the data comes from)
//   - Component tree structure
//   - Show/Hide toggle behavior

import { useState, useEffect } from 'react';
import JokeList from './components/JokeList';
import JokeCount from './components/JokeCount';
import AdminPanel from './components/AdminPanel';
const API_BASE = import.meta.env.VITE_API_BASE;

function App() {
  const [jokes, setJokes] = useState([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showJokes, setShowJokes] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        // Fetch jokes and count in parallel
        const [jokesRes, countRes] = await Promise.all([
          fetch(`${API_BASE}/jokes`),
          fetch(`${API_BASE}/jokes/count`),
        ]);

        if (!jokesRes.ok) {
          throw new Error(`Jokes endpoint returned ${jokesRes.status}`);
        }
        if (!countRes.ok) {
          throw new Error(`Count endpoint returned ${countRes.status}`);
        }

        const jokesBody = await jokesRes.json();
        const countBody = await countRes.json();

        setJokes(jokesBody.data.jokes);
        setCount(countBody.data.count);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <p>Loading jokes from the Ministry archive...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  return (
    <div>
      <h1>Ministry of Jokes</h1>
      <p>Welcome, {currentUser.username}!</p>	
      {currentUser.role === 'admin' && <AdminPanel />}
      <JokeCount count={count} />
      {currentUser.has_submitted ? (
        <>
          {loading && <p>Loading jokes...</p>}
          {error && <p style={{ color: 'red' }}>Error: {error}</p>}
          {!loading && !error && <JokeList jokes={jokes} />}
         </>
       ) : (
          <p><em>Submit your first joke to unlock the archive.
            Leave a penny, take a penny.</em></p>
       )}
  
      <button onClick={() => setShowJokes(!showJokes)}>
        {showJokes ? "Hide Jokes" : "Show Jokes"}
      </button>

      <JokeCount count={count} />

      <button onClick={() => setShowJokes(!showJokes)}>
        {showJokes ? "Hide Jokes" : "Show Jokes"}
      </button>

      {showJokes && <JokeList jokes={jokes} />}
    </div>
  );
}

export default App;
