import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import { useReactMediaRecorder } from "react-media-recorder";
import toast, { Toaster } from "react-hot-toast";
import { FaSpinner } from "react-icons/fa"; // Import spinner icon

const LivenessCheck = () => {
  const webcamRef = useRef(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Configure the video recorder
  const { startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder(
    {
      video: true,
      blobPropertyBag: { type: "video/mp4" },
    }
  );

  const handleStartRecording = () => {
    toast.success("Recording started");
    startRecording();
    setTimeout(() => handleStopRecording(), 10000); // Automatically stop after 10 seconds
  };

  const handleStopRecording = async () => {
    stopRecording();
    setIsProcessing(true);

    // Wait for the video to be available as a blob
    const response = await fetch(mediaBlobUrl);
    const videoBlob = await response.blob();
    const formData = new FormData();
    formData.append("video", videoBlob, "liveness_video.mp4");

    try {
      const apiResponse = await axios.post(
        "http://localhost:5000/api/process_liveness",
        formData
      );

      if (apiResponse.data.message === "No blink detected, please try again!") {
        toast.error("No blink detected. Please try again!");
      } else {
        toast.success("Liveness detection successful");
        setTimeout(() => {
          toast.success(apiResponse.data.message);
        }, 1000);
        setTimeout(() => {
          window.location.href = "http://localhost:5173/verified";
        }, 2000);
      }
    } catch (error) {
      toast.error("Error processing liveness detection.");
      console.error("Error:", error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <Toaster position="top-center" reverseOrder={false} />
      <div className="bg-white shadow-md p-6 rounded-lg w-96 flex flex-col items-center border">
        <h1 className="text-xl text-center text-gray-700 font-semibold mb-4">
          Step 3: Liveness and Face Match Detection
        </h1>
        <p className="pb-2 text-gray-500">Blink normally to detect liveness</p>
        <div className="w-68 h-68 border-2 border-gray-300 rounded-lg overflow-hidden mb-4">
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="w-full h-full object-cover"
            videoConstraints={{ width: 320, height: 240 }}
          />
        </div>
        <button
          onClick={handleStartRecording}
          className="bg-[#4a62a3] hover:bg-[#5d7ac9] text-white px-4 py-2 rounded"
        >
          Start
        </button>
        {isProcessing && (
          <div className="flex items-center mt-4 text-blue-500 text-xl">
            <FaSpinner className="animate-spin mr-2" /> Processing...
          </div>
        )}
      </div>
    </div>
  );
};

export default LivenessCheck;
