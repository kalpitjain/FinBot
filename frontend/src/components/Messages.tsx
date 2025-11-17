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
  >
    {messages.map((message: MessageType, index: number) => (
      <MessageBubble key={index} text={message.text} isUser={message.isUser} />
    ))}

    {/* Typing Indicator */}
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
