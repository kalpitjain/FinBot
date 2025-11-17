import React from 'react';
import Messages from './Messages';
import ChatInput from './ChatInput';
import { MessageType } from '../types/MessageType';

interface ChatAreaProps {
  chatMessages: MessageType[];
  loading: boolean;
  messageContainerRef: React.RefObject<HTMLDivElement>;
  showScrollButton: boolean;
  scrollToBottom: () => void;
  userInput: string;
  setUserInput: (val: string) => void;
  sendMessage: () => void;
  inputRef: React.RefObject<HTMLTextAreaElement>;
}

const ChatArea: React.FC<ChatAreaProps> = ({
  chatMessages,
  loading,
  messageContainerRef,
  showScrollButton,
  scrollToBottom,
  userInput,
  setUserInput,
  sendMessage,
  inputRef,
}) => (
  <div className="chat-area" aria-live="polite">
    <Messages
      messages={chatMessages}
      isLoading={loading}
      messageContainerRef={messageContainerRef}
    />
    {showScrollButton && (
      <button
        className="scroll-to-bottom"
        onClick={scrollToBottom}
        type="button"
      >
        ↓
      </button>
    )}
    <ChatInput
      input={userInput}
      handleInput={(e: React.ChangeEvent<HTMLTextAreaElement>) => setUserInput(e.target.value)}
      handleKeyDown={(e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      }}
      sendMessage={sendMessage}
      isLoading={loading}
      inputRef={inputRef}
    />
  </div>
);

export default ChatArea;
