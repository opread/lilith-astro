// Mock type definition for Horoscope Narrative data structure
interface HoroscopeNarrative {
    title: string;
    summary: string;
    sections: {
        title: string;
        content: string;
        // Allows PM to check which rule or prompt generated this part
        sourceRuleOrPromptId?: string; 
    }[];
    // Raw output from the AI for debug purposes
    rawAiOutput: string; 
}

export default HoroscopeNarrative;