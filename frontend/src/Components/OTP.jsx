import React, { useState } from "react";
import axios from "axios";

const OTP = () => {
  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");

  // Function to verify OTP
  const verifyOtp = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/verify_otp", {
        otp_code: otp,
      });
      if (response.data.message === "OTP verified successfully.") {
        setMessage("OTP verified successfully!");
        setTimeout(() => {
          window.location.href = "http://localhost:5173/liveness";
        }, 3000);
      } else {
        setMessage("Invalid OTP. Please try again.");
      }
    } catch (error) {
      setMessage("Error verifying OTP. Please try again.");
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-200">
      <div className="w-full max-w-md p-6 bg-white shadow-md rounded-lg">
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">
          Step 2: OTP Verification
        </h2>

        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          className="w-full text-gray-600 px-4 py-2 mb-4 border rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={verifyOtp}
          className="w-full px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-600 transition duration-200"
        >
          Verify OTP
        </button>

        {message && (
          <p className="mt-4 text-center text-lg text-gray-700 font-semibold">
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default OTP;
