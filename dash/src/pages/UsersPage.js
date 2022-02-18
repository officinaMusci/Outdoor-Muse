import {
  useState,
  useEffect
} from 'react';
import {
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';

import useApi from '../services/apiHook';
import Table from '../components/Table';
import DialogForm from '../components/DialogForm';


// The API path to use
const apiPath = 'users';


// The table columns
const tableColumns = [
  {id: 'id', label: 'ID', align: 'right'},
  {id: 'created', label: 'Créé'},
  {id: 'updated', label: 'Mis à jour'},

  {id: 'email', label: 'E-mail'},
  {id: 'confirmed', label: 'Confirmé', align: 'center'},
  {id: 'role', label: 'Rôle'},
  {id: 'name', label: 'Nom'},
  {id: 'points', label: 'Points', align: 'right'},

  {id: 'edit', label: '', align: 'center'},
  {id: 'delete', label: '', align: 'center'}
];


// The empty form data to use for form reset
const emptyFormData = {
  id: undefined,
  email: '',
  password: '',
  role: 'user',
  name: '',
  points: 0
}


// The roles available for users
const roleList = [
  'admin',
  'user'
];


/**
 * Renders the users page
 * @component
 */
export default function UsersPage() {
  const { apiCall } = useApi();

  const [isLoading, setIsLoading] = useState(true);
  const [rows, setRows] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formData, setFormData] = useState(emptyFormData);
  const [formError, setFormError] = useState('');

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
      setFormData({
        ...formData,
        [input[0]]: {
          ...formData[input[0]],
          [input[1]]: value
        }
      });

    } else {
      setFormData({ ...formData, [input]: value });
    }
  }

  const handleFormValidate = () => {
    if (!formData.email) { setFormError('email'); return false; }
    if (!formData.role) { setFormError('role'); return false; }
    if (!formData.name) { setFormError('name'); return false; }
    if (typeof formData.points !== 'number') { setFormError('points'); return false; }

    return true;
  }

  const handleFormSubmit = () => {
    console.log(formData)
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
        isLoading={isLoading}
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
          value={formData.email}
          onInput={e => handleFormChange('email', e)}
          label='Adresse e-mail'
          error={formError === 'email'}
          sx={inputStyle}
        />
        <FormControl sx={inputStyle}>
          <InputLabel id='role-label'>
            Rôle
          </InputLabel>
          <Select
            labelId='role-label'
            label='Rôle'
            value={formData.role}
            onChange={e => handleFormChange('role', e)}
            error={formError === 'role'}
          >
            {roleList.map((role) => (
              <MenuItem
                key={role}
                value={role}
              >
                {role.charAt(0).toUpperCase() + role.slice(1)}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          required
          value={formData.name}
          onInput={e => handleFormChange('name', e)}
          label='Nom'
          error={formError === 'name'}
          sx={inputStyle}
        />
        <TextField
          required
          value={formData.points}
          onInput={e => handleFormChange('points', e)}
          label='Points'
          error={formError === 'points'}
          sx={inputStyle}
        />
      </DialogForm>
    </Paper>
  );
}