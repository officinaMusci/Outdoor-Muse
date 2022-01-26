import {
    createContext,
    useState
} from 'react';


// The Auth context to handle the logged in status for the user.
export const AuthContext = createContext();


/**
 * Returns the provider for the Auth context.
 * @component
 */
export const AuthProvider = props => {
    const token = sessionStorage.getItem('outdoor_muse_jwt');

    const [isAuthenticated, setIsAuthenticated] = useState(!!token);

    const handleSetIsAuthenticated = async state => {
        state = await state;

        if (typeof state === 'string') {
            sessionStorage.setItem('outdoor_muse_jwt', state);
            setIsAuthenticated(true);

        } else {
            sessionStorage.removeItem('outdoor_muse_jwt');
            setIsAuthenticated(false);
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