import axios from 'axios';
import AstrologicalChart from './types/AstrologicalChart';
import HoroscopeNarrative from './types/HoroscopeNarrative';
import { UserInput } from './components/InputForm';

const API_BASE_URL = 'http://localhost:8000/api/v1'; // Assuming the backend runs on port 8000

interface ProcessFlowResult {
  chart: AstrologicalChart;
  narrative: HoroscopeNarrative;
}

/**
 * Sends user input and AI/Calc parameters to the backend for processing.
 * @param input The combined user and PM parameters.
 * @returns A promise resolving to the generated chart and narrative.
 */
export const processFlow = async (input: UserInput): Promise<ProcessFlowResult> => {
  console.log('Sending request to backend with parameters:', input);

  // --- MOCK API RESPONSE ---
  // Since we haven't installed dependencies or started the server yet,
  // we use a delayed mock response for UI development.

  return new Promise((resolve) => {
    setTimeout(() => {
      // Simulate successful calculation and narrative synthesis
      const mockChart: AstrologicalChart = {
        birthDate: input.date,
        birthTime: input.time,
        birthLocation: input.location,
        houseSystem: input.houseSystem,
        positions: [
          { name: 'Sun', sign: 'Aries', degree: 15.5 },
          { name: 'Moon', sign: 'Libra', degree: 22.1 },
          { name: 'Ascendant', sign: 'Cancer', degree: 5.0 },
        ],
        aspects: [
          { planet1: 'Sun', planet2: 'Moon', type: 'Opposition', orb: 1.6 },
        ]
      };

      const mockNarrative: HoroscopeNarrative = {
        title: `Your Destiny (Generated with Temperature: ${input.aiTemperature})`,
        summary: `A high-level summary generated using ${input.interpretationEngine}.`,
        sections: [
          {
            title: 'I. Core Identity (Sun in Aries)',
            content: 'The Sun in Aries placement suggests a dynamic and pioneering spirit. This energy often translates into leadership and a need for independent action. It\'s a fire sign emphasizing initiation.',
            sourceRuleOrPromptId: 'R-SUN-ARIES-01'
          },
          {
            title: 'II. Emotional Landscape (Moon in Libra)',
            content: 'The Moon in Libra indicates a need for harmony and balance in emotional expression. You seek fairness and partnership, often prioritizing relationships.',
            sourceRuleOrPromptId: 'R-MOON-LIBRA-03'
          },
          {
            title: 'III. Synthesized Narrative (AI Layer)',
            content: `The opposition between the Sun and Moon creates a push-pull dynamic. This narrative was synthesized using the AI with a focus on ${input.narrativeStyle}. The system temperature was set to ${input.aiTemperature} to control creativity.`,
            sourceRuleOrPromptId: 'P-OPPOSITION-AI-01'
          }
        ],
        rawAiOutput: '{"sun_in_aries": "dynamic", "moon_in_libra": "balanced", "model_version": "GPT-4.5-LILITH"}'
      };

      resolve({ chart: mockChart, narrative: mockNarrative });
    }, 1500); // Simulate network delay
  });
  // --- END MOCK API RESPONSE ---
};