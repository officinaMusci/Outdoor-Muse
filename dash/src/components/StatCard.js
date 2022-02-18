import {
  useTheme,
  Paper,
  Typography,
  Divider
} from '@mui/material';

import Plot from 'react-plotly.js';


/**
 * Renders a card showing time statistics
 * @property  {string}  title  The card title
 * @property  {Array}   data   The stats to show
 * @property  {string}  type   The stats type to use (defaults to 'scatter')
 * @property  {string}  mode   The stats mode to use (defaults to 'lines')
 * @component
 */
const StatCard = props => {
  const theme = useTheme();

  const {
    title,
    data,
    type='scatter',
    mode='lines'
  } = props;

  return (
    <Paper sx={{
      padding: theme.spacing(1)
    }}>
      <Typography
        variant='h5'
        color='secondary'
        align='center'
      >
        {title}
      </Typography>
      <Divider light sx={{ mt: 1, mb: 1 }} />
      <Plot
        data={[
          {
            x: data ? data.map(datum => datum[0]) : [],
            y: data ? data.map(datum => datum[1]) : [],
            type: type,
            mode: type === 'scatter' ? mode : '',
            //marker: { color: theme.palette.secondary.main },
          }
        ]}
        layout={{
          responsive: true,
          autosize: true,
          useResizeHandler: true,
          margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 0
          },
          xaxis: {
            rangeselector: type === 'scatter',
            rangeslider: type === 'scatter',
          }
        }}
        style={{width: '100%', height: '100%'}}
      />
    </Paper>
  )
}

export default StatCard;