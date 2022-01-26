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
    <main
      style={{
        width: '100%',
        height: '100%',
        backgroundColor: theme.palette.grey[100]
      }}
    >
      <AuthProvider>
        <ThemeProvider theme={theme}>
          <Router>
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
          </Router>
        </ThemeProvider>
      </AuthProvider>
    </main>
  );
}