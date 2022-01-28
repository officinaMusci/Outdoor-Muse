import {
  useState,
  useEffect
} from 'react';
import {
  Grid,
  Skeleton
} from '@mui/material';

import useApi from '../services/apiHook';
import StatCard from '../components/StatCard';


/**
 * Renders the statistics page
 * @component
 */
export default function StatsPage() {
  const { apiCall } = useApi();

  const [isLoading, setIsLoading] = useState(true);
  const [overtimeData, setOvertimeData] = useState();

  useEffect(() => {
    setIsLoading(true);
    apiCall(
      `/statistics/over-time`,
      'GET'
    )
      .then(response => {
        setIsLoading(false);
        if (!response.error) {
          setOvertimeData(response.result);
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
                height: 150,
                transform: 'none'
              }}
            />
          </Grid>
        ))
        :
        overtimeData ?
          <>
            <Grid item xs={12} md={6}>
              <StatCard
                title='Avis'
                data={overtimeData.reviews}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <StatCard
                title='Partenaires'
                data={overtimeData.partners}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <StatCard
                title='Utilisateurs'
                data={overtimeData.users}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <StatCard
                title='Recherches'
                data={overtimeData.queries}
              />
            </Grid>
          </>
          :
          null
      }
    </Grid>
  );
}