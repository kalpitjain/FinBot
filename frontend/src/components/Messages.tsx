import React, { RefObject } from 'react';
import './Chatbot.css';
import MessageBubble from './MessageBubble';
import { MessageType } from '../types/MessageType';

interface MessagesProps {
  messages: MessageType[];
  isLoading: boolean;
  messageContainerRef: RefObject<HTMLDivElement>;
}

const Messages: React.FC<MessagesProps> = ({ messages, isLoading, messageContainerRef }) => (
  <div
    className="message-container"
    ref={messageContainerRef}
    tabIndex={0}
    aria-live="polite"
    aria-label="Chat messages"
    role="log"
  >
    {messages.map((message: MessageType, index: number) => (
      <MessageBubble key={index} text={message.text} isUser={message.isUser} />
    ))}
    {isLoading && (
      <div className="loading-animation" aria-label="Bot is typing">
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    )}
  </div>
);

export default Messages;
