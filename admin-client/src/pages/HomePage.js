import {
  useState,
  useEffect
} from 'react';
import {
  useTheme,
  Grid,
  Typography,
  Divider,
  Skeleton,
  Paper
} from '@mui/material';
import {
  Landscape as DecorativeIcon,
} from '@mui/icons-material';

import useApi from '../services/apiHook';
import DataCard from '../components/DataCard';


/**
 * Renders the home page
 * @component
 */
export default function HomePage() {
  const theme = useTheme();
  const { apiCall } = useApi();
  
  const [isLoading, setIsLoading] = useState(true);
  const [overviewData, setOverviewData] = useState();

  useEffect(() => {
    setIsLoading(true);
    apiCall(
      `/statistics/overview`,
      'GET'
    )
    .then(response => {
      setIsLoading(false);
      if (!response.error) {
        setOverviewData(response.result);
      }
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Paper sx={{
        backgroundColor: 'rgba(0,0,0,.5)',
        p: 5,
        mt: 3,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        <DecorativeIcon
          sx={{
            fontSize: 100,
            color: theme.palette.secondary.contrastText
          }}
        />
        <Typography
          variant='h4'
          align='center'
          sx={{
            color: theme.palette.secondary.contrastText,
            textShadow: `0 0 3px ${theme.palette.grey[900]}`
          }}
        >
          {isLoading ?
            <Skeleton
              animation='wave'
              sx={{
                width: 200,
                backgroundColor: 'rgba(255, 255, 255, .5)',
                margin: 'auto'
              }}
            />
            :
            `${theme.custom.appName} :`
          }
        </Typography>
        <Typography
          variant='h2'
          align='center'
          sx={{
            color: theme.palette.secondary.contrastText,
            textShadow: `0 0 5px ${theme.palette.grey[800]}`,
          }}
        >
          {isLoading ?
            <Skeleton
              animation='wave'
              sx={{
                width: 600,
                backgroundColor: 'rgba(255, 255, 255, .5)',
                margin: 'auto'
              }}
            />
            :
            'Une montagne de données'
          }
        </Typography>
      </Paper>
      <Divider light sx={{ mt: 3, mb: 3 }} />
      <Grid container spacing={2}>
        {isLoading ?
          Array(5).fill('').map((_, index) => (
            <Grid
              key={index}
              item
              xs={12}
              md={6}
              lg={4}
              height='fit-content'
            >
              <Skeleton
                animation='wave'
                sx={{
                  height: 150,
                  backgroundColor: 'rgba(255, 255, 255, .5)',
                  transform: 'none'
                }}
              />
            </Grid>
          ))
          :
          overviewData ?
            <>
              <Grid item xs={12} md={6} lg={4}>
                <DataCard
                  count={overviewData.reviews.total_count}
                  description='avis'
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <DataCard
                  count={overviewData.places.total_count}
                  description='randonnées'
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <DataCard
                  count={overviewData.partners.total_count}
                  description='partenaires'
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <DataCard
                  count={overviewData.users.total_count}
                  description='utilisateurs'
                  caption={`Dont ${overviewData.users.confirmed_count.toLocaleString()} confirmés`}
                />
              </Grid>
              <Grid item xs={12} md={6} lg={4}>
                <DataCard
                  count={overviewData.queries.total_count}
                  description='recherches'
                  caption={`Dont ${overviewData.queries.anonymous_count.toLocaleString()} anonymes`}
                />
              </Grid>
            </>
            :
            null
        }
      </Grid>
    </>
  );
}