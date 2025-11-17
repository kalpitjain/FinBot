import axios, { AxiosError } from 'axios';
import { MessageType } from '../types/MessageType';

const API_BASE_URL: string = import.meta.env.VITE_APP_API_URL || 'http://localhost:8000';

// Configure axios defaults
axios.defaults.timeout = 30000;

export const sendChatMessage = async (
  userAsk: string,
  conversationHistory: MessageType[],
): Promise<string> => {
  if (!userAsk || !userAsk.trim()) {
    throw new Error('Message cannot be empty');
  }

  if (userAsk.length > 1000) {
    throw new Error('Message is too long. Please limit to 1000 characters.');
  }

  try {
    const response = await axios.post(
      `${API_BASE_URL}/getBotResponse`,
      { conversationHistory, userAsk: userAsk.trim() },
      { 
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
        }
      }
    );
    
    if (response.data?.success && response.data?.response) {
      return response.data.response;
    }
    
    throw new Error(response.data?.error || 'Failed to get response');
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<{error?: string}>;
      
      if (axiosError.response) {
        // Server responded with error
        const errorMsg = axiosError.response.data?.error || 'Server error occurred';
        throw new Error(errorMsg);
      } else if (axiosError.code === 'ECONNABORTED') {
        throw new Error('Request timeout. The server took too long to respond.');
      } else if (axiosError.code === 'ECONNREFUSED') {
        throw new Error('Cannot connect to server. Please check if the backend is running.');
      } else if (axiosError.request) {
        throw new Error('No response from server. Please check your connection.');
      }
    }
    
    throw error;
  }
};
