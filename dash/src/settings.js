import {
  createTheme
} from '@mui/material';
import {
  Home as HomeIcon,
  QueryStats as StatsIcon,
  Group as UsersIcon,
  Store as PartnersIcon,
  Landscape as PlacesIcon,
  Comment as ReviewsIcon,
} from '@mui/icons-material';
import { frFR } from '@mui/material/locale';

import HomePage from './pages/HomePage';
import StatsPage from './pages/StatsPage';
import UsersPage from './pages/UsersPage';
import PartnersPage from './pages/PartnersPage';
import PlacesPage from './pages/PlacesPage';
import ReviewsPage from './pages/ReviewsPage';


// The token name
export const tokenName = 'outdoor_muse_jwt';


// The routes of the app
export const routes = [
  {
    label: 'Accueil',
    path: '/',
    icon: <HomeIcon />,
    page: <HomePage />
  },
  {
    label: 'Statistiques',
    path: '/statistics',
    icon: <StatsIcon />,
    page: <StatsPage />
  },
  {
    label: 'Utilisateurs',
    path: '/users',
    icon: <UsersIcon />,
    page: <UsersPage />
  },
  {
    label: 'Partenaires',
    path: '/partners',
    icon: <PartnersIcon />,
    page: <PartnersPage />
  },
  {
    label: 'Randonnées',
    path: '/places',
    icon: <PlacesIcon />,
    page: <PlacesPage />
  },
  {
    label: 'Avis',
    path: '/reviews',
    icon: <ReviewsIcon />,
    page: <ReviewsPage />
  },
]


// The Material UI theme for the app
export const theme = createTheme({
  palette: {
    primary: {
      main: '#006069'
    },
    secondary: {
      main: '#AB4600'
    }
  },
  typography: {
    fontFamily: [
      'Ubuntu',
    ].join(','),
  },
  custom: {
    appName: 'Outdoor Muse',
    appFrame: {
      title: 'Outdoor Muse Console',
      drawerWidth: 300,
      breakPoint: 'lg'
    },
    datetimeFormat: 'DD.MM.YYYY HH:mm',
    backgroundImage: 'https://live.staticflickr.com/1531/24075708082_babc1a444e_k_d.jpg'
  }
}, frFR);