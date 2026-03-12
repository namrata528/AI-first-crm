import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaMicrophone, FaSmile, FaMeh, FaFrown } from "react-icons/fa";

function LogForm({ formData }) {
  const [hcp, setHcp] = useState("");
  const [hospital, setHospital] = useState("");
  const [interactionType, setInteractionType] = useState("Meeting");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [attendees, setAttendees] = useState("");
  const [discussion, setDiscussion] = useState("");
  const [sentiment, setSentiment] = useState("Neutral");
  const [outcome, setOutcome] = useState("");
  const [followup, setFollowup] = useState("");
  const [materials, setMaterials] = useState([]);

  /* AUTO FILL FROM CHATBOT */
  useEffect(() => {
    if (!formData || Object.keys(formData).length === 0) return;
    console.log("Received Chatbot Data:", formData);

    // auto‑date/time when doctor name is set and not already populated
    if (formData.doctor_name && !date && !time) {
      const now = new Date();
      setDate(now.toISOString().slice(0, 10));
      setTime(now.toLocaleTimeString("en-GB", { hour12: false }).slice(0, 5));
    }

    setHcp(formData.doctor_name || "");
    setHospital(formData.hospital || "");
    // pick first sentence/phrase for discussion
    let discussionText = formData.discussion || "";
    discussionText = discussionText.split(/[.?!]\s/)[0];
    setDiscussion(discussionText);
    setOutcome(formData.outcome || "");
    setFollowup(formData.followup || "");
    setSentiment(formData.sentiment || "Neutral");
    if (formData.materials) setMaterials(formData.materials);
  }, [formData]);

  const saveInteraction = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/log_interaction", {
        doctor_name: hcp,
        hospital: hospital,
        interaction_type: interactionType,
        date,
        time,
        attendees,
        discussion,
        sentiment,
        outcome,
        follow_up: followup
      });

      alert("Interaction saved successfully");
    } catch (err) {
      console.error(err);
      alert("Error saving interaction");
    }
  };

  return (
    <div className="card p-4">
      <h5 className="mb-3">Interaction Details</h5>
      <form onSubmit={saveInteraction}>
        <div className="row mb-3">
          <div className="col-md-6">
            <label>HCP Name</label>
            <input className="form-control" placeholder="Search or select HCP..." value={hcp} onChange={(e) => setHcp(e.target.value)} />
          </div>
          <div className="col-md-6">
            <label>Interaction Type</label>
            <select className="form-control" value={interactionType} onChange={(e) => setInteractionType(e.target.value)}>
              <option>Meeting</option>
              <option>Call</option>
              <option>Email</option>
            </select>
          </div>
        </div>

        <div className="row mb-3">
          <div className="col-md-6">
            <label>Date</label>
            <input type="date" className="form-control" value={date} onChange={(e) => setDate(e.target.value)} />
          </div>
          <div className="col-md-6">
            <label>Time</label>
            <input type="time" className="form-control" value={time} onChange={(e) => setTime(e.target.value)} />
          </div>
        </div>

        <div className="mb-3">
          <label>Attendees</label>
          <input className="form-control" placeholder="Enter names or search..." value={attendees} onChange={(e) => setAttendees(e.target.value)} />
        </div>

        <div className="mb-3">
          <label>Topics Discussed</label>
          <textarea className="form-control" rows="3" placeholder="Enter key discussion points..." value={discussion} onChange={(e) => setDiscussion(e.target.value)} />
        </div>

        <button type="button" className="btn btn-light mb-3">
          <FaMicrophone style={{ marginRight: "6px" }} /> Summarize from Voice Note
        </button>

        <h6>Materials Shared / Samples Distributed</h6>
        <div className="card p-2 mb-2">
          <div className="d-flex justify-content-between">
            <span>Materials Shared</span>
            <button type="button" className="btn btn-sm btn-outline-secondary">Search/Add</button>
          </div>
          {materials.length > 0 ? (
            <ul className="mb-0">
              {materials.map((m, idx) => (
                <li key={idx}>{m}</li>
              ))}
            </ul>
          ) : (
            <p className="text-muted">No materials added.</p>
          )}
        </div>

        <div className="card p-2 mb-3">
          <div className="d-flex justify-content-between">
            <span>Samples Distributed</span>
            <button type="button" className="btn btn-sm btn-outline-secondary">Add Sample</button>
          </div>
          <p className="text-muted">No samples added.</p>
        </div>

        <div className="mb-3">
          <label className="mb-2">Observed/Inferred HCP Sentiment</label>
          <div className="d-flex gap-4">
            <label>
              <input type="radio" name="sentiment" value="Positive" checked={sentiment === "Positive"} onChange={(e) => setSentiment(e.target.value)} />
              <FaSmile color="green" style={{ marginLeft: "5px" }} /> Positive
            </label>
            <label>
              <input type="radio" name="sentiment" value="Neutral" checked={sentiment === "Neutral"} onChange={(e) => setSentiment(e.target.value)} />
              <FaMeh color="orange" style={{ marginLeft: "5px" }} /> Neutral
            </label>
            <label>
              <input type="radio" name="sentiment" value="Negative" checked={sentiment === "Negative"} onChange={(e) => setSentiment(e.target.value)} />
              <FaFrown color="red" style={{ marginLeft: "5px" }} /> Negative
            </label>
          </div>
        </div>

        <div className="mb-3">
          <label>Outcomes</label>
          <textarea className="form-control" rows="2" placeholder="Key outcomes or agreements..." value={outcome} onChange={(e) => setOutcome(e.target.value)} />
        </div>

        <div className="mb-3">
          <label>Follow-up Actions</label>
          <textarea className="form-control" rows="2" placeholder="Enter next steps or tasks..." value={followup} onChange={(e) => setFollowup(e.target.value)} />
        </div>

        <div className="mb-3">
          <label>AI Suggested Follow-ups</label>
          <ul className="text-primary">
            <li>Schedule follow-up meeting in 2 weeks</li>
            <li>Send OncoBoost Phase III PDF</li>
            <li>Add Dr. Sharma to advisory board invite list</li>
          </ul>
        </div>

        <button className="btn btn-primary">Save Interaction</button>
      </form>
    </div>
  );
}

export default LogForm;