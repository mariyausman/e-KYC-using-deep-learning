import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './index.css';

import App from './App.jsx';
import Navbar from './Components/Navbar.jsx';
import Footer from './Components/Footer.jsx';
import Home from './Components/Home.jsx';
import OTP from './Components/OTP.jsx';
import UploadForm from './Components/UploadForm.jsx';
import TestConnection from './Components/TestConnection.jsx';
import LivenessCheck from './Components/LivenessCheck.jsx';
import Verified from './Components/Verified.jsx';


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Toaster/>
      <Navbar />
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/liveness" element={<LivenessCheck/>} />
        <Route path="/upload" element={<UploadForm />} /> {/* Assuming App is the UploadForm component */}
        <Route path="/otp" element={<OTP />} />
        <Route path="/verified" element={<Verified />} />
        <Route path="/test-connection" element={<TestConnection />} />
      </Routes>

      <Footer />
    </Router>
  </StrictMode>
);
