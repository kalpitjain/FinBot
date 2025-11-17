import React from 'react';

interface MessageBubbleProps {
  text: string;
  isUser: boolean;
}

const parseBoldText = (text: string): (string | JSX.Element)[] => {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, index) => {
    if (/^\*\*[^*]+\*\*$/.test(part)) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
};

const MessageBubble: React.FC<MessageBubbleProps> = ({ text, isUser }) => {
  const textLines = text.split('\n');
  const bulletPoints = textLines.filter((line) => line.trim().startsWith('* '));
  const regularLines = textLines.filter((line) => !line.trim().startsWith('* '));

  return (
    <div
      className={`message ${isUser ? 'user' : 'bot'} message-pop`}
      aria-live={isUser ? undefined : 'polite'}
      tabIndex={0}
      aria-label={isUser ? 'User message' : 'Bot message'}
      role="article"
      style={{ position: 'relative' }}
    >
      {regularLines.map((line, index) => (
        <p key={`p-${index}`} className="message-line">
          {parseBoldText(line)}
        </p>
      ))}
      {bulletPoints.length > 0 && (
        <ul className="message-bullets" style={{ marginLeft: 0, paddingLeft: '1.2em' }}>
          {bulletPoints.map((line, index) => (
            <li key={`li-${index}`}>{parseBoldText(line.trim().slice(2))}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MessageBubble;
