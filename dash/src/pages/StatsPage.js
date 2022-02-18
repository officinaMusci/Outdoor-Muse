import {
  useState,
  useEffect
} from 'react';
import {
  Divider,
  Grid,
  Skeleton
} from '@mui/material';

import useApi from '../services/apiHook';
import DataCard from '../components/DataCard';
import StatCard from '../components/StatCard';


/**
 * Renders the statistics page
 * @component
 */
export default function StatsPage() {
  const { apiCall } = useApi();

  const [isLoading, setIsLoading] = useState(true);
  const [allData, setAllData] = useState();

  useEffect(() => {
    setIsLoading(true);
    apiCall(
      `/statistics/all`,
      'GET'
    )
      .then(response => {
        setIsLoading(false);
        if (!response.error) {
          setAllData(response.result);
        }
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Grid container spacing={2}>
      {isLoading ?
        Array(4).fill('').map((_, index) => (
          <Grid
            key={index}
            item
            xs={12}
            md={6}
            height='fit-content'
          >
            <Skeleton
              animation='wave'
              sx={{
                height: 500,
                backgroundColor: 'rgba(255, 255, 255, .5)',
                transform: 'none'
              }}
            />
          </Grid>
        ))
        :
        allData ?
          <>
            <Grid item xs={12} md={6}>
              <StatCard
                title='Météo souhaitée'
                data={allData.weather_counts}
                type='bar'
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <DataCard
                count={Number(allData.radius_mean / 1000).toFixed(2) + ' km'}
                description='Rayon max (μ)'
              />
              <Divider light sx={{mt: 1, mb: 1}} />
              <DataCard
                count={allData.max_travel_mean.split('.')[0]}
                description='Trajet max (μ)'
              />
              <Divider light sx={{mt: 1, mb: 1}} />
              <DataCard
                count={allData.max_walk_mean.split('.')[0]}
                description='Marche max (μ)'
              />
            </Grid>
            <Grid item xs={12}>
              <StatCard
                title='Avis'
                data={allData.over_time.reviews}
              />
            </Grid>
            <Grid item xs={12}>
              <StatCard
                title='Utilisateurs'
                data={allData.over_time.users}
              />
            </Grid>
            <Grid item xs={12}>
              <StatCard
                title='Recherches'
                data={allData.over_time.queries}
              />
            </Grid>
          </>
          :
          null
      }
    </Grid>
  );
}