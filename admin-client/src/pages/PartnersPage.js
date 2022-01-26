import {
  useState,
  useEffect
} from 'react';
import {
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TablePagination,
  IconButton
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import moment from 'moment';

import useApi from '../services/Api';


/**
 * 
 * @component
 */
const TableButton = props => {
  const {
    type,
    rowId,
    handleEdit,
    handleDelete
  } = props;

  return type === 'edit' ?
    <IconButton onClick={() => handleEdit(rowId)}>
      <EditIcon />
    </IconButton>
    :
    type === 'delete' ?
      <IconButton onClick={() => handleDelete(rowId)}>
        <DeleteIcon />
      </IconButton>
      :
      null
  ;
}


/**
 * 
 * @component
 */
const PartnersTable = props => {
  const {
    columns,
    rows,
    handleEdit,
    handleDelete
  } = props;

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const formatValue = value => {
    if (Array.isArray(value)) {
      value = value.join(', ');
      value = value.charAt(0).toUpperCase() + value.slice(1);
      
    } else if (typeof value === 'object') {
      value = 'lat ' + value.lat + ', lng ' + value.lng;

    } else if (
      value
      && typeof value !== 'number'
      && moment(value).isValid()
    ) {
      value = moment(new Date(value)).format('DD.MM.YYYY HH:mm');
    }

    return value;
  }

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: '80vh' }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row) => {
                return (
                  <TableRow
                    hover
                    role='checkbox'
                    tabIndex={-1}
                    key={row.id}
                  >
                    {columns.map((column) => {
                      const value = row[column.id];
                      return (
                        <TableCell
                          key={column.id}
                          align={column.align}
                        >
                          {['edit', 'delete'].includes(column.id) ?
                              <TableButton
                                type={column.id}
                                rowId={row.id}
                                handleEdit={handleEdit}
                                handleDelete={handleDelete}
                              />
                              :
                              formatValue(value)
                          }
                        </TableCell>
                      );
                    })}
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[25, 50, 100]}
        component='div'
        count={rows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}


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

  useEffect(async () => {
    let response = await apiCall(
      '/partners',
      'GET'
    );
    setRows(response);
  }, []);

  const handleEdit = async id => {

  }

  const handleDelete = async id => {
    let hasDeleted = await apiCall(
      '/partners/' + id,
      'DELETE'
    );

    if (hasDeleted) {
      let response = await apiCall(
        '/partners',
        'GET'
      );

      setRows(response);
    }
  }

  return (
    <Paper>
      <PartnersTable
        columns={columns}
        rows={rows}
        handleEdit={handleEdit}
        handleDelete={handleDelete}
      />
    </Paper>
  );
}