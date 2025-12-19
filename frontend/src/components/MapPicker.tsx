import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api';

// Define map container styles
const containerStyle = {
  width: '100%',
  height: '50vh',
};

// Required libraries for the Google Maps API loader
const libraries: ("places" | "drawing" | "geometry" | "visualization")[] = ["places"];
const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || ''; 

interface MapPickerProps {
  show: boolean;
  onClose: () => void;
  onSelectCoordinates: (latitude: number, longitude: number) => void;
  initialLat: number;
  initialLon: number;
}

const MapPicker: React.FC<MapPickerProps> = ({ show, onClose, onSelectCoordinates, initialLat, initialLon }) => {
  // Use local state to manage the selected coordinates within the modal
  const [selectedLat, setSelectedLat] = useState(initialLat);
  const [selectedLon, setSelectedLon] = useState(initialLon);
  const [map, setMap] = useState<google.maps.Map | null>(null);

  // Sync internal state with props when modal opens or initial values change
  useEffect(() => {
    setSelectedLat(initialLat);
    setSelectedLon(initialLon);
  }, [initialLat, initialLon]);

  // Load the Google Maps JS API script
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: GOOGLE_MAPS_API_KEY,
    libraries: libraries,
  });

  const handleSelect = useCallback(() => {
    onSelectCoordinates(selectedLat, selectedLon);
    onClose();
  }, [selectedLat, selectedLon, onSelectCoordinates, onClose]);

  const onMapClick = useCallback((e: google.maps.MapMouseEvent) => {
    if (e.latLng) {
      const newLat = e.latLng.lat();
      const newLon = e.latLng.lng();
      setSelectedLat(parseFloat(newLat.toFixed(4)));
      setSelectedLon(parseFloat(newLon.toFixed(4)));
    }
  }, []);

  const onLoad = useCallback(function callback(map: google.maps.Map) {
    // Center map on the initial coordinates, falling back to a default view (zoom 2) if coordinates are zero (indicating no location set yet)
    if (initialLat !== 0 && initialLon !== 0) {
        map.setCenter({ lat: initialLat, lng: initialLon });
        map.setZoom(10);
    } else {
        map.setCenter({ lat: 0, lng: 0 }); 
        map.setZoom(2);
    }
    setMap(map);
  }, [initialLat, initialLon]);

  const onUnmount = useCallback(function callback(map: google.maps.Map) {
    setMap(null);
  }, []);

  const mapComponent = isLoaded ? (
    <div className="text-center p-2 bg-light text-dark rounded border">
        <p className="fw-bold mb-2">Click on the map to set coordinates.</p>
        <div style={{ position: 'relative' }}>
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={{ lat: selectedLat, lng: selectedLon }}
                zoom={5} // Base zoom level
                onLoad={onLoad}
                onUnmount={onUnmount}
                onClick={onMapClick}
                options={{ streetViewControl: false, mapTypeControl: false, fullscreenControl: false }}
            >
                <Marker 
                    position={{ lat: selectedLat, lng: selectedLon }} 
                />
            </GoogleMap>
            <div style={{ position: 'absolute', top: '10px', left: '10px', zIndex: 10, background: 'rgba(0, 0, 0, 0.7)', padding: '5px', borderRadius: '5px', color: 'white' }}>
                Selected: Lat: {selectedLat.toFixed(4)}, Lon: {selectedLon.toFixed(4)}
            </div>
        </div>
    </div>
  ) : (
    <div style={containerStyle} className="d-flex justify-content-center align-items-center bg-secondary-subtle border">
        <p>Loading Google Map...</p>
    </div>
  );

  return (
    <div className={`modal ${show ? 'd-block' : 'd-none'}`} tabIndex={-1} role="dialog" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
      <div className="modal-dialog modal-lg modal-dialog-centered" role="document">
        <div className="modal-content bg-dark border-primary">
          <div className="modal-header text-white border-primary">
            <h5 className="modal-title">Pick Coordinates on Map</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose} aria-label="Close"></button>
          </div>
          <div className="modal-body text-white">
            {mapComponent}
          </div>
          <div className="modal-footer border-primary">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="button" className="btn btn-primary" onClick={handleSelect} disabled={!selectedLat || !selectedLon}>
              Use Coordinates ({selectedLat.toFixed(4)}, {selectedLon.toFixed(4)})
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MapPicker;