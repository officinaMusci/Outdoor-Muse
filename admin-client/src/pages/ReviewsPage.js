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
  const apiPath = 'reviews';
  
  
  // The table columns
  const tableColumns = [
    {id: 'id', label: 'ID', align: 'right'},
    {id: 'created', label: 'Créé'},
    {id: 'updated', label: 'Mis à jour'},
  
    {id: 'comment', label: 'Commentaire'},
    {id: 'rating', label: 'Évaluation'},

    //{id: 'parent', label: 'Réponse à'}, 
    {id: 'partner_name', label: 'Partenaire'},
    {id: 'place_name', label: 'Randonnée'},
  
    {id: 'delete', label: '', align: 'center'}
  ];
  
  
  /**
   * Renders the reviews page
   * @component
   */
  export default function ReviewPage() {
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
  
    const handleTableDelete = id => {
      apiCall(
        `/${apiPath}/${id}`,
        'DELETE'
      )
        .then(response => {
          if (!response.error) {
            apiCall(
              `/${apiPath}`,
              'GET'
            )
              .then(response => {
                if (!response.error) {
                  setRows(response.result);
                }
              });
          }
        });
    }
  
    return (
      <Paper>
        <Table
          columns={tableColumns}
          rows={rows}
          onDelete={handleTableDelete}
          isLoading={isLoading}
        />
      </Paper>
    );
  }