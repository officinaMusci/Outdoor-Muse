import {
  useTheme,
  Paper
} from '@mui/material';
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup
} from 'react-leaflet'
import L from 'leaflet';
import MarkerClusterGroup from 'react-leaflet-markercluster';

import 'leaflet/dist/leaflet.css';
import 'react-leaflet-markercluster/dist/styles.min.css';


delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});


const MapCard = props => {
  const theme = useTheme();

  const {
    data
  } = props;

  return (
    <Paper sx={{
      height: 550,
      padding: theme.spacing(1)
    }}>
      <MapContainer
        center={[46.800663464, 8.222665776]}
        zoom={8}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MarkerClusterGroup>
          {data.map(datum => (
            <Marker
              key={datum.id}
              position={[
                datum.location.lat, 
                datum.location.lng
              ]}
            >
              <Popup>
                {datum.name}
              </Popup>
            </Marker>
          ))}
        </MarkerClusterGroup>
      </MapContainer>
    </Paper>
  );
}

export default MapCard;