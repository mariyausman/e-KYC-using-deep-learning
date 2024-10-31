import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleVerifyNowClick = () => {
    navigate('/upload'); // Navigates to the /upload route
  };

  return (
    <div className="flex flex-col-reverse md:flex-row items-center justify-between p-6 pb-0 md:p-12 min-h-screen">
      {/* Text Section */}
      <div className="md:w-1/2 space-y-4 text-center md:text-left">
        <h1 className="text-4xl md:text-5xl font-semibold text-gray-600">
          Welcome to e-KYC
        </h1>
        <p className="text-lg md:text-xl text-gray-600">
          Our platform offers a seamless and secure electronic KYC process to
          verify your identity quickly and efficiently.
        </p>
        <button 
          onClick={handleVerifyNowClick}
          className="px-6 py-2 bg-white font-semibold rounded-md shadow-md shadow-indigo-200 hover:shadow-lg hover:bg-[#e4eaf9e6] transition duration-200"
        >
          <span className="text-transparent text-lg bg-clip-text bg-gradient-to-r from-purple-500 to-blue-600">
            Verify Now
          </span>
        </button>
      </div>

      {/* Image Section */}
      <div className="md:w-1/2 mb-8 md:mb-0 flex justify-center">
        <img
          src="../hero_img.png" // Path to your image in the public folder
          alt="e-KYC illustration"
          className="w-full max-w-sm md:max-w-md object-cover"
        />
      </div>
    </div>
  );
};

export default Home;
