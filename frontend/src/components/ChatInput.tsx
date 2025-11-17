import React, { RefObject } from 'react';

interface ChatInputProps {
  input: string;
  handleInput: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleKeyDown: (event: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  sendMessage: () => void;
  isLoading: boolean;
  inputRef: RefObject<HTMLTextAreaElement>;
}

const ChatInput: React.FC<ChatInputProps> = ({
  input,
  handleInput,
  handleKeyDown,
  sendMessage,
  isLoading,
  inputRef,
}) => (
  <div className="input-container">
    <textarea
      id="chat-input"
      className="input"
      value={input}
      onChange={handleInput}
      onKeyDown={handleKeyDown}
      placeholder="Type a message..."
      autoFocus
      disabled={isLoading}
      ref={inputRef}
      rows={1}
      style={{ minHeight: 44, maxHeight: 180, resize: 'vertical' }}
    />
    <span
      className={`send-icon input-buttons${isLoading ? ' disabled' : ''}`}
      onClick={!isLoading ? sendMessage : undefined}
      tabIndex={isLoading ? -1 : 0}
      role="button"
      onKeyDown={(e) => {
        if (!isLoading && (e.key === 'Enter' || e.key === ' ')) {
          sendMessage();
        }
      }}
      onMouseDown={(e) => {
        if (!isLoading) e.currentTarget.classList.add('pressed');
      }}
      onMouseUp={(e) => {
        if (!isLoading) e.currentTarget.classList.remove('pressed');
      }}
      onMouseLeave={(e) => {
        if (!isLoading) e.currentTarget.classList.remove('pressed');
      }}
    >
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
        <path d="M3 20v-6l13-2-13-2V4l19 8-19 8z" fill="currentColor" />
      </svg>
    </span>
  </div>
);

export default ChatInput;
