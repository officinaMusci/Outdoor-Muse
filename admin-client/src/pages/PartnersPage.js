import {
  useState,
  useEffect
} from 'react';
import {
  Paper,
  TextField,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';

import useApi from '../services/apiHook';
import Table from '../components/Table';
import DialogForm from '../components/DialogForm';


// The API path to use
const apiPath = 'partners';


// The table columns
const tableColumns = [
  {id: 'id',  label: 'ID'},
  {id: 'created',  label: 'Créé'},
  {id: 'updated',  label: 'Mis à jour'},

  {id: 'name',  label: 'Nom'},
  {id: 'types',  label: 'Types'},
  {id: 'location',  label: 'Emplacement'},
  
  {id: 'edit',  label: ''},
  {id: 'delete',  label: ''}
];


// The empty form data to use for form reset
const emptyFormData = {
  id: undefined,
  name: '',
  types: [],
  location: {}
}


// The types available for partners
const typeList = [
  'restaurant',
  'hotel',
  'bar'
];


/**
 * Renders the partners page
 * @component
 */
export default function PartnersPage() {
  const { apiCall } = useApi();

  const [rows, setRows] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formData, setFormData] = useState(emptyFormData);
  const [formError, setFormError] = useState('');

  useEffect(() => {
    apiCall(
      `/${apiPath}`,
      'GET'
    )
    .then(response => {
      if (!response.error) {
        setRows(response.result);
      }
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleTableCreate = () => {
    setFormData(emptyFormData);
    setDialogOpen(true);
  }

  const handleTableEdit = id => {
    setFormData(rows.find(row => row.id === id));
    setDialogOpen(true);
  }

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

  const handleFormChange = (input, e) => {
    let value = e.target.value;
    
    if (input.includes('.')) {
      input = input.split('.');
      setFormData({...formData,
        [input[0]]: {
          ...formData[input[0]],
          [input[1]]: value
        }
      });

    } else {
      setFormData({...formData, [input]: value});
    }
  }

  const handleFormValidate = () => {
    if (!formData.name) { setFormError('name'); return false; }
    if (!formData.types.length) { setFormError('types'); return false; }
    if (!formData.location.lat) { setFormError('location.lat'); return false; }
    if (!formData.location.lng) { setFormError('location.lng'); return false; }
    return true;
  }

  const handleFormSubmit = () => {console.log(formData)
    if (!formError) {
      apiCall(
        formData.id ? `/${apiPath}/${formData.id}` : `/${apiPath}`,
        formData.id ? 'PUT' : 'POST',
        formData
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
  }

  const handleFormCancel = () => {
    setFormData(emptyFormData);
    setFormError('');
  }

  const inputStyle = {
    width: '100%',
    marginTop: 2
  }

  return (
    <Paper>
      <Table
        columns={tableColumns}
        rows={rows}
        onCreate={handleTableCreate}
        onEdit={handleTableEdit}
        onDelete={handleTableDelete}
      />
      <DialogForm
        open={dialogOpen}
        setOpen={setDialogOpen}
        onCancel={handleFormCancel}
        onValidate={handleFormValidate}
        onSubmit={handleFormSubmit}
        title={formData.id ? 'Modifier' : 'Créer'}
        description={''}
      >
        <TextField
          required
          value={formData.name}
          onInput={e => handleFormChange('name', e)}
          label='Nom'
          error={formError === 'name'}
          sx={inputStyle}
        />
        <FormControl sx={inputStyle}>
          <InputLabel id='types-label'>
            Types
          </InputLabel>
          <Select
            labelId='types-label'
            label='Types'
            multiple
            value={formData.types}
            onChange={e => handleFormChange('types', e)}
            error={formError === 'types'}
          >
            {typeList.map((type) => (
              <MenuItem
                key={type}
                value={type}
              >
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Box>
          <TextField
            required
            type='number'
            value={formData.location.lat}
            onInput={e => handleFormChange('location.lat', e)}
            label='Latitude'
            error={formError === 'location.lat'}
            sx={inputStyle}
          />
          <TextField
            required
            type='number'
            value={formData.location.lng}
            onInput={e => handleFormChange('location.lng', e)}
            label='Longitude'
            error={formError === 'location.lng'}
            sx={inputStyle}
          />
        </Box>
      </DialogForm>
    </Paper>
  );
}