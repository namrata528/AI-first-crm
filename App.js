import React, { useState } from "react";
import LogForm from "./LogForm";
import ChatInterface from "./ChatInterface";

function App() {

  const [formData, setFormData] = useState({});

  const handleChatData = (data) => {
    // if the chatbot is sending a correction message, apply it
    if (data && data.correction) {
      const { field, value } = data.correction;
      console.log("Received correction", field, value);
      setFormData(prev => ({ ...prev, [field]: value }));
      // continue, in case backend also returned fields below
    }

    console.log("Data received from chatbot:", data);
    if (data) setFormData(prev => ({ ...prev, ...data }));
  };

  return (

    <div className="container mt-4">

      <h2 className="mb-4">
        Log HCP Interaction
      </h2>

      <div className="row">

        <div className="col-md-8">
          <LogForm formData={formData} />
        </div>

        <div className="col-md-4">
          <ChatInterface sendMessage={handleChatData} />
        </div>

      </div>

    </div>

  );

}

export default App;