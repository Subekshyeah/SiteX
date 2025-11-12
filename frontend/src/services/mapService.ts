import axios from 'axios';

const MAP_API_BASE_URL = 'https://api.example.com/maps'; // Replace with actual map API base URL

export const fetchMapData = async (location: string) => {
    try {
        const response = await axios.get(`${MAP_API_BASE_URL}/data`, {
            params: { location }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching map data:', error);
        throw error;
    }
};

export const fetchNearbyPlaces = async (location: string) => {
    try {
        const response = await axios.get(`${MAP_API_BASE_URL}/nearby`, {
            params: { location }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching nearby places:', error);
        throw error;
    }
};

export const getDirections = async (origin: string, destination: string) => {
    try {
        const response = await axios.get(`${MAP_API_BASE_URL}/directions`, {
            params: { origin, destination }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching directions:', error);
        throw error;
    }
};