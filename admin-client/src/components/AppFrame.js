import {
  forwardRef,
  useContext,
  useState
} from 'react';
import {
  Link as RouterLink,
  useLocation,
  useNavigate
} from 'react-router-dom';
import {
  useTheme,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Container
} from '@mui/material';
import {
  Menu as MenuIcon,
  Close as CloseIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';

import { routes } from '../settings';
import { AuthContext } from '../services/authContext';


// Override the default MUI link behaviour with the Router one.
const LinkBehaviour = forwardRef((props, ref) => (
  <RouterLink
    ref={ref}
    {...props}
  />
));


/**
 * Renders the app menu list
 * @property  {CallableFunction}  handleDrawerToggle  The function to toggle the mobile drawer
 * @property  {CallableFunction}  handleLogoutClick   The function to call on logout button click
 * @component 
 */
const MenuList = props => {
  const location = useLocation();
  const theme = useTheme();

  const {
    handleDrawerToggle,
    handleLogoutClick
  } = props;

  return (
    <>
      <AppBar position='static'>
        <Toolbar disableGutters>
          <IconButton
            size='large'
            onClick={handleDrawerToggle}
            color='inherit'
            sx={{
              ml: .5,
              mr: 1.75,
              display: {
                fontSize: '.1rem',
                xs: 'block',
                [theme.custom.appFrame.breakPoint]: 'none'
              }
            }}
          >
            <CloseIcon />
          </IconButton>
          <Typography
            variant='h6'
            sx={{
              ml: {
                [theme.custom.appFrame.breakPoint]: 2.5
              }
            }}
          >
            {theme.custom.appFrame.title}
          </Typography>
        </Toolbar>
      </AppBar>
      <List>
        {routes.map((route, index) => (
          <ListItem
            button
            key={index}
            component={LinkBehaviour}
            onClick={handleDrawerToggle}
            to={route.path}
            selected={(
                route.path === location.pathname
                || (route.path === '/' && !location.pathname)
              )}
            >
            <ListItemIcon>
              {route.icon ? route.icon : null}
            </ListItemIcon>
            <ListItemText>{route.label}</ListItemText>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        <ListItem
          button
          key={routes.length}
          onClick={() => handleLogoutClick()}
        >
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText>Logout</ListItemText>
        </ListItem>
      </List>
    </>
  );
}


/**
 * Renders the app frame drawers, containing the menu list
 * @property  {boolean}           mobileOpen          If the mobile drawer is open
 * @property  {CallableFunction}  handleDrawerToggle  The function to toggle the mobile drawer
 * @property  {Array}             children            The children of the component
 * @component 
 */
const Drawers = props => {
  const theme = useTheme();

  const {
    mobileOpen,
    handleDrawerToggle,
    children
  } = props;

  const container = props.window !== undefined ?
    () => props.window().document.body
    :
    undefined;

  return (
    <>
      <Drawer
        container={container}
        variant='temporary'
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: {
            xs: 'block',
            [theme.custom.appFrame.breakPoint]: 'none'
          },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: theme.custom.appFrame.drawerWidth
          },
        }}
      >
        {children}
      </Drawer>
      <Drawer
        variant='permanent'
        sx={{
          display: {
            xs: 'none',
            [theme.custom.appFrame.breakPoint]: 'block'
          },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: theme.custom.appFrame.drawerWidth
          },
        }}
        open
      >
        {children}
      </Drawer>
    </>
  );
}


/**
 * Renders the app frame
 * @property  {Array}  children  The children of the component
 * @component
 */
export default function AppFrame(props) {
  const [isAuthenticated, setIsAuthenticated] = useContext(AuthContext);
  const location = useLocation();
  const navigate = useNavigate();
  const theme = useTheme();

  const {
    children
  } = props;

  const currentPage = routes.filter(route => (
    route.path === location.pathname
    || (route.path === '/' && !location.pathname)
  ));
  const currentPageLabel = currentPage.length ?
    currentPage[0].label
    :
    location.pathname !== '/login' ?
      '404'
      :
      '';

  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogoutClick = () => {
    setIsAuthenticated(false);
    setMobileOpen(false);
    navigate('/login');
  }

  return (
    <>
      <AppBar
        position='sticky'
        sx={isAuthenticated ?
          {
            width: {
              [theme.custom.appFrame.breakPoint]: `calc(100% - ${theme.custom.appFrame.drawerWidth}px)`
            },
            ml: {
              [theme.custom.appFrame.breakPoint]: `${theme.custom.appFrame.drawerWidth}px`
            },
          }
          :
          {}
        }
      >
        <Toolbar disableGutters>
          {isAuthenticated ?
            <>
              <IconButton
                size='large'
                aria-haspopup='true'
                onClick={handleDrawerToggle}
                color='inherit'
                sx={{
                  ml: .5,
                  mr: 1.75,
                  display: {
                    fontSize: '.1rem',
                    xs: 'block',
                    [theme.custom.appFrame.breakPoint]: 'none'
                  }
                }}
              >
                <MenuIcon />
              </IconButton>
              <Drawers
                mobileOpen={mobileOpen}
                handleDrawerToggle={handleDrawerToggle}
              >
                <MenuList
                  handleDrawerToggle={handleDrawerToggle}
                  handleLogoutClick={handleLogoutClick}
                />
              </Drawers>
            </>
            :
            <Typography
              variant='h6'
              sx={{
                m: 'auto'
              }}
            >
              {theme.custom.appFrame.title}
            </Typography>
          }
          <Typography
            variant='h6'
            sx={{
              mr: currentPage ? .5 : undefined,
              display: {
                xs: 'block',
                [theme.custom.appFrame.breakPoint]: 'none'
              }
            }}
          >
            {theme.custom.appFrame.title}
            {currentPage ? ' /' : ''}
          </Typography>
          {currentPage && currentPageLabel ?
            <Typography
              variant='h6'
              sx={{
                ml: {
                  [theme.custom.appFrame.breakPoint]: 3
                }
              }}
            >
              {currentPageLabel}
            </Typography>
            :
            null
          }
        </Toolbar>
      </AppBar>
      <Container
        sx={isAuthenticated ?
          {
            width: {
              [theme.custom.appFrame.breakPoint]: `calc(100% - ${theme.custom.appFrame.drawerWidth}px)`
            },
            maxWidth: '100% !important',
            mt: 3,
            ml: {
              [theme.custom.appFrame.breakPoint]: `${theme.custom.appFrame.drawerWidth}px`
            },
          }
          :
          {}
        }
      >
        {children}
      </Container>
    </>
  );
};
