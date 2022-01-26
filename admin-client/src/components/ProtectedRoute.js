import * as React from 'react';
import {
  Navigate,
  Outlet
} from 'react-router-dom';
import { AuthConsumer } from '../services/Auth';


/**
 * Protects a route requiring auth, redirects on login page if not authorized
 * @component
 */
export default function ProtectedRoute({
  component: Component,
  ...restOfProps
}) {
  return (
    <AuthConsumer>
      {([isAuthenticated, ]) => isAuthenticated ?
        <Outlet />
        :
        <Navigate to='/login' />}
    </AuthConsumer>
  )
}