import React, { useState, useCallback, useMemo } from 'react';
import { geocodeLocation } from '../utils/geocoding';
import MapPicker from './MapPicker';

export interface UserInput {
  name: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
  location: string;
  latitude: number;
  longitude: number;
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
  isAdmin: boolean;
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
  latitude: 51.5074,
  longitude: -0.1278,
  houseSystem: 'Placidus',
  ephemerisSource: 'SwissEphemeris',
  interpretationEngine: 'Hybrid',
  narrativeStyle: 'Professional',
  aiModel: 'Gemini',
  aiTemperature: 0.7,
  aiPromptVersion: 'v1.2-beta',
  isAdmin: false,
};

const InputForm: React.FC<InputFormProps> = ({ onSubmit, isLoading, isAdmin }) => {
  const [input, setInput] = useState<UserInput>({...defaultInput, isAdmin});
  const [isPMConfigOpen, setIsPMConfigOpen] = useState(false);
  const [locationSearchStatus, setLocationSearchStatus] = useState<'idle' | 'searching' | 'found' | 'not-found'>('idle');
  const [showMapPicker, setShowMapPicker] = useState(false);
  const [coordinateSource, setCoordinateSource] = useState<'none' | 'manual' | 'geocoded'>('geocoded');

  const handleGeocode = useCallback(async (location: string) => {
    if (!location) {
      setLocationSearchStatus('idle');
      setCoordinateSource('none');
      setInput(prev => ({ ...prev, latitude: 0, longitude: 0 }));
      return;
    }
    setLocationSearchStatus('searching');
    const result = await geocodeLocation(location);

    if (result) {
      setLocationSearchStatus('found');
      setCoordinateSource('geocoded');
      setInput(prev => ({
        ...prev,
        latitude: result.lat,
        longitude: result.lon,
      }));
    } else {
      setLocationSearchStatus('not-found');
      setCoordinateSource('none');
      setInput(prev => ({ ...prev, latitude: 0, longitude: 0 }));
    }
  }, []);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    if (name === 'location') {
      // Clear coordinates on location change and mark as 'none' source, pending search
      setInput(prev => ({
        ...prev,
        location: value,
        latitude: 0,
        longitude: 0,
      }));
      setCoordinateSource('none');
      setLocationSearchStatus('idle'); // Will search on blur/submit
    } else {
      setInput(prev => ({
        ...prev,
        [name]: type === 'number' ? parseFloat(value) : value,
      }));
    }
  }, []);

  const handleLocationBlur = useCallback((e: React.FocusEvent<HTMLInputElement>) => {
    if (e.target.name === 'location' && e.target.value && locationSearchStatus === 'idle') {
      handleGeocode(e.target.value);
    }
  }, [handleGeocode, locationSearchStatus]);

  const handleSelectCoordinates = useCallback((lat: number, lon: number) => {
    setInput(prev => ({
      ...prev,
      latitude: lat,
      longitude: lon,
    }));
    setCoordinateSource('manual');
    setShowMapPicker(false);
  }, []);

  const handleManualEntry = () => {
    setCoordinateSource('manual');
    setLocationSearchStatus('found'); // Treat manual entry as "found" for UI logic
  }

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    // Only proceed if coordinates are available or manually entered.
    if (input.latitude === 0 && input.longitude === 0 && coordinateSource !== 'manual') {
      alert("Please enter coordinates manually or pick them on the map.");
      return;
    }
    onSubmit(input);
  }, [input, onSubmit, coordinateSource]);

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
              <input type="text" id="location" name="location" className="form-control" value={input.location} onChange={handleChange} onBlur={handleLocationBlur} required />
            </div>
            
            {locationSearchStatus === 'searching' && (
              <div className="col-12 text-light">
                <i className="bi bi-arrow-clockwise spinner-border-sm me-2"></i> Searching for coordinates...
              </div>
            )}
            
            {locationSearchStatus === 'not-found' && coordinateSource === 'none' && (
              <div className="col-12 text-light">
                <span className="text-danger">Location not automatically resolved.</span>
                <button type="button" className="btn btn-sm btn-outline-warning ms-3 me-2" onClick={handleManualEntry}>
                  Enter Coordinates Manually
                </button>
                <button type="button" className="btn btn-sm btn-outline-info" onClick={() => setShowMapPicker(true)}>
                  Pick on Map
                </button>
              </div>
            )}
            
            {(coordinateSource === 'geocoded' || coordinateSource === 'manual') && (
              <>
                <div className="col-md-4">
                  <label htmlFor="latitude" className="form-label text-light">Latitude</label>
                  <input
                    type="number"
                    id="latitude"
                    name="latitude"
                    className="form-control"
                    value={input.latitude}
                    onChange={handleChange}
                    step="0.0001"
                  />
                </div>
                <div className="col-md-4">
                  <label htmlFor="longitude" className="form-label text-light">Longitude</label>
                  <div className="input-group">
                    <input
                      type="number"
                      id="longitude"
                      name="longitude"
                      className="form-control"
                      value={input.longitude}
                      onChange={handleChange}
                      step="0.0001"
                    />
                    {/* Admin Verify Coordinates Button (Task 4) */}
                    {isAdmin && (
                      <button
                        type="button"
                        className="btn btn-outline-secondary"
                        onClick={() => window.open(`https://maps.google.com/?q=${input.latitude},${input.longitude}`, '_blank')}
                        title="Verify Location in Google Maps"
                      >
                        <i className="bi bi-globe"></i>
                      </button>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>

          <MapPicker
            show={showMapPicker}
            onClose={() => setShowMapPicker(false)}
            onSelectCoordinates={handleSelectCoordinates}
            initialLat={input.latitude || defaultInput.latitude}
            initialLon={input.longitude || defaultInput.longitude}
          />
          
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