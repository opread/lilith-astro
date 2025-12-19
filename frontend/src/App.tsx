import React, { useState } from 'react';
import InputForm, { UserInput } from './components/InputForm';
import OutputDisplay from './components/OutputDisplay';
import AstrologicalChart from './types/AstrologicalChart';
import HoroscopeNarrative from './types/HoroscopeNarrative';
import { processFlow } from './api';

// Define the main application state stages
type AppState = 'INPUT' | 'PROCESSING' | 'DISPLAY';

const App: React.FC = () => {
  // Use location path to determine the view type (basic routing)
  const isAdmin = window.location.pathname.startsWith('/admin');
  
  const [state, setState] = useState<AppState>('INPUT');
  const [chart, setChart] = useState<AstrologicalChart | null>(null);
  const [narrative, setNarrative] = useState<HoroscopeNarrative | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleProcess = async (input: UserInput) => {
    setState('PROCESSING');
    setError(null);
    setChart(null);
    setNarrative(null);

    try {
      const result = await processFlow(input);
      setChart(result.chart);
      setNarrative(result.narrative);
      setState('DISPLAY');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An unknown error occurred during processing.');
      setState('INPUT'); // Return to input state on error
    }
  };

  const handleReset = () => {
    setState('INPUT');
    setError(null);
    setChart(null);
    setNarrative(null);
  };

  const renderContent = () => {
    switch (state) {
      case 'INPUT':
        return <InputForm onSubmit={handleProcess} isLoading={false} isAdmin={isAdmin} />;
      case 'PROCESSING':
        return (
          <div className="text-center p-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Calculating chart and synthesizing narrative...</p>
          </div>
        );
      case 'DISPLAY':
        if (chart && narrative) {
          return (
            <OutputDisplay
              chart={chart}
              narrative={narrative}
              onReset={handleReset}
              isAdmin={isAdmin}
            />
          );
        }
        return <p className="text-danger">Error: Missing chart or narrative data.</p>;
      default:
        return null;
    }
  };

  return (
    <div className="container-fluid min-vh-100 bg-dark text-white p-4">
      <h1 className="text-center mb-5 text-primary">{isAdmin ? 'Lilith AI Admin Dashboard' : 'Lilith AI Horoscope Synthesizer'}</h1>
      {error && (
        <div className="alert alert-danger" role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}
      <div className="row justify-content-center">
        <div className="col-lg-10">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default App;