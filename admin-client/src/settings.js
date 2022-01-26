import {
  createTheme
} from '@mui/material';
import {
  Home as HomeIcon,
  QueryStats as StatsIcon,
  Group as UsersIcon,
  Store as PartnersIcon,
  Flag as ReportsIcon,
} from '@mui/icons-material';
import { frFR } from '@mui/material/locale';

import HomePage from './pages/HomePage';
import StatsPage from './pages/StatsPage';
import UsersPage from './pages/UsersPage';
import PartnersPage from './pages/PartnersPage';
import ReportsPage from './pages/ReportsPage';


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
    label: 'Reportages',
    path: '/reports',
    icon: <ReportsIcon />,
    page: <ReportsPage />
  },
]


// The Material UI theme for the app
export const theme = createTheme({
  
  custom: {
    appFrame: {
      title: 'Outdoor Muse Console',
      drawerWidth: 300,
      breakPoint: 'lg'
    }
  }
}, frFR);