import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './style.css'; // This now contains your Tailwind styles

ReactDOM.createRoot(document.getElementById('app')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);