import React, { useState } from "react";
import axios from "axios";


function ChatInterface({ sendMessage }) {
  const [msg, setMsg] = useState("");
  const [reply, setReply] = useState("");
  const [lastPrompt, setLastPrompt] = useState("");

  const sendMsg = async () => {
    if (!msg.trim()) return;

    setLastPrompt(msg);

    // compute heuristics immediately so they can be used even on pure corrections
    const heuristics = parsePrompt(msg);

    // look for a simple correction pattern: "not <old> this <new>"
    const corrMatch = msg.match(/not\s+(\w+).*this\s+(\w+)/i);
    if (corrMatch) {
      const [, wrongName, correctName] = corrMatch;
      setReply(`✏️ Updated doctor name to '${correctName}'.`);
      if (sendMessage) {
        // send correction first
        sendMessage({ correction: { field: "doctor_name", value: correctName } });
        // also share any other heuristics discovered
        if (Object.keys(heuristics).length > 0) {
          sendMessage(heuristics);
        }
      }
      // if heuristics are empty, it's a pure correction; skip backend call
      if (Object.keys(heuristics).length === 0) {
        setMsg("");
        return;
      }
      // otherwise we fall through to backend so we can refresh additional info
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", { message: msg });
      console.log("Backend Response:", res.data);

      setReply("Interaction details extracted successfully");

      let serverData = res.data?.data || res.data || {};

      // merge heuristics and server data, but don't let empty strings from server wipe good heuristics
      const extracted = { ...heuristics };
      Object.keys(serverData).forEach(key => {
        const val = serverData[key];
        if (val !== undefined && val !== null && val !== "") {
          extracted[key] = val;
        }
      });

      if (sendMessage && Object.keys(extracted).length > 0) {
        sendMessage(extracted);
      }
    } catch (error) {
      console.error("Chatbot Error:", error);
      setReply("⚠️ Unable to process message. Please try again.");
    } finally {
      setMsg("");
    }
  };

  // simple rule-based extraction from prompt text
  function parsePrompt(text) {
    const result = {};
    if (!text) return result;
    // doctor name after 'Met Dr.' or 'met Dr.'
    const nameMatch = text.match(/met\s+Dr\.?\s+([A-Za-z ]+)/i);
    if (nameMatch) {
      result.doctor_name = nameMatch[1].trim();
    }
    // discussion: after explained/discussed
    const discMatch = text.match(/(?:explained|discussed|talked about)\s+(.+?)(?:\.|,| and|\n|$)/i);
    if (discMatch) {
      result.discussion = discMatch[1].trim();
    }
    // outcome: look for appreciative/agreements
    const outMatch = text.match(/(?:Doctor\s+)?appreciated[^.]*\.?|agreed to[^.]*\.?/i);
    if (outMatch) {
      result.outcome = outMatch[0].trim();
    }
    // follow-up phrase
    const followMatch = text.match(/follow(?:\s*up)?(?:\s*in)?\s+([^\.]+)/i);
    if (followMatch) {
      result.followup = followMatch[1].trim();
    }
    // materials
    const materials = [];
    if (/brochure|brocher|pdf|flyer/i.test(text)) materials.push("Brochure");
    if (materials.length) result.materials = materials;
    // sentiment only when explicitly positive/negative
    if (/\b(?:appreciated|agreed|positive|good|great|success|benefit|advantage)\b/i.test(text)) {
      result.sentiment = "Positive";
    } else if (/\b(?:negative|not interested|concern|issue|problem)\b/i.test(text)) {
      result.sentiment = "Negative";
    }
    return result;
  }

  return (
    <div className="container d-flex justify-content-center" style={{ height: "100%" }}>
      <div className="card shadow" style={{ width: "420px", height: "650px" }}>
        <div className="card-body d-flex flex-column">
          <h5 className="mb-0">🌐 AI Assistant</h5>
          <small className="text-muted mb-3">Log interaction via chat</small>

          <div className="border rounded p-2 mb-3" style={{ height: "480px", background: "#f8f9fa", overflowY: "auto" }}>
            <div className="alert alert-light small">
              Log interaction details here (e.g. "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.
            </div>


            {lastPrompt && (
              <div className="alert alert-secondary small mt-2">
                <strong>Prompt:</strong> {lastPrompt}
              </div>
            )}
            {reply && <div className="alert alert-info mt-2">{reply}</div>}
          </div>

          <div className="d-flex">
            <input
              type="text"
              className="form-control me-2"
              placeholder="Describe interaction..."
              value={msg}
              onChange={(e) => setMsg(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMsg()}
            />
            <button
              className="btn btn-secondary"
              style={{ width: "70px", height: "38px", fontSize: "14px" }}
              onClick={sendMsg}
            >
              Log
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatInterface;