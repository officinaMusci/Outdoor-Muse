import {
  createContext,
  useState
} from 'react';
import { useNavigate } from 'react-router-dom';

import { tokenName } from '../settings';


// The Auth context to handle the logged in status for the user.
export const AuthContext = createContext();


/**
 * Returns the provider for the Auth context.
 * @component
 */
export const AuthProvider = props => {
  const navigate = useNavigate();

  const token = sessionStorage.getItem(tokenName);
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);

  const handleSetIsAuthenticated = async state => {
    state = await state;

    if (typeof state === 'string') {
      sessionStorage.setItem(tokenName, state);
      setIsAuthenticated(true);

    } else {
      sessionStorage.removeItem(tokenName);
      setIsAuthenticated(false);
      navigate('/login');
    }
  }

  return (
    <AuthContext.Provider
      value={[
        isAuthenticated,
        handleSetIsAuthenticated
      ]}
    >
      {props.children}
    </AuthContext.Provider>
  );
}


/**
 * Returns a consumer for the Auth context.
 * @component
 */
export const AuthConsumer = props => {
  return (
    <AuthContext.Consumer>
      {props.children}
    </AuthContext.Consumer>
  );
}