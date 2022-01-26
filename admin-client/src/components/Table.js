import { useState } from 'react';
import {
  useTheme,
  Paper,
  Box,
  TableContainer,
  Table as MuiTable,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TablePagination,
  IconButton
} from '@mui/material';
import {
  Add as CreateIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Check as TrueIcon,
  Close as FalseIcon
} from '@mui/icons-material';
import moment from 'moment';


/**
 * Renders a button to create a new table row
 * @property  {CallableFunction}  onCreate  The function to call on button click
 * @component
 */
const TableCreateButton = props => {
  const {
    onCreate
  } = props;

  return (
    <IconButton
      onClick={onCreate}
      sx={{
        fontSize: '1.5rem'
      }}
    >
      <CreateIcon />
    </IconButton>
  );
}


/**
 * Renders a button to edit or delete a table row
 * @property  {string}            type          The button type to render
 * @property  {integer}           rowId         The row id to which the button belongs
 * @property  {CallableFunction}  onEdit    The function to call on edit button click
 * @property  {CallableFunction}  onDelete  The function to call on delete button click
 * @component
 */
const TableButton = props => {
  const {
    type,
    rowId,
    onEdit,
    onDelete
  } = props;

  return type === 'edit' ?
    <IconButton
      onClick={() => onEdit(rowId)}
      sx={{
        fontSize: '1.5rem'
      }}
    >
      <EditIcon />
    </IconButton>
    :
    type === 'delete' ?
      <IconButton
        onClick={() => onDelete(rowId)}
      sx={{
        fontSize: '1.5rem'
      }}
      >
        <DeleteIcon />
      </IconButton>
      :
      null
    ;
}


/**
 * Renders a table
 * @property  {Array}             columns       The table columns
 * @property  {Array}             rows          The table rows
 * @property  {CallableFunction}  onCreate  The function to call on create button click
 * @property  {CallableFunction}  onEdit    The function to call on edit button click
 * @property  {CallableFunction}  onDelete  The function to call on delete button click
 * @component
 */
const Table = props => {
  const theme = useTheme();

  const {
    columns,
    rows,
    onCreate,
    onEdit,
    onDelete
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
    
    } else if (typeof value === 'boolean') {
      value = value ? <TrueIcon color='success' /> : <FalseIcon color='warning' />;
    
    } else if (typeof value === 'string' && !value.includes('@')) {
      value = value.charAt(0).toUpperCase() + value.slice(1)
    }

    return value;
  }

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: '80vh' }}>
        <MuiTable stickyHeader>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  sx={{
                    fontWeight: 700,
                    borderBottomColor: theme.palette.grey[600]
                  }}
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
                              onEdit={onEdit}
                              onDelete={onDelete}
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
        </MuiTable>
      </TableContainer>
      <Box
        sx={{
          paddingLeft: .5,
          paddingRight: .5,
          borderTop: '1px solid ' + theme.palette.grey[600],
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap'
        }}
      >
        <TableCreateButton
          onCreate={onCreate}
        />
        <TablePagination
          rowsPerPageOptions={[25, 50, 100]}
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          component='div'
        />
      </Box>
    </Paper>
  );
}

export default Table;