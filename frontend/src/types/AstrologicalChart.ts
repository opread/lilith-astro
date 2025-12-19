// Mock type definition for Astrological Chart data structure
export interface PlanetPosition {
    name: string;
    sign: string;
    degree: number;
}

export interface Aspect {
    planet1: string;
    planet2: string;
    type: string;
    orb: number;
}

interface AstrologicalChart {
    birthDate: string;
    birthTime: string;
    birthLocation: string;
    houseSystem: string;
    positions: PlanetPosition[];
    aspects: Aspect[];
}

export default AstrologicalChart;