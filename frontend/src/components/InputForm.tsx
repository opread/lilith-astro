import React, { useState, useCallback, useMemo } from 'react';

export interface UserInput {
  name: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
  location: string;
  // Calculation Parameters (PM Exposure)
  houseSystem: 'Placidus' | 'Koch' | 'Regiomontanus';
  ephemerisSource: 'SwissEphemeris' | 'NASA';
  // Interpretation Engine Parameters (PM Exposure)
  interpretationEngine: 'RuleBased' | 'Hybrid' | 'PureAI';
  narrativeStyle: 'Professional' | 'Poetic' | 'Debug';
  // AI Layer Parameters (PM Exposure)
  aiModel: 'Gemini' | 'GPT-4' | 'Custom';
  aiTemperature: number; // 0.0 to 1.0
  aiPromptVersion: string;
}

interface InputFormProps {
  onSubmit: (input: UserInput) => void;
  isLoading: boolean;
  isAdmin: boolean;
}

const defaultInput: UserInput = {
  name: 'John Doe',
  date: '1990-01-01',
  time: '12:00',
  location: 'London, UK',
  houseSystem: 'Placidus',
  ephemerisSource: 'SwissEphemeris',
  interpretationEngine: 'Hybrid',
  narrativeStyle: 'Professional',
  aiModel: 'Gemini',
  aiTemperature: 0.7,
  aiPromptVersion: 'v1.2-beta',
};

const InputForm: React.FC<InputFormProps> = ({ onSubmit, isLoading, isAdmin }) => {
  const [input, setInput] = useState<UserInput>(defaultInput);
  const [isPMConfigOpen, setIsPMConfigOpen] = useState(false);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setInput(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : value,
    }));
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(input);
  }, [input, onSubmit]);

  const pmConfigSection = useMemo(() => (
    <div className="card bg-secondary-subtle border-0 mt-4 p-3">
      <h5 className="card-title text-dark mb-3">Product Manager AI/Calc Configuration (Degrees of Freedom)</h5>
      
      <div className="row g-3">
        {/* Calculation Parameters */}
        <div className="col-md-6">
          <label htmlFor="houseSystem" className="form-label text-dark">House System</label>
          <select id="houseSystem" name="houseSystem" className="form-select" value={input.houseSystem} onChange={handleChange}>
            <option value="Placidus">Placidus</option>
            <option value="Koch">Koch</option>
            <option value="Regiomontanus">Regiomontanus</option>
          </select>
        </div>
        <div className="col-md-6">
          <label htmlFor="ephemerisSource" className="form-label text-dark">Ephemeris Source</label>
          <select id="ephemerisSource" name="ephemerisSource" className="form-select" value={input.ephemerisSource} onChange={handleChange}>
            <option value="SwissEphemeris">Swiss Ephemeris</option>
            <option value="NASA">NASA JPL (Experimental)</option>
          </select>
        </div>

        {/* Interpretation Engine Parameters */}
        <div className="col-md-6">
          <label htmlFor="interpretationEngine" className="form-label text-dark">Interpretation Engine</label>
          <select id="interpretationEngine" name="interpretationEngine" className="form-select" value={input.interpretationEngine} onChange={handleChange}>
            <option value="RuleBased">Rule-Based Only</option>
            <option value="Hybrid">Hybrid (Rules + AI Synthesis)</option>
            <option value="PureAI">Pure AI (Max Creativity)</option>
          </select>
        </div>
        <div className="col-md-6">
          <label htmlFor="narrativeStyle" className="form-label text-dark">Narrative Style</label>
          <select id="narrativeStyle" name="narrativeStyle" className="form-select" value={input.narrativeStyle} onChange={handleChange}>
            <option value="Professional">Professional (Neutral Tone)</option>
            <option value="Poetic">Poetic / Evocative</option>
            <option value="Debug">Debug (Detailed, rule-by-rule)</option>
          </select>
        </div>

        {/* AI Layer Parameters */}
        <div className="col-md-4">
          <label htmlFor="aiModel" className="form-label text-dark">AI Model</label>
          <select id="aiModel" name="aiModel" className="form-select" value={input.aiModel} onChange={handleChange}>
            <option value="Gemini">Gemini</option>
            <option value="GPT-4">GPT-4</option>
            <option value="Custom">Custom Local Model</option>
          </select>
        </div>
        <div className="col-md-4">
          <label htmlFor="aiTemperature" className="form-label text-dark">AI Temperature (0.0 - 1.0)</label>
          <input
            type="number"
            id="aiTemperature"
            name="aiTemperature"
            className="form-control"
            value={input.aiTemperature}
            onChange={handleChange}
            min="0.0"
            max="1.0"
            step="0.1"
          />
        </div>
        <div className="col-md-4">
          <label htmlFor="aiPromptVersion" className="form-label text-dark">AI Prompt Version</label>
          <input
            type="text"
            id="aiPromptVersion"
            name="aiPromptVersion"
            className="form-control"
            value={input.aiPromptVersion}
            onChange={handleChange}
          />
        </div>
      </div>
    </div>
  ), [input, handleChange]);


  return (
    <div className="card shadow-lg bg-dark border-primary">
      <div className="card-body p-5">
        <h3 className="card-title mb-4 text-white">Step 1: Input Birth Data</h3>
        <form onSubmit={handleSubmit}>
          {/* User Data Inputs */}
          <div className="row g-3 text-start">
            <div className="col-12">
              <label htmlFor="name" className="form-label text-light">Name</label>
              <input type="text" id="name" name="name" className="form-control" value={input.name} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <label htmlFor="date" className="form-label text-light">Birth Date</label>
              <input type="date" id="date" name="date" className="form-control" value={input.date} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <label htmlFor="time" className="form-label text-light">Birth Time (HH:MM)</label>
              <input type="time" id="time" name="time" className="form-control" value={input.time} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <label htmlFor="location" className="form-label text-light">Birth Location (City, Country)</label>
              <input type="text" id="location" name="location" className="form-control" value={input.location} onChange={handleChange} required />
            </div>
          </div>

          {/* PM Configuration Toggle */}
          {isAdmin && (
            <div className="d-grid mt-4">
              <button
                type="button"
                className={`btn btn-sm ${isPMConfigOpen ? 'btn-warning' : 'btn-info'}`}
                onClick={() => setIsPMConfigOpen(!isPMConfigOpen)}
              >
                {isPMConfigOpen ? 'Hide PM AI/Calc Configuration' : 'Show PM AI/Calc Configuration (Degrees of Freedom)'}
              </button>
            </div>
          )}

          {/* PM Configuration Section */}
          {isAdmin && isPMConfigOpen && pmConfigSection}

          {/* Submit Button */}
          <div className="d-grid mt-4">
            <button type="submit" className="btn btn-primary btn-lg" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Generate Horoscope & Synthesize Narrative'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InputForm;