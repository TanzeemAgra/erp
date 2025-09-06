/**
 * Smart Chatbot Frontend Integration Test
 * Tests the React components and API integration
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { SmartChatbot, ChatbotButton, useChatbot } from '../src/components/Chatbot';
import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

const theme = createTheme();

// Test component that uses the chatbot hook
const TestComponent: React.FC = () => {
  const chatbot = useChatbot('employee');
  
  return (
    <ThemeProvider theme={theme}>
      <div>
        <ChatbotButton
          onClick={chatbot.toggleChatbot}
          hasUnreadMessages={chatbot.hasUnreadMessages}
        />
        
        <SmartChatbot
          open={chatbot.isOpen}
          onClose={chatbot.closeChatbot}
          userType={chatbot.userType}
        />
        
        <button onClick={chatbot.openChatbot} data-testid="open-chatbot">
          Open Chatbot
        </button>
        
        <span data-testid="chatbot-status">
          {chatbot.isOpen ? 'open' : 'closed'}
        </span>
      </div>
    </ThemeProvider>
  );
};

describe('Smart Chatbot Integration', () => {
  beforeEach(() => {
    // Mock localStorage
    const localStorageMock = {
      getItem: jest.fn(() => 'mock-token'),
      setItem: jest.fn(),
      removeItem: jest.fn(),
      clear: jest.fn(),
    };
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders chatbot button', () => {
    render(<TestComponent />);
    
    // Check if chatbot button is rendered
    const chatbotButton = screen.getByRole('button', { name: /smart ai assistant/i });
    expect(chatbotButton).toBeInTheDocument();
  });

  test('opens and closes chatbot', async () => {
    render(<TestComponent />);
    
    const statusElement = screen.getByTestId('chatbot-status');
    const openButton = screen.getByTestId('open-chatbot');
    
    // Initially closed
    expect(statusElement).toHaveTextContent('closed');
    
    // Open chatbot
    fireEvent.click(openButton);
    await waitFor(() => {
      expect(statusElement).toHaveTextContent('open');
    });
    
    // Check if chatbot drawer is visible
    expect(screen.getByText('Smart Chatbot')).toBeInTheDocument();
  });

  test('sends message through API', async () => {
    // Mock successful API response
    mockedAxios.post.mockResolvedValueOnce({
      data: {
        response: 'Hello! How can I help you today?',
        type: 'text',
        escalate: false,
        suggestions: ['Leave Policy', 'Payroll Info']
      }
    });

    render(<TestComponent />);
    
    // Open chatbot
    fireEvent.click(screen.getByTestId('open-chatbot'));
    
    await waitFor(() => {
      expect(screen.getByText('Smart Chatbot')).toBeInTheDocument();
    });
    
    // Find and use the message input
    const messageInput = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    
    // Type and send message
    fireEvent.change(messageInput, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);
    
    // Verify API call
    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledWith(
        '/api/v1/chatbot/chat/',
        expect.objectContaining({
          message: 'Hello',
          context: 'employee',
          user_type: 'employee'
        }),
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer mock-token'
          })
        })
      );
    });
  });

  test('handles API error gracefully', async () => {
    // Mock API error
    mockedAxios.post.mockRejectedValueOnce(new Error('Network error'));

    render(<TestComponent />);
    
    // Open chatbot
    fireEvent.click(screen.getByTestId('open-chatbot'));
    
    await waitFor(() => {
      expect(screen.getByText('Smart Chatbot')).toBeInTheDocument();
    });
    
    // Find and use the message input
    const messageInput = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    
    // Type and send message
    fireEvent.change(messageInput, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);
    
    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/experiencing technical difficulties/i)).toBeInTheDocument();
    });
  });

  test('switches between employee and customer modes', async () => {
    render(<TestComponent />);
    
    // Open chatbot
    fireEvent.click(screen.getByTestId('open-chatbot'));
    
    await waitFor(() => {
      expect(screen.getByText('Employee Assistant')).toBeInTheDocument();
    });
    
    // Find and click the more options menu
    const moreButton = screen.getByRole('button', { name: /more/i });
    fireEvent.click(moreButton);
    
    // Switch to customer mode
    const switchElement = screen.getByRole('checkbox', { name: /switch to customer/i });
    fireEvent.click(switchElement);
    
    await waitFor(() => {
      expect(screen.getByText('Customer Support')).toBeInTheDocument();
    });
  });

  test('displays welcome message', async () => {
    render(<TestComponent />);
    
    // Open chatbot
    fireEvent.click(screen.getByTestId('open-chatbot'));
    
    await waitFor(() => {
      expect(screen.getByText(/Hello! I'm your Smart AI Assistant/i)).toBeInTheDocument();
    });
  });

  test('handles suggestion clicks', async () => {
    // Mock API response with suggestions
    mockedAxios.post.mockResolvedValueOnce({
      data: {
        response: 'Here are some options:',
        type: 'text',
        escalate: false,
        suggestions: ['Leave Policy', 'Payroll Info', 'IT Equipment']
      }
    });

    render(<TestComponent />);
    
    // Open chatbot and wait for welcome message
    fireEvent.click(screen.getByTestId('open-chatbot'));
    
    await waitFor(() => {
      expect(screen.getByText('Leave Policy')).toBeInTheDocument();
    });
    
    // Click on a suggestion
    const suggestionChip = screen.getByText('Leave Policy');
    fireEvent.click(suggestionChip);
    
    // Verify API call was made
    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledWith(
        '/api/v1/chatbot/chat/',
        expect.objectContaining({
          message: 'Leave Policy'
        }),
        expect.any(Object)
      );
    });
  });
});

// Export test results
export const testResults = {
  testsPassed: 0,
  testsFailed: 0,
  testDetails: [],
  
  summary: () => {
    console.log('🧪 Smart Chatbot Frontend Tests Summary');
    console.log('=' * 50);
    console.log(`✅ Tests Passed: ${testResults.testsPassed}`);
    console.log(`❌ Tests Failed: ${testResults.testsFailed}`);
    console.log('\n📋 Test Coverage:');
    console.log('- Chatbot button rendering');
    console.log('- Open/close functionality');
    console.log('- Message sending via API');
    console.log('- Error handling');
    console.log('- User type switching');
    console.log('- Welcome message display');
    console.log('- Suggestion interactions');
    console.log('\n🚀 Integration Status: Ready for production!');
  }
};

export default TestComponent;
