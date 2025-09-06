import React, { useState } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Badge,
  Avatar,
  Menu,
  MenuItem as MuiMenuItem,
  useTheme,
  useMediaQuery,
  Collapse,
  Tooltip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Business as BusinessIcon,
  Notifications as NotificationsIcon,
  AccountCircle,
  Settings,
  Logout,
  ChevronLeft,
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store/store';
import { toggleSidebar, setSidebarOpen } from '../../store/slices/uiSlice';
import { logoutUser } from '../../store/slices/authSlice';
import { getMainMenuItems, MenuItem as MenuItemType } from '../../config/menuConfig';

// Smart Chatbot imports
import { SmartChatbot, ChatbotButton, useChatbot } from '../Chatbot';

const drawerWidth = 300; // Slightly wider for better sub-menu display

interface EnhancedLayoutProps {
  children: React.ReactNode;
}

const EnhancedLayout: React.FC<EnhancedLayoutProps> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [expandedItems, setExpandedItems] = useState<string[]>(['Human Resource Management']); // Default HRM expanded

  // Smart Chatbot integration
  const chatbot = useChatbot('employee'); // Default to employee mode

  const menuItems = getMainMenuItems();

  const handleDrawerToggle = () => {
    if (isMobile) {
      dispatch(setSidebarOpen(!sidebarOpen));
    } else {
      dispatch(toggleSidebar());
    }
  };

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    dispatch(logoutUser() as any);
    navigate('/login');
    handleProfileMenuClose();
  };

  const handleProfileClick = () => {
    navigate('/profile');
    handleProfileMenuClose();
  };

  const handleExpandClick = (itemText: string) => {
    setExpandedItems(prev => 
      prev.includes(itemText) 
        ? prev.filter(item => item !== itemText)
        : [...prev, itemText]
    );
  };

  const isMenuItemActive = (item: MenuItemType): boolean => {
    if (item.path) {
      return location.pathname === item.path;
    }
    if (item.subItems) {
      return item.subItems.some((subItem: any) => location.pathname === subItem.path);
    }
    return false;
  };

  const isSubItemActive = (path: string): boolean => {
    return location.pathname === path;
  };

  const renderMenuItem = (item: MenuItemType) => {
    const Icon = item.icon;
    const isActive = isMenuItemActive(item);
    const isExpanded = expandedItems.includes(item.text);
    const hasSubItems = item.subItems && item.subItems.length > 0;

    return (
      <React.Fragment key={item.text}>
        <ListItem disablePadding sx={{ mb: 0.5, px: 1 }}>
          <ListItemButton
            onClick={() => {
              if (hasSubItems) {
                handleExpandClick(item.text);
              } else if (item.text === 'Smart Chatbot') {
                // Open chatbot instead of navigating
                chatbot.openChatbot();
              } else if (item.path) {
                navigate(item.path);
              }
            }}
            sx={{
              borderRadius: 2,
              backgroundColor: isActive ? 'primary.main' : 'transparent',
              color: isActive ? 'white' : 'inherit',
              '&:hover': {
                backgroundColor: isActive ? 'primary.dark' : 'action.hover',
              },
              transition: 'all 0.2s',
              py: 1.5,
            }}
          >
            <ListItemIcon
              sx={{
                color: isActive ? 'white' : 'primary.main',
                minWidth: 40,
              }}
            >
              <Icon />
            </ListItemIcon>
            <ListItemText
              primary={item.text}
              primaryTypographyProps={{
                fontWeight: isActive ? 600 : 500,
                fontSize: '0.875rem',
              }}
            />
            {hasSubItems && (
              <IconButton
                size="small"
                sx={{ 
                  color: isActive ? 'white' : 'inherit',
                  ml: 1 
                }}
              >
                {isExpanded ? <ExpandLess /> : <ExpandMore />}
              </IconButton>
            )}
          </ListItemButton>
        </ListItem>

        {/* Sub-menu items */}
        {hasSubItems && (
          <Collapse in={isExpanded} timeout="auto" unmountOnExit>
            <List component="div" disablePadding sx={{ pl: 2 }}>
              {item.subItems!.map((subItem: any) => {
                const SubIcon = subItem.icon;
                const isSubActive = isSubItemActive(subItem.path);

                return (
                  <ListItem key={subItem.text} disablePadding sx={{ mb: 0.3 }}>
                    <Tooltip 
                      title={subItem.description || subItem.text} 
                      placement="right"
                      arrow
                    >
                      <ListItemButton
                        onClick={() => navigate(subItem.path)}
                        sx={{
                          borderRadius: 1.5,
                          backgroundColor: isSubActive ? 'secondary.main' : 'transparent',
                          color: isSubActive ? 'white' : 'text.secondary',
                          minHeight: 44,
                          '&:hover': {
                            backgroundColor: isSubActive ? 'secondary.dark' : 'action.hover',
                          },
                          transition: 'all 0.2s',
                        }}
                      >
                        <ListItemIcon
                          sx={{
                            color: isSubActive ? 'white' : 'secondary.main',
                            minWidth: 36,
                          }}
                        >
                          <SubIcon sx={{ fontSize: 20 }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={subItem.text}
                          primaryTypographyProps={{
                            fontWeight: isSubActive ? 600 : 400,
                            fontSize: '0.8rem',
                            lineHeight: 1.2,
                          }}
                        />
                      </ListItemButton>
                    </Tooltip>
                  </ListItem>
                );
              })}
            </List>
          </Collapse>
        )}
      </React.Fragment>
    );
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Logo Section */}
      <Box
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          minHeight: 64,
          background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
          color: 'white',
        }}
      >
        <BusinessIcon sx={{ mr: 1, fontSize: 28 }} />
        <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 'bold' }}>
          ERP System
        </Typography>
        {!isMobile && (
          <IconButton
            onClick={handleDrawerToggle}
            sx={{ ml: 'auto', color: 'white' }}
          >
            <ChevronLeft />
          </IconButton>
        )}
      </Box>

      <Divider />

      {/* HRM Feature Banner */}
      <Box sx={{ 
        p: 1.5, 
        mx: 1, 
        mt: 1,
        backgroundColor: 'success.light',
        borderRadius: 2,
        border: '1px solid',
        borderColor: 'success.main'
      }}>
        <Typography variant="caption" sx={{ 
          color: 'success.dark',
          fontWeight: 600,
          display: 'block',
          textAlign: 'center'
        }}>
          🆕 Enhanced HRM Features
        </Typography>
      </Box>

      {/* Navigation Menu */}
      <List sx={{ flexGrow: 1, pt: 1 }}>
        {menuItems.map(renderMenuItem)}
      </List>

      {/* User Info Section */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Avatar
            sx={{
              width: 32,
              height: 32,
              mr: 1,
              bgcolor: 'primary.main',
              fontSize: '0.875rem',
            }}
          >
            {user?.first_name?.charAt(0) || 'U'}
          </Avatar>
          <Box sx={{ flexGrow: 1, minWidth: 0 }}>
            <Typography variant="body2" noWrap fontWeight={600}>
              {user?.full_name || user?.username || 'User'}
            </Typography>
            <Typography variant="caption" color="text.secondary" noWrap>
              {user?.designation || 'Employee'}
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${sidebarOpen ? drawerWidth : 0}px)` },
          ml: { md: sidebarOpen ? `${drawerWidth}px` : 0 },
          transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          backgroundColor: 'background.paper',
          color: 'text.primary',
          boxShadow: '0px 1px 3px rgba(0,0,0,0.1)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: sidebarOpen ? 'none' : 'flex' } }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, fontWeight: 600 }}
          >
            Human Resource Management System
          </Typography>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <IconButton color="inherit">
              <Badge badgeContent={4} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
            
            <IconButton
              size="large"
              edge="end"
              aria-label="account of current user"
              aria-controls="primary-search-account-menu"
              aria-haspopup="true"
              onClick={handleProfileMenuOpen}
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Profile Menu */}
      <Menu
        id="primary-search-account-menu"
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={Boolean(anchorEl)}
        onClose={handleProfileMenuClose}
      >
        <MuiMenuItem onClick={handleProfileClick}>
          <ListItemIcon>
            <AccountCircle fontSize="small" />
          </ListItemIcon>
          Profile
        </MuiMenuItem>
        <MuiMenuItem onClick={handleProfileMenuClose}>
          <ListItemIcon>
            <Settings fontSize="small" />
          </ListItemIcon>
          Settings
        </MuiMenuItem>
        <Divider />
        <MuiMenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          Logout
        </MuiMenuItem>
      </Menu>

      {/* Sidebar Drawer */}
      <Box
        component="nav"
        sx={{ width: { md: sidebarOpen ? drawerWidth : 0 }, flexShrink: { md: 0 } }}
      >
        <Drawer
          variant={isMobile ? 'temporary' : 'persistent'}
          open={sidebarOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              borderRight: '1px solid',
              borderColor: 'divider',
            },
          }}
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${sidebarOpen ? drawerWidth : 0}px)` },
          mt: 8,
          transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
        }}
      >
        {children}
      </Box>

      {/* Smart Chatbot Integration */}
      <ChatbotButton
        onClick={chatbot.toggleChatbot}
        hasUnreadMessages={chatbot.hasUnreadMessages}
      />
      
      <SmartChatbot
        open={chatbot.isOpen}
        onClose={chatbot.closeChatbot}
        userType={chatbot.userType}
      />
    </Box>
  );
};

export default EnhancedLayout;
