// App.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './Components/Navbar';
import Footer from './Components/Footer';
import Home from './Components/Home';
import OTP from './Components/OTP';
import UploadForm from './Components/UploadForm';
import TestConnection from './Components/TestConnection';
import LivenessCheck from './Components/LivenessCheck';
import Verified from './Components/Verified';

const App = () => {
  return (
    <div className="app">
      <Navbar />

      <main className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/liveness" element={<LivenessCheck />} />
          <Route path="/upload" element={<UploadForm />} />
          <Route path="/otp" element={<OTP />} />
          <Route path="/verified" element={<Verified />} />
          <Route path="/test-connection" element={<TestConnection />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
};

export default App;
