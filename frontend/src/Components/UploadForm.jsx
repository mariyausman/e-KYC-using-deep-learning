import React, { useState } from 'react';
import axios from 'axios';
import OTP from './OTP'; 
import toast, { Toaster } from 'react-hot-toast';

function UploadForm() {
  const [aadhar, setAadhar] = useState(null);
  const [pan, setPan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showOtpVerification, setShowOtpVerification] = useState(false); // State to control OTP component display

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!aadhar || !pan) {
      alert("Please upload both Aadhaar and PAN images.");
      return;
    }

    const formData = new FormData();
    formData.append('aadhar', aadhar);
    formData.append('pan', pan);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      toast.success("Files uploaded successfully!");
      
      setTimeout(() => {
        toast.success(response.data.message);
        setShowOtpVerification(true);
      }, 1000);

    } catch (error) {
      toast.error(error.response?.data?.error || "File upload failed");
    } finally {
      setLoading(false);
    }
  };

  if (showOtpVerification) {
    return <OTP />; 
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-200 p-6">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">Step 1: Upload Aadhaar and PAN</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Aadhaar Input */}
          <div>
            <label className="block text-gray-600 font-semibold mb-2" htmlFor="aadhar">
              Aadhaar Image
            </label>
            <input
              type="file"
              id="aadhar"
              accept="image/*"
              onChange={(e) => setAadhar(e.target.files[0])}
              className="block w-full text-gray-800 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
              required
            />
          </div>

          {/* PAN Input */}
          <div>
            <label className="block text-gray-600 font-semibold mb-2" htmlFor="pan">
              PAN Image
            </label>
            <input
              type="file"
              id="pan"
              accept="image/*"
              onChange={(e) => setPan(e.target.files[0])}
              className="block w-full text-gray-800 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
              required
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className={`w-full py-3 rounded-lg font-semibold text-white transition duration-200 ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-[#4f0c93b0] hover:bg-purple-700"
            }`}
            disabled={loading}
          >
            {loading ? "Uploading..." : "Submit"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default UploadForm;
