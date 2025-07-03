import { useEffect, useState, type FormEvent } from 'react';
import axios from 'axios';
import reactLogo from './assets/react.svg';
import viteLogo from './assets/vite.svg';
import './App.css';

interface CatFact {
  id: number;
  fact: string;
  created_at: string;
}

function App() {
  const [catFacts, setCatFacts] = useState<CatFact[]>([])
  const [newFact, setNewFact] = useState('')
  const [message, setMessage] = useState('')

  const fetchCatFacts = async () => {
    try {
      const response = await axios.get<CatFact[]>('http://localhost:8000/catfacts');
      setCatFacts(response.data);
    } catch (error) {
      console.error('Error fetching cat facts:', error);
    }
  };

  useEffect(() => {
    fetchCatFacts();
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage(''); // Clear previous message
    if (!newFact.trim()) return; // Prevent empty submissions
    try {
      await axios.post(
        'http://localhost:8000/catfacts',
        new URLSearchParams({fact: newFact}),
        {headers: {'Content-Type': 'application/x-www-form-urlencoded',}}
      );
      setMessage('Fact added successfully!');
      setNewFact(''); // Clear input field
      fetchCatFacts(); // Refresh the list of cat facts
    } catch (err: any) {
      if (err.response?.status === 409) {
        setMessage('Error: Fact already exists.');
      } else {
        setMessage('Error adding fact.');
      }
    }
  };

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <div className="container">
      <h1 className="title">🐱 Cat Facts</h1>

      <form onSubmit={handleSubmit} className="form">
        <input
          className="form-input"
          placeholder="Enter a new cat fact"
          value={newFact}
          onChange={(e) => setNewFact(e.target.value)}
        />
        <button type="submit" className="form-button">
          Add
        </button>
      </form>

      {message && <p className="message">{message}</p>}

      <ul className="fact-list">
        {catFacts.map((fact) => (
          <li key={fact.id} className="fact-item">
            <p className="fact-text">{fact.fact}</p>
            <small className="text-xs text-gray-500">Added on {fact.created_at}</small>
          </li>
        ))}
      </ul>
    </div>
    </>
  )
}

export default App
