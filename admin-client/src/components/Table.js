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
  IconButton,
  Skeleton,
  Rating,
  TableSortLabel
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
 * @property  {string}            type      The button type to render
 * @property  {integer}           rowId     The row id to which the button belongs
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

  return type === 'edit' && onEdit ?
    <IconButton
      onClick={() => onEdit(rowId)}
      sx={{
        fontSize: '1.5rem'
      }}
    >
      <EditIcon />
    </IconButton>
    :
    type === 'delete' && onDelete ?
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
 * @property  {Array}             columns    The table columns
 * @property  {Array}             rows       The table rows
 * @property  {CallableFunction}  onCreate   The function to call on create button click
 * @property  {CallableFunction}  onEdit     The function to call on edit button click
 * @property  {CallableFunction}  onDelete   The function to call on delete button click
 * @property  {boolean}           isLoading  If the table is loading
 * @component
 */
const Table = props => {
  const theme = useTheme();

  const {
    columns,
    rows,
    onCreate,
    onEdit,
    onDelete,
    isLoading
  } = props;

  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('calories');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const formatValue = (value, column) => {
    if (column === 'distance') {
      value = Number(value / 1000).toLocaleString()  + ' km';
    
    } else if (column === 'duration') {
      value = value.split(':');
      value = value.slice(0, 2).join(':')
    
    } else if (Array.isArray(value)) {
      value = value.join(', ');
      value = value.charAt(0).toUpperCase() + value.slice(1);

    } else if (typeof value === 'object') {
      value = 'lat ' + value.lat + ', lng ' + value.lng;

    } else if (
      value
      && typeof value !== 'number'
      && moment(value).isValid()
    ) {
      value = moment(new Date(value)).local().format(theme.custom.datetimeFormat);
    
    } else if (typeof value === 'boolean') {
      value = value ? <TrueIcon color='success' /> : <FalseIcon color='warning' />;
    
    } else if (typeof value === 'string' && !value.includes('@')) {
      value = value.charAt(0).toUpperCase() + value.slice(1)
    
    } else if (typeof value === 'number') {
      value = value.toLocaleString();
    }

    return value;
  }

  const descendingComparator = (a, b, orderBy) => {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }
  
  const getComparator = (order, orderBy) => {
    return order === 'desc'
      ? (a, b) => descendingComparator(a, b, orderBy)
      : (a, b) => -descendingComparator(a, b, orderBy);
  }
  
  const stableSort = (array, comparator) => {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) {
        return order;
      }
      return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
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
                  sortDirection={orderBy === column.id ? order : false}
                  sx={{
                    color: theme.palette.secondary.main,
                    fontWeight: 700,
                    borderBottomColor: theme.palette.grey[600]
                  }}
                >
                  <TableSortLabel
                    active={orderBy === column.id}
                    direction={orderBy === column.id ? order : 'asc'}
                    onClick={e => handleRequestSort(e, column.id)}
                  >
                    {column.label}
                  </TableSortLabel>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {isLoading ?
              Array(rowsPerPage).fill('').map((_, index) => (
                <TableRow
                  hover
                  role='checkbox'
                  tabIndex={-1}
                  key={index}
                >
                  {columns.map(column => (
                    <TableCell
                      key={column.id}
                    >
                      <Skeleton animation='wave' />
                    </TableCell>
                  ))}
                </TableRow>
              ))
              :
              stableSort(rows, getComparator(order, orderBy))
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map(row => (
                <TableRow
                  hover
                  role='checkbox'
                  tabIndex={-1}
                  key={row.id}
                >
                  {columns.map(column => {
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
                          ['rating', 'average_rating'].includes(column.id) ?
                            <Rating value={value} precision={.5} readOnly />
                            :
                            formatValue(value, column.id)
                        }
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))}
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
        {onCreate ?
          <TableCreateButton
            onCreate={onCreate}
          />
          :
          <Box />
        }
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