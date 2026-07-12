import { motion } from "framer-motion";
import { useMemo, useState } from "react";
import { FaPaperPlane, FaRobot, FaUser } from "react-icons/fa";
import { chat } from "../services/api";
import "../styles/chat.css";

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Ask me about compliance gaps, risk exposure, delivery status, or commissioning readiness."
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const suggestions = useMemo(
    () => [
      "Summarize top project risks",
      "Find missing vendor clauses",
      "What shipments are delayed?",
      "Show commissioning blockers"
    ],
    []
  );

  const sendMessage = async (text = input) => {
    const trimmed = text.trim();
    if (!trimmed) return;

    const nextMessages = [...messages, { role: "user", content: trimmed }];
    setMessages(nextMessages);
    setInput("");
    setIsTyping(true);

    try {
      const response = await chat({ messages: nextMessages });
      setMessages([...nextMessages, { role: "assistant", content: response.message || response.answer }]);
    } catch {
      setMessages([
        ...nextMessages,
        {
          role: "assistant",
          content: "I could not reach the FastAPI service yet. The chat UI is ready and will connect when the backend is running."
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <section className="chat-page">
      <div className="chat-shell glass-panel">
        <aside className="chat-history">
          <span className="section-label">Chat History</span>
          <button type="button">Project controls review</button>
          <button type="button">Compliance exception list</button>
          <button type="button">Commissioning readiness</button>
        </aside>

        <main className="chat-main">
          <div className="chat-heading">
            <span className="section-label">AI Chat</span>
            <h1>EPC Copilot Assistant</h1>
          </div>

          <div className="message-list">
            {messages.map((message, index) => (
              <motion.div
                className={`message message-${message.role}`}
                key={`${message.role}-${index}`}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <span className="message-avatar">{message.role === "assistant" ? <FaRobot /> : <FaUser />}</span>
                <p>{message.content}</p>
              </motion.div>
            ))}
            {isTyping && (
              <div className="typing-indicator" aria-label="AI is typing">
                <span />
                <span />
                <span />
              </div>
            )}
          </div>

          <div className="suggestions">
            {suggestions.map((suggestion) => (
              <button type="button" key={suggestion} onClick={() => sendMessage(suggestion)}>
                {suggestion}
              </button>
            ))}
          </div>

          <form className="chat-input" onSubmit={(event) => { event.preventDefault(); sendMessage(); }}>
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask EPC AI Copilot..."
            />
            <button type="submit" aria-label="Send message">
              <FaPaperPlane />
            </button>
          </form>
        </main>
      </div>
    </section>
  );
}
