import React from 'react';
import Chatbot from './components/Chatbot';
import ErrorBoundary from './components/ErrorBoundary';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Chatbot />
    </ErrorBoundary>
  );
};

export default App;
