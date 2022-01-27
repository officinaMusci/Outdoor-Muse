import {
    useState,
    useEffect
  } from 'react';
  import {
    Paper
  } from '@mui/material';
  
  import useApi from '../services/apiHook';
  import Table from '../components/Table';
  
  
  // The API path to use
  const apiPath = 'places';
  
  
  // The table columns
  const tableColumns = [
    {id: 'id',  label: 'ID', align: 'right'},
  
    {id: 'name',  label: 'Nom'},
    {id: 'types',  label: 'Catégories'},
    {id: 'difficulty', label: 'Difficulté', align: 'right'},
    {id: 'duration', label: 'Durée', align: 'right'},
    {id: 'distance', label: 'Distance', align: 'right'},
    {id: 'location',  label: 'Emplacement'},

    {id: 'average_rating',  label: 'Évaluation (μ)'},
    {id: 'query_count',  label: 'Apparitions', align: 'right'}
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
      <Paper>
        <Table
          columns={tableColumns}
          rows={rows}
          isLoading={isLoading}
        />
      </Paper>
    );
  }