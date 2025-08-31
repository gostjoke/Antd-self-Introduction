import React, { useState, useRef, useEffect } from "react";
import { Button, Input, Avatar, Tooltip, message } from "antd";
import { 
  MessageOutlined, 
  CloseOutlined, 
  SendOutlined, 
  UserOutlined, 
  ClearOutlined,
  CopyOutlined 
} from "@ant-design/icons";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

// 模擬聊天數據
interface Message {
  id: string;
  text: string;
  user: {
    id: string;
    name: string;
    image?: string;
  };
  created_at: Date;
}

const ChatPage: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentMessage, setCurrentMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "歡迎來到 AI 助手聊天室！有什麼問題我可以幫助您嗎？\n\n您可以詢問程式設計相關問題，我會提供帶有語法高亮的程式碼範例。",
      user: {
        id: "ai-assistant",
        name: "AI 助手",
        image: "🤖",
      },
      created_at: new Date(Date.now() - 60000),
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自動滾動到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 清除對話
  const clearMessages = () => {
    setMessages([
      {
        id: "1",
        text: "對話已清除！有什麼新問題我可以幫助您嗎？",
        user: {
          id: "ai-assistant",
          name: "AI 助手",
          image: "🤖",
        },
        created_at: new Date(),
      },
    ]);
  };

  // 自定義 Markdown 組件
  const MarkdownMessage: React.FC<{ content: string }> = ({ content }) => {
    const copyToClipboard = async (text: string) => {
      try {
        await navigator.clipboard.writeText(text);
        message.success('程式碼已複製到剪貼簿！');
      } catch (err) {
        message.error('複製失敗');
      }
    };

    return (
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code: ({ node, inline, className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '');
            const language = match ? match[1] : '';
            const codeContent = String(children).replace(/\n$/, '');
            
            return !inline && language ? (
              <div style={{ position: "relative", margin: "8px 0" }}>
                <SyntaxHighlighter
                  style={vscDarkPlus}
                  language={language}
                  PreTag="div"
                  customStyle={{
                    borderRadius: "6px",
                    fontSize: "12px",
                    lineHeight: "1.4",
                    paddingTop: "40px"
                  }}
                  {...props}
                >
                  {codeContent}
                </SyntaxHighlighter>
                {/* 語言標籤和複製按鈕 */}
                <div
                  style={{
                    position: "absolute",
                    top: "8px",
                    left: "12px",
                    right: "12px",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    fontSize: "11px",
                    color: "#999",
                  }}
                >
                  <span style={{ 
                    textTransform: "uppercase",
                    fontWeight: "500",
                    color: "#8b949e"
                  }}>
                    {language}
                  </span>
                  <Button
                    type="text"
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={() => copyToClipboard(codeContent)}
                    style={{
                      color: "#8b949e",
                      border: "none",
                      background: "transparent",
                      padding: "0 4px",
                      height: "20px",
                      fontSize: "11px"
                    }}
                  />
                </div>
              </div>
            ) : (
              <code 
                className={className} 
                style={{
                  backgroundColor: "#f5f5f5",
                  padding: "2px 4px",
                  borderRadius: "3px",
                  fontSize: "13px",
                  color: "#d63384"
                }}
                {...props}
              >
                {children}
              </code>
            );
          },
          p: ({ children }) => (
            <div style={{ margin: "4px 0", lineHeight: "1.5" }}>
              {children}
            </div>
          ),
          h1: ({ children }) => (
            <h1 style={{ fontSize: "16px", fontWeight: "bold", margin: "8px 0 4px 0" }}>
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 style={{ fontSize: "15px", fontWeight: "bold", margin: "6px 0 4px 0" }}>
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 style={{ fontSize: "14px", fontWeight: "bold", margin: "4px 0 2px 0" }}>
              {children}
            </h3>
          ),
          ul: ({ children }) => (
            <ul style={{ margin: "4px 0", paddingLeft: "16px" }}>
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol style={{ margin: "4px 0", paddingLeft: "16px" }}>
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li style={{ margin: "2px 0" }}>
              {children}
            </li>
          ),
          blockquote: ({ children }) => (
            <blockquote style={{
              borderLeft: "3px solid #ddd",
              paddingLeft: "8px",
              margin: "8px 0",
              fontStyle: "italic",
              color: "#666"
            }}>
              {children}
            </blockquote>
          ),
            table: ({ children }) => (
            <table
                style={{
                borderCollapse: "collapse",
                width: "100%",
                margin: "8px 0",
                }}
            >
                {children}
            </table>
            ),
            th: ({ children }) => (
            <th
                style={{
                border: "1px solid #ddd",
                padding: "6px 8px",
                backgroundColor: "#f5f5f5",
                fontWeight: "bold",
                textAlign: "left",
                }}
            >
                {children}
            </th>
            ),
            td: ({ children }) => (
            <td
                style={{
                border: "1px solid #ddd",
                padding: "6px 8px",
                }}
            >
                {children}
            </td>
            ),
            tr: ({ children }) => (
            <tr style={{ borderBottom: "1px solid #ddd" }}>{children}</tr>
            ),
        }}
      >
        {content}
      </ReactMarkdown>
    );
  };

  // 模擬 AI 回應
  const aiResponses = [
    // "很高興為您服務！有什麼問題我可以幫忙解答嗎？",
    // "這是一個很好的問題！我會盡力幫助您。",
    // "感謝您的詢問，讓我為您解答。",
    // "我理解您的需求，這邊有一些建議給您參考。",
    // "非常感謝您使用我們的服務！",
    // "關於您的問題，我建議您可以嘗試以下方法：",
    // "這是一個常見的問題，讓我為您詳細說明。",
    // "如果您需要更多幫助，請隨時告訴我！",
    `這裡是一個 Python 範例：

\`\`\`python
def fibonacci(n):
    """計算斐波那契數列的第n項"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 測試函數
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
\`\`\`

這個函數使用遞迴來計算斐波那契數列。`,
    `以下是 JavaScript 的陣列操作範例：

\`\`\`javascript
const numbers = [1, 2, 3, 4, 5];

// 使用 map 轉換陣列
const doubled = numbers.map(x => x * 2);
console.log('雙倍:', doubled);

// 使用 filter 過濾陣列
const evens = numbers.filter(x => x % 2 === 0);
console.log('偶數:', evens);

// 使用 reduce 計算總和
const sum = numbers.reduce((acc, x) => acc + x, 0);
console.log('總和:', sum);
\`\`\``,
    `React Hook 的使用範例：

\`\`\`tsx
import React, { useState, useEffect } from 'react';

const Counter: React.FC = () => {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    document.title = \`計數器: \${count}\`;
  }, [count]);
  
  return (
    <div>
      <p>目前計數: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
    </div>
  );
};
\`\`\`

這個組件展示了 useState 和 useEffect 的基本用法。`,

`
| 語言       | 特點                  |
| ---------- | --------------------- |
| Python     | 易讀、適合快速開發     |
| JavaScript | 網頁前端必備語言       |
| C++        | 高效能、適合系統程式   |
`

  ];

  const sendMessage = () => {
    if (!currentMessage.trim()) return;

    // 添加用戶消息
    const userMessage: Message = {
      id: Date.now().toString(),
      text: currentMessage,
      user: {
        id: "user",
        name: "您",
      },
      created_at: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage("");

    // 模擬 AI 回應（延遲 1-2 秒）
    const delay = 100 ;//+  Math.random() * 1000 ;
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: aiResponses[Math.floor(Math.random() * aiResponses.length)],
        user: {
          id: "ai-assistant",
          name: "AI 助手",
          image: "🤖",
        },
        created_at: new Date(),
      };
      setMessages(prev => [...prev, aiMessage]);
    }, delay);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* 聊天氣泡按鈕 */}
      {!isOpen && (
        <Button
          type="primary"
          shape="circle"
          size="large"
          icon={<MessageOutlined />}
          onClick={() => setIsOpen(true)}
          style={{
            position: "fixed",
            bottom: "24px",
            right: "24px",
            width: "60px",
            height: "60px",
            zIndex: 1000,
            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
          }}
        />
      )}

      {/* 聊天對話框 */}
      {isOpen && (
        <div
          style={{
            position: "fixed",
            bottom: "24px",
            right: "24px",
            width: "500px",
            height: "700px",
            zIndex: 1000,
            backgroundColor: "white",
            borderRadius: "12px",
            boxShadow: "0 8px 24px rgba(0, 0, 0, 0.15)",
            border: "1px solid #d9d9d9",
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* 聊天窗口標題欄 */}
          <div
            style={{
              padding: "12px 16px",
              backgroundColor: "#1677ff",
              color: "white",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span style={{ fontWeight: "500" }}>💬 AI Tien-Wei Hsu</span>
            <div style={{ display: "flex", gap: "8px" }}>
              <Tooltip title="清除對話">
                <Button
                  type="text"
                  size="small"
                  icon={<ClearOutlined />}
                  onClick={clearMessages}
                  style={{ color: "white" }}
                />
              </Tooltip>
              <Button
                type="text"
                size="small"
                icon={<CloseOutlined />}
                onClick={() => setIsOpen(false)}
                style={{ color: "white" }}
              />
            </div>
          </div>

          {/* 聊天訊息區域 */}
          <div 
            style={{ 
              flex: 1, 
              overflow: "auto", 
              padding: "16px",
              display: "flex",
              flexDirection: "column",
              gap: "12px",
              backgroundColor: "#fafafa"
            }}
          >
            {messages.map((message) => (
              <div
                key={message.id}
                style={{
                  display: "flex",
                  justifyContent: message.user.id === "user" ? "flex-end" : "flex-start",
                  alignItems: "flex-start",
                  gap: "8px",
                }}
              >
                {message.user.id !== "user" && (
                  <div
                    style={{
                      width: "32px",
                      height: "32px",
                      borderRadius: "50%",
                      backgroundColor: "#f0f0f0",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "16px",
                      flexShrink: 0,
                    }}
                  >
                    {message.user.image || <UserOutlined />}
                  </div>
                )}
                
                <div
                  style={{
                    maxWidth: "70%",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: message.user.id === "user" ? "flex-end" : "flex-start",
                  }}
                >
                  <div
                    style={{
                      padding: "8px 12px",
                      borderRadius: "12px",
                      backgroundColor: message.user.id === "user" ? "#1677ff" : "white",
                      color: message.user.id === "user" ? "white" : "black",
                      fontSize: "14px",
                      lineHeight: "1.4",
                      boxShadow: "0 1px 2px rgba(0, 0, 0, 0.1)",
                      border: message.user.id !== "user" ? "1px solid #f0f0f0" : "none",
                      maxWidth: "100%",
                      overflow: "hidden",
                    }}
                  >
                    {message.user.id === "user" ? (
                      // 用戶訊息直接顯示純文字
                      <div style={{ whiteSpace: "pre-wrap" }}>
                        {message.text}
                      </div>
                    ) : (
                      // AI 訊息使用 Markdown 渲染
                      <div style={{ color: "black" }}>
                        <MarkdownMessage content={message.text} />
                      </div>
                    )}
                  </div>
                  <div
                    style={{
                      fontSize: "11px",
                      color: "#999",
                      marginTop: "4px",
                      marginLeft: "8px",
                      marginRight: "8px",
                    }}
                  >
                    {message.created_at.toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>

                {message.user.id === "user" && (
                  <Avatar 
                    size={32} 
                    icon={<UserOutlined />} 
                    style={{ backgroundColor: "#1677ff", flexShrink: 0 }} 
                  />
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* 輸入框區域 */}
          <div
            style={{
              padding: "12px 16px",
              borderTop: "1px solid #f0f0f0",
              backgroundColor: "white",
              display: "flex",
              gap: "8px",
              alignItems: "flex-end",
            }}
          >
            <Input.TextArea
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="輸入訊息... (支援 Markdown 語法，Enter 發送，Shift+Enter 換行)"
              autoSize={{ minRows: 1, maxRows: 3 }}
              style={{ 
                flex: 1,
                resize: "none",
                border: "1px solid #d9d9d9",
                borderRadius: "8px",
              }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={sendMessage}
              disabled={!currentMessage.trim()}
              style={{
                height: "32px",
                borderRadius: "8px",
              }}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatPage;

