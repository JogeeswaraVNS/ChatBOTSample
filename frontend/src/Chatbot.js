import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import "./Chatbot.css";
import logo from "C:/Users/jogee/Desktop/ChatBOT/frontend/src/VNRVJIETLogo.png";
import SendIcon from "@mui/icons-material/Send";
import { Modal, ModalBody, ModalFooter } from "react-bootstrap";

const Chatbot = () => {
  const [pdfUrl, setPdfUrl] = useState("");

  const [pdfId, setpdfId] = useState("");

  const [showpdf, setshowpdf] = useState(false);

  useEffect(() => {
    const fetchPdf = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/view/${pdfId}`,
          {
            responseType: "blob",
          }
        );
        const url = URL.createObjectURL(
          new Blob([response.data], { type: "application/pdf" })
        );
        setPdfUrl(url);
      } catch (error) {
        console.error("Error fetching the PDF", error);
      }
    };

    fetchPdf();
    return () => {
      URL.revokeObjectURL(pdfUrl);
    };
  }, [pdfId]);

  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I assist you today?" },
  ]);
  const [userMessage, setUserMessage] = useState("");
  const [ResponseTime, setResponseTime] = useState("");
  const chatEndRef = useRef(null);

  const handleInputChange = (e) => {
    setUserMessage(e.target.value);
  };

  const handleSendMessage = async () => {
    if (userMessage.trim() === "") return;
    setMessages([...messages, { sender: "user", text: userMessage }]);

    try {
      const response = await axios.post("http://localhost:5000/chat", {
        message: userMessage,
      });

      const botMessage = response.data.response.response;
      const botData = response.data.response.data;

      console.log(response.data.response.data);
      setResponseTime(response.data.response_time);

      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: botMessage, data: botData },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    }

    setUserMessage("");
  };

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div style={{ whiteSpace: "pre-line" }} className="chat-container mt-5">
      <Modal show={showpdf} backdrop="static" centered className="modal-lg">
        <div style={{ display: "flex", justifyContent: "space-around" }}>
          <div style={{ marginRight: "auto" }}></div>

          <div style={{ display: "flex", justifyContent: "flex-end" }}>
            <button
              className="btn-close pt-5 pe-5"
              type="button"
              onClick={() => setshowpdf(false)}
            ></button>
          </div>
        </div>

        <ModalBody style={{ marginTop: "-2rem", marginBottom: "1.5rem" }}>
          <div>
            {pdfUrl ? (
              <iframe
                src={pdfUrl}
                style={{ width: "100%", height: "600px" }}
                frameBorder="0"
              ></iframe>
            ) : (
              <p>Loading PDF...</p>
            )}
          </div>
        </ModalBody>
      </Modal>
      <div style={{ fontSize: "1.3rem" }} className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            {msg.sender === "bot" && (
              <img
                style={{ borderRadius: "50%" }}
                src={logo}
                alt="Bot Logo"
                className="bot-logo"
              />
            )}
            <div className={`message-bubble ${msg.sender}`}>
              <div className="px-2">{msg.text}</div>
              {msg.sender === "bot" && msg.data && msg.data.length !== 0 && (
                <div
                  style={{ overflowX: "auto", maxHeight: "50vh" }}
                  className="px-2 my-3"
                >
                  {msg.data && msg.data.length > 0 && (
                    <table
                      style={{ fontSize: "1.2rem", tableLayout: "auto" }}
                      className="table table-bordered table-auto"
                    >
                      <thead className="table-primary">
                        <tr>
                          {Object.keys(msg.data[0])
                            .filter((key) => key !== "id")
                            .map((key) => (
                              <th key={key} style={{ whiteSpace: "nowrap" }}>
                                {key
                                  .replace(/_/g, " ")
                                  .replace(/\b\w/g, (l) =>
                                    l.toUpperCase()
                                  )}{" "}
                              </th>
                            ))}
                        </tr>
                      </thead>

                      <tbody>
                        {msg.data.map((item, id) => (
                          <tr key={id}>
                            {Object.keys(item).map((key) => {
                              if (key === "id") return null;
                              return (
                                <td key={key}>
                                  {key === "invoice_no" ? (
                                    <div
                                      onClick={() => {
                                        setpdfId(item["id"]);
                                        setshowpdf(true);
                                      }}
                                      style={{ width: "100%" }}
                                      className="btn btn-success"
                                    >
                                      {item[key]}
                                    </div>
                                  ) : (
                                    item[key]
                                  )}
                                </td>
                              );
                            })}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              )}
              {ResponseTime.length !== 0 && msg.sender === "bot" && (
                <div className="ps-2" style={{ fontSize: "1rem" }}>
                  Generated Response in {ResponseTime} secs
                </div>
              )}
            </div>
            {msg.sender === "user" && (
              <AccountCircleIcon className="ms-2" style={{ fontSize: 40 }} />
            )}
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      <div className="input-container input-group">
        <input
          style={{ fontSize: "1.3rem" }}
          className="form-control p-3 w-75"
          type="text"
          placeholder="Type your message..."
          value={userMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
        />
        <button
          className="btn btn-primary form-control"
          onClick={handleSendMessage}
        >
          <div style={{ display: "flex", justifyContent: "center" }}>
            <div>
              <h5>Send</h5>
            </div>
            <div>
              <SendIcon className="ps-1" />
            </div>
          </div>
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
