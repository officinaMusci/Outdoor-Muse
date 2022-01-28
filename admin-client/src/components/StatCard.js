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
 * @component
 */
const StatCard = props => {
  const theme = useTheme();

  const {
    title,
    data
  } = props;

  return (
    <Paper sx={{
      padding: theme.spacing(1)
    }}>
      <Typography
        variant='h5'
        color='secondary'
        fontWeight={700}
      >
        {title}
      </Typography>
      <Divider light sx={{ mt: 1, mb: 1 }} />
      <Plot
        data={[
          {
            x: data ? data.map(datum => datum.datetime) : [],
            y: data ? data.map(datum => datum.count) : [],
            type: 'scatter',
            mode: 'lines',
            marker: { color: theme.palette.secondary.main },
          }
        ]}
        layout={{
          responsive: true,
          autosize: true,
          useResizeHandler: true,
          margin: {
            l: 10,
            r: 10,
            b: 10,
            t: 10,
            pad: 0
          },
          xaxis: {
            rangeselector: true,
            rangeslider: true,
          }
        }}
        style={{width: '100%', height: '100%'}}
      />
    </Paper>
  )
}

export default StatCard;