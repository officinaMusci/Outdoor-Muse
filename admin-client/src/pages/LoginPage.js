import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  OutlinedInput,
  InputAdornment,
  IconButton,
  Button,
  Alert
} from '@mui/material';
import {
  VisibilityOff,
  Visibility
} from '@mui/icons-material';

import useApi from '../services/apiHook';
import { AuthContext } from '../services/authContext';


/**
 * Renders the login page
 * @component
 */
export default function LoginPage() {
  const [, setIsAuthenticated] = useContext(AuthContext);
  const navigate = useNavigate();
  const { apiCall } = useApi();

  const [email, setEmail] = useState('admin@test.test');
  const [password, setPassword] = useState('test_password');
  const [error, setError] = useState(false)
  const [showPassword, setShowPassword] = useState(false);

  const handleEmailChange = event => {
    setError(false);
    setEmail(event.target.value);
  }

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  }

  const handlePasswordChange = event => {
    setError(false);
    setPassword(event.target.value);
  }

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  }

  const handleSubmit = () => {
    apiCall(
      '/auth/login',
      'POST',
      { email, password }
    )
    .then(response => {
      if (!response.error) {
        setIsAuthenticated(response.result)
        .then(() => {
          navigate('/');
        });
        
      } else {
        setError(true);
      }
    });
  }

  const inputStyle = {
    width: '100%',
    marginTop: 3
  }

  return (
    <Box
      component='form'
      sx={{
        mt: 4,
        display: 'flex',
        justifyContent: 'center',
        '& > :not(style)': {
          m: 1,
          maxWidth: '25ch'
        },
      }}
      noValidate
      autoComplete='off'
      onSubmit={e => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <Paper
        elevation={5}
        sx={{
          p: 2
        }}
      >
        <Typography
          variant='h5'
          component='h2'
          textAlign='center'
          sx={{
            mt: 1
          }}
        >
          Login
        </Typography>
        <TextField
          value={email}
          onInput={handleEmailChange}
          label='E-mail'
          error={error}
          sx={inputStyle}
        />
        <FormControl
          error={error}
          sx={inputStyle}
        >
          <InputLabel
            htmlFor='password-input'
          >
            Password
          </InputLabel>
          <OutlinedInput
            id='password-input'
            type={showPassword ? 'text' : 'password'}
            value={password}
            onInput={handlePasswordChange}
            endAdornment={
              <InputAdornment position='end'>
                <IconButton
                  aria-label='toggle password visibility'
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge='end'
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label='Password'
          />
        </FormControl>
        {error ?
          <Alert
            severity='error'
            sx={{
              mt: 3
            }}
          >
            La combinaison de l’ID utilisateur
            et le mot de passe entré n’est pas valide
          </Alert>
          :
          null
        }
        <Button
          variant='contained'
          type='submit'
          sx={inputStyle}
        >
          Login
        </Button>
      </Paper>
    </Box>
  );
}