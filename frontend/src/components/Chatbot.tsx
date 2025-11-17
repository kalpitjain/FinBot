import React, { useState, useEffect, useRef, useCallback } from 'react';
import ChatArea from './ChatArea';
import { sendChatMessage } from '../utils/apiHandler';
import './Chatbot.css';
import { MessageType } from '../types/MessageType';

const Chatbot: React.FC = () => {
  const [chatMessages, setChatMessages] = useState<MessageType[]>([]);
  const [userInput, setUserInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [showScrollButton, setShowScrollButton] = useState<boolean>(false);

  const messageContainerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSendMessage = useCallback(async (): Promise<void> => {
    const trimmedInput = userInput.trim();
    
    if (!trimmedInput || loading) return;
    
    if (trimmedInput.length > 1000) {
      const errorMessage: MessageType = { 
        text: 'Message is too long. Please limit to 1000 characters.', 
        isUser: false 
      };
      setChatMessages([...chatMessages, errorMessage]);
      return;
    }
    
    setLoading(true);
    const userMessage: MessageType = { text: trimmedInput, isUser: true };
    const updatedMessages = [...chatMessages, userMessage];
    setChatMessages(updatedMessages);
    setUserInput('');
    
    try {
      const response = await sendChatMessage(trimmedInput, updatedMessages);
      
      if (!response || typeof response !== 'string') {
        throw new Error('Invalid response from server');
      }
      
      setChatMessages([...updatedMessages, { text: response, isUser: false }]);
    } catch (error: unknown) {
      let errorMsg = 'Failed to get response. Please try again.';
      
      if (error instanceof Error) {
        errorMsg = error.message;
      } else if (typeof error === 'string') {
        errorMsg = error;
      }
      
      setChatMessages([...updatedMessages, { text: errorMsg, isUser: false }]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [userInput, loading, chatMessages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);


  useEffect(() => {
    messageContainerRef.current?.scrollTo({
      top: messageContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [chatMessages]);

  useEffect(() => {
    const container = messageContainerRef.current;
    if (!container) return;
    const handleScroll = () => {
      const atBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 40;
      setShowScrollButton(!atBottom);
    };
    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToBottom = () => {
    messageContainerRef.current?.scrollTo({
      top: messageContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  };

  return (
    <div className="chatbot-container" role="main" aria-label="FinBot Chatbot">
      <div className="chatbot-header" tabIndex={0} aria-label="FinBot header">
        <span className="bot-avatar" aria-label="Bot" role="img">
          💰
        </span>
        FinBot - Financial Assistant
      </div>

      <ChatArea
        chatMessages={chatMessages}
        loading={loading}
        messageContainerRef={messageContainerRef}
        showScrollButton={showScrollButton}
        scrollToBottom={scrollToBottom}
        userInput={userInput}
        setUserInput={setUserInput}
        sendMessage={handleSendMessage}
        inputRef={inputRef}
      />
    </div>
  );
};

export default Chatbot;
