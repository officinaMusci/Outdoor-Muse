import {
  useState,
  useEffect
} from 'react';
import {
  Divider,
  Skeleton
} from '@mui/material';

import useApi from '../services/apiHook';
import Table from '../components/Table';
import MapCard from '../components/MapCard';


// The API path to use
const apiPath = 'places';


// The table columns
const tableColumns = [
  { id: 'id', label: 'ID', align: 'right' },

  { id: 'name', label: 'Nom' },
  { id: 'types', label: 'Catégories' },
  { id: 'difficulty', label: 'Difficulté', align: 'right' },
  { id: 'duration', label: 'Durée', align: 'right' },
  { id: 'distance', label: 'Distance', align: 'right' },
  { id: 'location', label: 'Emplacement' },

  { id: 'review_count', label: 'Avis', align: 'right' },
  { id: 'average_rating', label: 'Évaluation (μ)' },
  { id: 'query_count', label: 'Apparitions', align: 'right' }
];


/**
 * Renders the places page
 * @component
 */
export default function PlacesPage() {
  const { apiCall } = useApi();

  const [isLoading, setIsLoading] = useState(true);
  const [rows, setRows] = useState([]);

  useEffect(() => {
    setIsLoading(true);
    apiCall(
      `/${apiPath}`,
      'GET'
    )
      .then(response => {
        setIsLoading(false);
        if (!response.error) {
          setRows(response.result);
        }
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      {isLoading ?
        <Skeleton
          animation='wave'
          sx={{
            height: 500,
            transform: 'none'
          }}
        />
        :
        <MapCard data={rows} />
      }
      <Divider light sx={{ mt: 3, mb: 3 }} />
      <Table
        columns={tableColumns}
        rows={rows}
        isLoading={isLoading}
      />
    </>
  );
}