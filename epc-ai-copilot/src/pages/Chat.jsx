import { Collapse } from "@mui/material";
import { motion } from "framer-motion";
import { useMemo, useRef, useEffect, useState } from "react";
import { FaPaperPlane, FaRobot, FaUser, FaLightbulb } from "react-icons/fa";
import AIMetadata from "../components/AIMetadata";
import { chat } from "../services/api";
import "../styles/chat.css";

const QUICK_PROMPTS = [
  { label: "Summarize Risks", icon: "⚠️", prompt: "Summarize all critical risks on this project." },
  { label: "Generate Executive Report", icon: "📋", prompt: "Generate an executive summary report of the project status." },
  { label: "Explain Compliance Issues", icon: "🔍", prompt: "Explain the top compliance issues and their business impact." },
  { label: "Show Delayed Vendors", icon: "🚚", prompt: "Which vendors are delayed and what is the schedule impact?" },
  { label: "Predict Project Completion", icon: "📅", prompt: "Predict the project completion date based on current progress." },
  { label: "Find Missing Documents", icon: "📄", prompt: "What specification documents or drawings are missing or incomplete?" }
];

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Welcome to EPC Orbit AI Chat. Ask me about compliance gaps, risk exposure, delivery status, vendor performance, or commissioning readiness.",
      citations: []
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [openCitation, setOpenCitation] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async (text = input) => {
    const trimmed = text.trim();
    if (!trimmed) return;

    const nextMessages = [...messages, { role: "user", content: trimmed, citations: [] }];
    setMessages(nextMessages);
    setInput("");
    setIsTyping(true);

    try {
      const response = await chat({ message: trimmed });
      setMessages([
        ...nextMessages,
        {
          role: "assistant",
          content: response.answer || response.message,
          citations: response.citations || []
        }
      ]);
    } catch {
      setMessages([
        ...nextMessages,
        {
          role: "assistant",
          content:
            "I could not reach the EPC Orbit backend yet. The AI Chat is ready and will connect when FastAPI is running.",
          citations: []
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <section className="chat-page">
      <div className="chat-shell glass-panel">
        {/* ── History Sidebar ───────────────────────────────── */}
        <aside className="chat-history">
          <span className="section-label">Chat History</span>
          <button type="button">Project controls review</button>
          <button type="button">Compliance exception list</button>
          <button type="button">Commissioning readiness</button>
          <button type="button">Vendor risk analysis</button>
        </aside>

        {/* ── Chat Main ────────────────────────────────────── */}
        <main className="chat-main">
          <div className="chat-heading">
            <span className="section-label">AI Chat</span>
            <h1>EPC Orbit AI Assistant</h1>
            <p className="chat-sub">Powered by Gemini · RAG-enhanced · Project Synapse</p>
          </div>

          {/* ── Quick Prompts ─────────────────────────────── */}
          <div className="prompt-chips" aria-label="Quick prompts">
            {QUICK_PROMPTS.map((chip) => (
              <button
                type="button"
                key={chip.label}
                className="prompt-chip"
                onClick={() => sendMessage(chip.prompt)}
                title={chip.prompt}
              >
                <span className="chip-icon">{chip.icon}</span>
                {chip.label}
              </button>
            ))}
          </div>

          {/* ── Messages ─────────────────────────────────── */}
          <div className="message-list">
            {messages.map((message, index) => (
              <motion.div
                className={`message message-${message.role}`}
                key={`${message.role}-${index}`}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.22 }}
              >
                <span className={`message-avatar message-avatar-${message.role}`}>
                  {message.role === "assistant" ? <FaRobot /> : <FaUser />}
                </span>
                <div className="message-body">
                  <p>{message.content}</p>

                  {/* Citations */}
                  {message.citations?.length > 0 && (
                    <div className="citation-list">
                      {message.citations.map((citation, citationIndex) => {
                        const key = `${index}-${citationIndex}`;
                        return (
                          <div key={key}>
                            <button
                              type="button"
                              className="citation-badge"
                              onClick={() =>
                                setOpenCitation(openCitation === key ? null : key)
                              }
                            >
                              📄 {citation.document || citation.source || "Source"}
                              {citation.page ? ` · p.${citation.page}` : ""}
                            </button>
                            <Collapse in={openCitation === key}>
                              <div className="citation-snippet">{citation.snippet}</div>
                            </Collapse>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* AI metadata on assistant messages */}
                  {message.role === "assistant" && (
                    <AIMetadata
                      source={
                        message.citations?.[0]?.document ||
                        message.citations?.[0]?.source
                      }
                      page={message.citations?.[0]?.page}
                    />
                  )}
                </div>
              </motion.div>
            ))}

            {isTyping && (
              <div className="typing-indicator" aria-label="AI is typing">
                <span className="message-avatar message-avatar-assistant">
                  <FaRobot />
                </span>
                <div className="typing-dots">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* ── Input ────────────────────────────────────── */}
          <form
            className="chat-input"
            onSubmit={(event) => {
              event.preventDefault();
              sendMessage();
            }}
          >
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask EPC Orbit about compliance, risk, vendors, schedule…"
            />
            <button type="submit" aria-label="Send message" disabled={!input.trim()}>
              <FaPaperPlane />
            </button>
          </form>
        </main>
      </div>
    </section>
  );
}
