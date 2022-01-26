import { useContext } from 'react';
import {
  Navigate,
  Outlet
} from 'react-router-dom';
import { AuthContext } from '../services/authContext';


/**
 * Protects a route requiring auth, redirects on login page if not authorized
 * @component
 */
export default function ProtectedRoute({
  component: Component,
  ...restOfProps
}) {
  const [isAuthenticated, ] = useContext(AuthContext);

  return isAuthenticated ?
    <Outlet />
    :
    <Navigate to='/login' />
  ;
}