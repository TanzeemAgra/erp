/**
 * Smart Chatbot Component
 * AI-Powered chatbot with RAG capabilities for Employee and Customer support
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  Drawer,
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
  List,
  ListItem,
  Avatar,
  Chip,
  Button,
  Divider,
  Badge,
  Tooltip,
  Menu,
  MenuItem,
  CircularProgress,
  Alert,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Close as CloseIcon,
  MoreVert as MoreIcon,
  AutoAwesome as AIIcon,
  Business as EmployeeIcon,
  Support as SupportIcon,
  Psychology as BrainIcon,
  AutoFixHigh as AutoFillIcon,
  Escalator as EscalateIcon,
  Lightbulb as SuggestionIcon,
} from '@mui/icons-material';
import axios from 'axios';

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  type?: 'text' | 'suggestion' | 'escalation' | 'autofill';
  suggestions?: string[];
  metadata?: any;
}

interface ChatbotProps {
  open: boolean;
  onClose: () => void;
  userType?: 'employee' | 'customer';
}

const SmartChatbot: React.FC<ChatbotProps> = ({ 
  open, 
  onClose, 
  userType = 'employee' 
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentUserType, setCurrentUserType] = useState<'employee' | 'customer'>(userType);
  const [menuAnchor, setMenuAnchor] = useState<null | HTMLElement>(null);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [conversationId] = useState(`conv_${Date.now()}`);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Initial welcome message
  useEffect(() => {
    if (open && messages.length === 0) {
      const welcomeMessage: ChatMessage = {
        id: 'welcome',
        text: currentUserType === 'employee' 
          ? "Hello! I'm your Smart AI Assistant. I can help you with HR policies, leave requests, payroll queries, equipment management, and more. How can I assist you today?"
          : "Welcome! I'm here to help with your orders, invoices, project status, and any other questions you may have. What can I help you with?",
        sender: 'bot',
        timestamp: new Date(),
        type: 'text',
        suggestions: currentUserType === 'employee' 
          ? ['Leave Policy', 'Apply for Leave', 'Payroll Info', 'IT Equipment']
          : ['Order Status', 'View Invoices', 'Project Updates', 'Contact Support']
      };
      setMessages([welcomeMessage]);
    }
  }, [open, currentUserType]);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when opened
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [open]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      text: text.trim(),
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/v1/chatbot/chat/', {
        message: text.trim(),
        context: currentUserType,
        user_type: currentUserType,
        conversation_id: conversationId
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });

      const botMessage: ChatMessage = {
        id: `bot_${Date.now()}`,
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date(),
        type: response.data.escalate ? 'escalation' : 'text',
        suggestions: response.data.suggestions || [],
        metadata: {
          escalate: response.data.escalate,
          type: response.data.type
        }
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Chatbot error:', error);
      const errorMessage: ChatMessage = {
        id: `error_${Date.now()}`,
        text: "I'm sorry, I'm experiencing technical difficulties. Please try again later or contact support directly.",
        sender: 'bot',
        timestamp: new Date(),
        type: 'escalation'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  const handleAutoFill = async (formType: string) => {
    setIsLoading(true);
    try {
      const response = await axios.post('/api/v1/chatbot/autofill/', {
        form_type: formType
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });

      const autoFillMessage: ChatMessage = {
        id: `autofill_${Date.now()}`,
        text: `I've prepared your ${formType.replace('_', ' ')} form with your information. Here's what I found:`,
        sender: 'bot',
        timestamp: new Date(),
        type: 'autofill',
        metadata: response.data
      };

      setMessages(prev => [...prev, autoFillMessage]);
    } catch (error) {
      console.error('Auto-fill error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEscalation = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post('/api/v1/chatbot/escalate/', {
        conversation_id: conversationId,
        reason: 'User requested human assistance',
        priority: 'medium'
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        }
      });

      const escalationMessage: ChatMessage = {
        id: `escalation_${Date.now()}`,
        text: `I've escalated your request to a human agent. ${response.data.message} Ticket ID: ${response.data.ticket_id}`,
        sender: 'bot',
        timestamp: new Date(),
        type: 'escalation'
      };

      setMessages(prev => [...prev, escalationMessage]);
    } catch (error) {
      console.error('Escalation error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUserTypeChange = () => {
    const newUserType = currentUserType === 'employee' ? 'customer' : 'employee';
    setCurrentUserType(newUserType);
    setMessages([]); // Clear messages when switching context
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputText);
    }
  };

  const renderMessage = (message: ChatMessage) => (
    <ListItem
      key={message.id}
      sx={{
        display: 'flex',
        flexDirection: message.sender === 'user' ? 'row-reverse' : 'row',
        alignItems: 'flex-start',
        mb: 1
      }}
    >
      <Avatar
        sx={{
          bgcolor: message.sender === 'user' ? 'primary.main' : 'secondary.main',
          ml: message.sender === 'user' ? 1 : 0,
          mr: message.sender === 'user' ? 0 : 1,
          width: 32,
          height: 32
        }}
      >
        {message.sender === 'user' ? <PersonIcon /> : <BotIcon />}
      </Avatar>
      
      <Box sx={{ maxWidth: '70%', minWidth: '200px' }}>
        <Paper
          elevation={1}
          sx={{
            p: 2,
            bgcolor: message.sender === 'user' ? 'primary.main' : 'grey.100',
            color: message.sender === 'user' ? 'white' : 'text.primary',
            borderRadius: message.sender === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px'
          }}
        >
          <Typography variant="body2">
            {message.text}
          </Typography>
          
          {message.type === 'escalation' && (
            <Alert severity="info" sx={{ mt: 1, fontSize: '0.75rem' }}>
              This conversation can be escalated to a human agent
            </Alert>
          )}
          
          {message.type === 'autofill' && message.metadata && (
            <Box sx={{ mt: 1 }}>
              <Typography variant="caption" display="block" sx={{ mb: 1 }}>
                Auto-filled Data:
              </Typography>
              {Object.entries(message.metadata).map(([key, value]) => (
                <Chip
                  key={key}
                  label={`${key}: ${value}`}
                  size="small"
                  sx={{ mr: 0.5, mb: 0.5, fontSize: '0.7rem' }}
                />
              ))}
            </Box>
          )}
        </Paper>
        
        {message.suggestions && message.suggestions.length > 0 && showSuggestions && (
          <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {message.suggestions.map((suggestion, index) => (
              <Chip
                key={index}
                label={suggestion}
                size="small"
                clickable
                onClick={() => handleSuggestionClick(suggestion)}
                icon={<SuggestionIcon />}
                sx={{ fontSize: '0.7rem' }}
              />
            ))}
          </Box>
        )}
        
        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
          {message.timestamp.toLocaleTimeString()}
        </Typography>
      </Box>
    </ListItem>
  );

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: {
          width: 400,
          maxWidth: '90vw',
          display: 'flex',
          flexDirection: 'column'
        }
      }}
    >
      {/* Header */}
      <Box sx={{ 
        p: 2, 
        bgcolor: 'primary.main', 
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Badge badgeContent={<AIIcon sx={{ fontSize: 12 }} />} color="secondary">
            <BrainIcon />
          </Badge>
          <Box sx={{ ml: 1 }}>
            <Typography variant="h6">Smart Chatbot</Typography>
            <Typography variant="caption">
              {currentUserType === 'employee' ? 'Employee Assistant' : 'Customer Support'}
            </Typography>
          </Box>
        </Box>
        
        <Box>
          <IconButton
            color="inherit"
            onClick={(e) => setMenuAnchor(e.currentTarget)}
            size="small"
          >
            <MoreIcon />
          </IconButton>
          <IconButton color="inherit" onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Settings Menu */}
      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={() => setMenuAnchor(null)}
      >
        <MenuItem>
          <FormControlLabel
            control={
              <Switch
                checked={currentUserType === 'customer'}
                onChange={handleUserTypeChange}
                color="primary"
              />
            }
            label={currentUserType === 'employee' ? 'Switch to Customer' : 'Switch to Employee'}
          />
        </MenuItem>
        <MenuItem>
          <FormControlLabel
            control={
              <Switch
                checked={showSuggestions}
                onChange={(e) => setShowSuggestions(e.target.checked)}
                color="primary"
              />
            }
            label="Show Suggestions"
          />
        </MenuItem>
        <Divider />
        {currentUserType === 'employee' && (
          <>
            <MenuItem onClick={() => handleAutoFill('leave_request')}>
              <AutoFillIcon sx={{ mr: 1 }} /> Auto-fill Leave Request
            </MenuItem>
            <MenuItem onClick={() => handleAutoFill('expense_report')}>
              <AutoFillIcon sx={{ mr: 1 }} /> Auto-fill Expense Report
            </MenuItem>
          </>
        )}
        <MenuItem onClick={handleEscalation}>
          <EscalateIcon sx={{ mr: 1 }} /> Escalate to Human
        </MenuItem>
      </Menu>

      {/* Messages */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
        <List sx={{ p: 0 }}>
          {messages.map(renderMessage)}
          {isLoading && (
            <ListItem sx={{ justifyContent: 'center' }}>
              <CircularProgress size={20} />
              <Typography variant="caption" sx={{ ml: 1 }}>
                AI is thinking...
              </Typography>
            </ListItem>
          )}
          <div ref={messagesEndRef} />
        </List>
      </Box>

      {/* Quick Actions */}
      <Box sx={{ p: 1, borderTop: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', gap: 0.5, mb: 1, flexWrap: 'wrap' }}>
          {currentUserType === 'employee' ? (
            <>
              <Button
                size="small"
                startIcon={<EmployeeIcon />}
                onClick={() => sendMessage('What is the leave policy?')}
                sx={{ fontSize: '0.7rem' }}
              >
                Leave Policy
              </Button>
              <Button
                size="small"
                startIcon={<AutoFillIcon />}
                onClick={() => sendMessage('Help me apply for leave')}
                sx={{ fontSize: '0.7rem' }}
              >
                Apply Leave
              </Button>
            </>
          ) : (
            <>
              <Button
                size="small"
                startIcon={<SupportIcon />}
                onClick={() => sendMessage('What is my order status?')}
                sx={{ fontSize: '0.7rem' }}
              >
                Order Status
              </Button>
              <Button
                size="small"
                startIcon={<SupportIcon />}
                onClick={() => sendMessage('Show my invoices')}
                sx={{ fontSize: '0.7rem' }}
              >
                Invoices
              </Button>
            </>
          )}
        </Box>
      </Box>

      {/* Input */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            ref={inputRef}
            fullWidth
            multiline
            maxRows={3}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            variant="outlined"
            size="small"
            disabled={isLoading}
          />
          <Tooltip title="Send message">
            <IconButton
              color="primary"
              onClick={() => sendMessage(inputText)}
              disabled={!inputText.trim() || isLoading}
              sx={{ 
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': { bgcolor: 'primary.dark' },
                '&:disabled': { bgcolor: 'grey.300' }
              }}
            >
              <SendIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
    </Drawer>
  );
};

export default SmartChatbot;
