// Type definition for processing steps data structure
export interface CoordinatesData {
    latitude: number;
    longitude: number;
    timezone: string;
}

export interface TimeCorrectionData {
    local_time: string;
    universal_time: string;
    offset: string;
}

export interface ChartGenerationData {
    planets: Array<{
        name: string;
        degree: number;
        sign: string;
    }>;
    houses: Array<{
        number: number;
        degree: number;
        sign: string;
    }>;
}

export interface RelationshipMappingData {
    aspects: Array<{
        planet1: string;
        planet2: string;
        type: string;
        orb: number;
    }>;
}

export interface PMConfigData {
    house_system: string;
    ephemeris_source: string;
    interpretation_engine: string;
    ai_model: string;
    temperature: number;
}

export interface ProcessingSteps {
    coordinates: CoordinatesData;
    time_correction: TimeCorrectionData;
    chart_generation: ChartGenerationData;
    relationship_mapping: RelationshipMappingData;
    pm_config: PMConfigData;
}

export default ProcessingSteps;