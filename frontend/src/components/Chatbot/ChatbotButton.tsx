/**
 * Floating Chatbot Button
 * Always visible button to open the Smart Chatbot
 */

import React from 'react';
import {
  Fab,
  Badge,
  Tooltip,
  Zoom,
  useTheme,
  alpha
} from '@mui/material';
import {
  SmartToy as BotIcon,
  AutoAwesome as AIIcon
} from '@mui/icons-material';

interface ChatbotButtonProps {
  onClick: () => void;
  hasUnreadMessages?: boolean;
  disabled?: boolean;
}

const ChatbotButton: React.FC<ChatbotButtonProps> = ({
  onClick,
  hasUnreadMessages = false,
  disabled = false
}) => {
  const theme = useTheme();

  return (
    <Zoom in={true}>
      <Tooltip title="Smart AI Assistant" placement="left">
        <Fab
          color="primary"
          onClick={onClick}
          disabled={disabled}
          sx={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            zIndex: 1000,
            background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
            boxShadow: theme.shadows[8],
            '&:hover': {
              background: `linear-gradient(45deg, ${theme.palette.primary.dark} 30%, ${theme.palette.secondary.dark} 90%)`,
              transform: 'scale(1.1)',
              boxShadow: theme.shadows[12],
            },
            '&:active': {
              transform: 'scale(0.95)',
            },
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              borderRadius: '50%',
              background: `radial-gradient(circle, ${alpha(theme.palette.primary.light, 0.3)} 0%, transparent 70%)`,
              animation: 'pulse 2s infinite',
            },
            '@keyframes pulse': {
              '0%': {
                transform: 'scale(1)',
                opacity: 1,
              },
              '50%': {
                transform: 'scale(1.2)',
                opacity: 0.7,
              },
              '100%': {
                transform: 'scale(1)',
                opacity: 1,
              },
            }
          }}
        >
          <Badge
            badgeContent={hasUnreadMessages ? <AIIcon sx={{ fontSize: 12 }} /> : null}
            color="error"
            overlap="circular"
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
          >
            <BotIcon sx={{ fontSize: 28, color: 'white' }} />
          </Badge>
        </Fab>
      </Tooltip>
    </Zoom>
  );
};

export default ChatbotButton;
