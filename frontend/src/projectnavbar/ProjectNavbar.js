import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "C:/Users/jogee/Desktop/ChatBOT/frontend/src/VNRVJIETLogo.png";

function ProjectNavbar() {
  const [show, setShow] = useState(false);
  const handleMouseEnter = () => {
    setShow(true);
  };

  const handleMouseLeave = () => {
    setShow(false);
  };
  return (
    <div>
      <div>
        <Navbar expand="lg" style={{ backgroundColor: "#03346E" }}>
          <Container>
            <Navbar.Brand
              className="text-white"
              style={{ fontFamily: "Lexend, sans-serif" }}
              href="/"
            >
              <img style={{ width: "2.2rem" }} src={logo}></img> VNRVJIET Chat
              Bot
            </Navbar.Brand>
            <Nav className="ms-auto">
              <Nav.Link className="text-white" href="/addcomponents">
                Add Components
              </Nav.Link>
            </Nav>
          </Container>
        </Navbar>
      </div>
    </div>
  );
}

export default ProjectNavbar;
