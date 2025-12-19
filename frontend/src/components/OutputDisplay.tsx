import React from 'react';
import AstrologicalChart, { PlanetPosition, Aspect } from '../types/AstrologicalChart';
import HoroscopeNarrative from '../types/HoroscopeNarrative';

interface OutputDisplayProps {
  chart: AstrologicalChart;
  narrative: HoroscopeNarrative;
  onReset: () => void;
  isAdmin: boolean;
}

const ChartSection: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div className="card bg-secondary text-white mb-4 shadow-sm">
    <div className="card-header border-light-subtle">
      <h4 className="mb-0 text-primary">{title}</h4>
    </div>
    <div className="card-body">
      {children}
    </div>
  </div>
);

const renderPlanetPositions = (positions: PlanetPosition[]) => (
  <ul className="list-group list-group-flush border-0">
    {positions.map((p, index) => (
      <li key={index} className="list-group-item bg-secondary text-light d-flex justify-content-between align-items-center border-0">
        <span className="fw-bold">{p.name}</span>
        <span>{p.degree.toFixed(2)}° in {p.sign}</span>
      </li>
    ))}
  </ul>
);

const renderAspects = (aspects: Aspect[]) => (
  <ul className="list-group list-group-flush border-0">
    {aspects.map((a, index) => (
      <li key={index} className="list-group-item bg-secondary text-light d-flex justify-content-between align-items-center border-0">
        <span className="fw-bold text-warning">{a.type}</span>
        <span>{a.planet1} <span className="text-muted">to</span> {a.planet2} (Orb: {a.orb.toFixed(2)}°)</span>
      </li>
    ))}
  </ul>
);


const renderNarrativeSections = (narrative: HoroscopeNarrative) => (
  <div>
    {narrative.sections.map((section, index) => (
      <div key={index} className="mb-4 p-3 bg-dark-subtle rounded">
        <h5 className="text-info">{section.title}</h5>
        <p className="text-light">{section.content}</p>
        {section.sourceRuleOrPromptId && (
          <small className="text-muted">Source ID: {section.sourceRuleOrPromptId}</small>
        )}
      </div>
    ))}
  </div>
);


const OutputDisplay: React.FC<OutputDisplayProps> = ({ chart, narrative, onReset, isAdmin }) => {
  return (
    <div className="bg-dark p-4 rounded shadow-lg border border-success">
      <div className="d-flex justify-content-between align-items-center mb-5">
        <h2 className="text-success mb-0">Step 2: Analysis Results</h2>
        <button className="btn btn-outline-light" onClick={onReset}>
          <i className="bi bi-arrow-left"></i> Start New Calculation
        </button>
      </div>

      {/* Narrative Synthesis Section */}
      <ChartSection title={narrative.title}>
        <p className="lead text-warning">{narrative.summary}</p>
        <hr className="text-muted"/>
        {renderNarrativeSections(narrative)}

        {/* PM Debug Info: Raw AI Output */}
        {isAdmin && (
          <div className="mt-5 pt-3 border-top border-light-subtle">
            <h5 className="text-danger">PM DEBUG: Raw AI Output</h5>
            <pre className="text-white bg-black p-3 rounded">{narrative.rawAiOutput}</pre>
          </div>
        )}
      </ChartSection>

      {/* Chart Calculation Section */}
      <div className="row">
        <div className="col-lg-12">
          <ChartSection title="Astrological Chart Data">
            <p className="text-light">
              <strong>House System:</strong> {chart.houseSystem} | <strong>Location:</strong> {chart.birthLocation}
            </p>
            <div className="row mt-3">
              <div className="col-md-6">
                <h6 className="text-info">Planetary Positions</h6>
                {renderPlanetPositions(chart.positions)}
              </div>
              <div className="col-md-6">
                <h6 className="text-info">Key Aspects</h6>
                {renderAspects(chart.aspects)}
              </div>
            </div>
          </ChartSection>
        </div>
      </div>

    </div>
  );
};

export default OutputDisplay;