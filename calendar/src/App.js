import React from 'react'
import './App.css';
import Header from './components/Header'
import EventsListPage from './pages/EventsListPage';
import { Route, BrowserRouter as Router, Routes } from "react-router-dom"
import EventPage from './pages/EventPage'

function App() {
  return (
    <Router>
      <div className='app-container'>
        <Header />
        <Routes >
          <Route path="/" element={<EventsListPage />} />
          <Route path="/event/:id" element={<EventPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
