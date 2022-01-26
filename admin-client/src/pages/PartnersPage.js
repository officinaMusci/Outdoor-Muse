import {
  useState,
  useEffect
} from 'react';
import {
  Paper
} from '@mui/material';

import useApi from '../services/apiHook';
import Table from '../components/Table';


/**
 * Renders the partners page
 * @component
 */
export default function PartnersPage() {
  const { apiCall } = useApi();

  const [rows, setRows] = useState([]);

  const columns = [
    {id: 'id',  label: 'ID'},
    {id: 'created',  label: 'Créé'},
    {id: 'updated',  label: 'Mis à jour'},
    {id: 'name',  label: 'Nom'},
    {id: 'types',  label: 'Types'},
    {id: 'location',  label: 'Emplacement'},
    {id: 'edit',  label: 'Modifier'},
    {id: 'delete',  label: 'Supprimer'}
  ];

  useEffect(() => {
    apiCall(
      '/partners',
      'GET'
    )
    .then(response => {
      if (!response.error) {
        setRows(response.result);
      }
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleCreate = () => {

  }

  const handleEdit = id => {

  }

  const handleDelete = id => {
    apiCall(
      '/partners/' + id,
      'DELETE'
    )
    .then(response => {
      if (!response.error) {
        apiCall(
          '/partners',
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
        columns={columns}
        rows={rows}
        handleCreate={handleCreate}
        handleEdit={handleEdit}
        handleDelete={handleDelete}
      />
    </Paper>
  );
}