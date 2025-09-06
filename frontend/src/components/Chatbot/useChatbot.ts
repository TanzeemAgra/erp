/**
 * Smart Chatbot Hook
 * Provides chatbot functionality and state management
 */

import { useState, useCallback } from 'react';
import axios from 'axios';

interface ChatbotState {
  isOpen: boolean;
  userType: 'employee' | 'customer';
  hasUnreadMessages: boolean;
}

interface ChatbotActions {
  openChatbot: () => void;
  closeChatbot: () => void;
  toggleChatbot: () => void;
  switchUserType: (type: 'employee' | 'customer') => void;
  markAsRead: () => void;
}

interface UseChatbotReturn extends ChatbotState, ChatbotActions {}

export const useChatbot = (initialUserType: 'employee' | 'customer' = 'employee'): UseChatbotReturn => {
  const [state, setState] = useState<ChatbotState>({
    isOpen: false,
    userType: initialUserType,
    hasUnreadMessages: false
  });

  const openChatbot = useCallback(() => {
    setState(prev => ({ ...prev, isOpen: true, hasUnreadMessages: false }));
  }, []);

  const closeChatbot = useCallback(() => {
    setState(prev => ({ ...prev, isOpen: false }));
  }, []);

  const toggleChatbot = useCallback(() => {
    setState(prev => ({ 
      ...prev, 
      isOpen: !prev.isOpen, 
      hasUnreadMessages: prev.isOpen ? prev.hasUnreadMessages : false 
    }));
  }, []);

  const switchUserType = useCallback((type: 'employee' | 'customer') => {
    setState(prev => ({ ...prev, userType: type }));
  }, []);

  const markAsRead = useCallback(() => {
    setState(prev => ({ ...prev, hasUnreadMessages: false }));
  }, []);

  return {
    ...state,
    openChatbot,
    closeChatbot,
    toggleChatbot,
    switchUserType,
    markAsRead
  };
};

// Chatbot API service functions
export const chatbotAPI = {
  sendMessage: async (message: string, userType: 'employee' | 'customer', conversationId: string) => {
    const response = await axios.post('/api/v1/chatbot/chat/', {
      message,
      context: userType,
      user_type: userType,
      conversation_id: conversationId
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  autoFillForm: async (formType: string) => {
    const response = await axios.post('/api/v1/chatbot/autofill/', {
      form_type: formType
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  getRecommendations: async () => {
    const response = await axios.get('/api/v1/chatbot/recommendations/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
    return response.data;
  },

  escalateToHuman: async (conversationId: string, reason: string, priority: 'low' | 'medium' | 'high' = 'medium') => {
    const response = await axios.post('/api/v1/chatbot/escalate/', {
      conversation_id: conversationId,
      reason,
      priority
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  },

  getStatus: async () => {
    const response = await axios.get('/api/v1/chatbot/status/');
    return response.data;
  }
};
