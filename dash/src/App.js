import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import {
  ThemeProvider
} from '@mui/material';

import { routes, theme } from './settings';
import AppFrame from './components/AppFrame';
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';
import { AuthProvider } from './services/authContext';


/**
 * Returns the app container
 * @component
 */
export default function App() {
  return (
    <Router>
      <AuthProvider>
        <ThemeProvider theme={theme}>
          <AppFrame>
            <Routes>
              <Route
                path='/login'
                element={<LoginPage />}
              />
              {routes.map(route => (
                <Route
                  key={route.path}
                  path={route.path}
                  element={<ProtectedRoute />}
                >
                  <Route
                    path={route.path}
                    element={route.page}
                  />
                </Route>
              ))}
              <Route element={<NotFoundPage />} />
            </Routes>
          </AppFrame>
        </ThemeProvider>
      </AuthProvider>
    </Router>
  );
}