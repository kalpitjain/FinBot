import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import ChartVisual from './ChartVisual';

interface MessageBubbleProps {
  text: string;
  isUser: boolean;
}

interface ChartRequest {
  chart_type: 'pie' | 'bar' | 'line';
  title: string;
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
  }>;
  insights?: string[];
}

// Reusable markdown components
const markdownComponents = {
  h1: ({ children }: any) => <h1 className="md-h1">{children}</h1>,
  h2: ({ children }: any) => <h2 className="md-h2">{children}</h2>,
  h3: ({ children }: any) => <h3 className="md-h3">{children}</h3>,
  h4: ({ children }: any) => <h4 className="md-h4">{children}</h4>,
  h5: ({ children }: any) => <h5 className="md-h5">{children}</h5>,
  h6: ({ children }: any) => <h6 className="md-h6">{children}</h6>,
  p: ({ children }: any) => <p className="md-paragraph">{children}</p>,
  ul: ({ children }: any) => <ul className="md-ul">{children}</ul>,
  ol: ({ children }: any) => <ol className="md-ol">{children}</ol>,
  li: ({ children }: any) => <li className="md-li">{children}</li>,
  table: ({ children }: any) => (
    <div className="md-table-wrapper">
      <table className="md-table">{children}</table>
    </div>
  ),
  thead: ({ children }: any) => <thead className="md-thead">{children}</thead>,
  tbody: ({ children }: any) => <tbody className="md-tbody">{children}</tbody>,
  tr: ({ children }: any) => <tr className="md-tr">{children}</tr>,
  th: ({ children }: any) => <th className="md-th">{children}</th>,
  td: ({ children }: any) => <td className="md-td">{children}</td>,
  code: ({ className, children, ...props }: any) => {
    const match = /language-(\w+)/.exec(className || '');
    const isInline = !match;
    
    return isInline ? (
      <code className="md-code-inline" {...props}>
        {children}
      </code>
    ) : (
      <code className={`md-code-block ${className}`} {...props}>
        {children}
      </code>
    );
  },
  pre: ({ children }: any) => <pre className="md-pre">{children}</pre>,
  blockquote: ({ children }: any) => <blockquote className="md-blockquote">{children}</blockquote>,
  strong: ({ children }: any) => <strong className="md-strong">{children}</strong>,
  em: ({ children }: any) => <em className="md-em">{children}</em>,
  hr: () => <hr className="md-hr" />,
  a: ({ href, children }: any) => (
    <a href={href} className="md-link" target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  ),
};

// Function to extract chart data from markdown text
const extractChartData = (text: string): { 
  chartData: ChartRequest | null; 
  beforeChart: string; 
  afterChart: string;
} => {
  try {
    // Look for JSON code blocks containing chart_request
    const jsonBlockRegex = /```json\s*(\{[\s\S]*?"chart_request"[\s\S]*?\})\s*```/;
    const match = text.match(jsonBlockRegex);
    
    if (match) {
      const jsonStr = match[1];
      const parsed = JSON.parse(jsonStr);
      
      if (parsed.chart_request) {
        // Split text before and after the chart
        const parts = text.split(jsonBlockRegex);
        const beforeChart = parts[0].trim();
        const afterChart = parts.slice(2).join('').trim();
        return { chartData: parsed.chart_request, beforeChart, afterChart };
      }
    }
    
    // Also check for chart_request object directly in the text (not in code block)
    const directJsonRegex = /\{[\s\S]*?"chart_request"[\s\S]*?\}/;
    const directMatch = text.match(directJsonRegex);
    
    if (directMatch) {
      const parsed = JSON.parse(directMatch[0]);
      if (parsed.chart_request) {
        const parts = text.split(directJsonRegex);
        const beforeChart = parts[0].trim();
        const afterChart = parts.slice(1).join('').trim();
        return { chartData: parsed.chart_request, beforeChart, afterChart };
      }
    }
  } catch (error) {
    console.error('Error parsing chart data:', error);
  }
  
  return { chartData: null, beforeChart: text, afterChart: '' };
};

const MessageBubble: React.FC<MessageBubbleProps> = ({ text, isUser }) => {
  // Extract chart data if present
  const { chartData, beforeChart, afterChart } = isUser 
    ? { chartData: null, beforeChart: text, afterChart: '' } 
    : extractChartData(text);
  
  return (
    <div
      className={`message ${isUser ? 'user' : 'bot'} message-pop`}
      tabIndex={0}
      style={{ position: 'relative' }}
    >
      {isUser ? (
        // For user messages, render as plain text
        <p className="message-line">{text}</p>
      ) : (
        <>
          {/* Render content before chart */}
          {beforeChart && (
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
              {beforeChart}
            </ReactMarkdown>
          )}
          
          {/* Render chart if found */}
          {chartData && <ChartVisual chartRequest={chartData} />}
          
          {/* Render content after chart */}
          {afterChart && (
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
              {afterChart}
            </ReactMarkdown>
          )}
        </>
      )}
    </div>
  );
};

export default MessageBubble;
