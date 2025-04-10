import React from 'react';
import { Map, Source, Layer } from 'react-map-gl';
import maplibregl from 'maplibre-gl';

const MapComponent = ({ route }) => {
    return (
        <Map
            mapLib={maplibregl}
            initialViewState={{
                longitude: -95.7129,
                latitude: 37.0902,
                zoom: 3
            }}
            style={{ width: '100%', height: 400 }}
            mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        >
            {route && (
                <Source
                    id="route"
                    type="geojson"
                    data={{
                        type: 'Feature',
                        properties: {},
                        geometry: route
                    }}
                >
                    <Layer
                        id="route"
                        type="line"
                        paint={{
                            'line-color': '#3b82f6',
                            'line-width': 4
                        }}
                    />
                </Source>
            )}
        </Map>
    );
};

export default MapComponent;