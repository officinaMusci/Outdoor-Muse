import {
  useTheme,
  Paper,
  Typography,
  Divider
} from '@mui/material';


/**
 * Renders a data card
 * @property  {number}  count        The data count to show
 * @property  {string}  description  The description of the count
 * @property  {string}  caption      The optional secondary caption
 * @component
 */
const DataCard = props => {
  const theme = useTheme();

  const {
    count,
    description,
    caption
  } = props;

  const paperStyle = {
    padding: theme.spacing(1),
    textAlign: 'center'
  }

  return (
    <Paper sx={paperStyle}>
      <Typography
        variant='h2'
        color='secondary'
      >
        {count.toLocaleString()}
      </Typography>
      <Typography variant='h6'>
        {description}
      </Typography>
      {caption ?
        <>
          <Divider light sx={{ mt: 1, mb: 1 }} />
          <Typography variant='caption'>
            {caption}
          </Typography>
        </>
        :
        null
      }
    </Paper>
  )
}

export default DataCard;