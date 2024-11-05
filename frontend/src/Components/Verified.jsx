import React, { useEffect } from "react";
import { FaCheckCircle } from "react-icons/fa";
import confetti from "canvas-confetti";

const KYCVerifiedPage = () => {
  useEffect(() => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ["#dfe6e9", "#594ef4", "#81ecec", "#14d2ef"],
    });
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-200 via-indigo-200 to-purple-200 text-gray-800 p-6">
      <div className="bg-slate-100 rounded-lg shadow-lg p-8 w-full max-w-md text-center">
        <FaCheckCircle className="text-green-500 text-6xl mx-auto mb-4" />
        <h1 className="text-3xl font-semibold mb-2">KYC Verified!</h1>
        <p className="text-lg mb-6">
          Congratulations, Your KYC has been successfully verified. You are now
          authorized to access all features.
        </p>
        <button
          className="bg-[#7c5ed6] text-white px-6 py-2 font-semibold rounded-lg hover:bg-purple-500 transition duration-300"
          onClick={() => (window.location.href = "/")}
        >
          Go to Dashboard
        </button>
      </div>
    </div>
  );
};

export default KYCVerifiedPage;
