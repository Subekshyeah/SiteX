import { useContext } from 'react';
import { MapContext } from '../contexts/MapContext';

const useMap = () => {
    const { map, setMap, markers, setMarkers } = useContext(MapContext);

    const addMarker = (marker) => {
        setMarkers((prevMarkers) => [...prevMarkers, marker]);
    };

    const removeMarker = (markerId) => {
        setMarkers((prevMarkers) => prevMarkers.filter(marker => marker.id !== markerId));
    };

    const clearMarkers = () => {
        setMarkers([]);
    };

    return {
        map,
        addMarker,
        removeMarker,
        clearMarkers,
    };
};

export default useMap;