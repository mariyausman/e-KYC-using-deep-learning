import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const App = () => {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [selfie, setSelfie] = useState(null);
  const [video, setVideo] = useState(null);
  const [aadharImage, setAadharImage] = useState(null);
  const [panImage, setPanImage] = useState(null);
  const [recording, setRecording] = useState(false);

  const captureSelfie = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setSelfie(imageSrc);
  };

  const handleImageChange = (event, setImage) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);
    }
  };

  const startRecording = () => {
    setRecording(true);
    mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
      mimeType: "video/webm",
    });
    let chunks = [];

    mediaRecorderRef.current.ondataavailable = (event) => {
      if (event.data.size > 0) chunks.push(event.data);
    };

    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(chunks, { type: "video/webm" });
      setVideo(blob);
      chunks = [];
    };

    mediaRecorderRef.current.start();

    setTimeout(() => {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }, 5000); // Stop recording after 5 seconds
  };

  const uploadData = async () => {
    if (!selfie || !video || !aadharImage || !panImage) return alert("Please provide selfie, video, Aadhaar, and PAN images.");

    const formData = new FormData();
    formData.append("aadhar", aadharImage, "aadhar.png");
    formData.append("pan", panImage, "pan.png");
    formData.append("selfie", dataURItoBlob(selfie), "selfie.png");
    formData.append("video", video, "video.webm");

    try {
      const response = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        alert("Files uploaded successfully!");
        checkFaceMatch();
      } else {
        alert("Upload failed.");
      }
    } catch (error) {
      console.error("Error uploading files:", error);
      alert("Error uploading files.");
    }
  };

  const dataURItoBlob = (dataURI) => {
    const byteString = atob(dataURI.split(",")[1]);
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
  };

  const checkFaceMatch = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/match", {
        method: "POST",
      });
      const result = await response.json();
      alert(result.message);  // Show "Face match found!" or "Face does not match."
    } catch (error) {
      console.error("Error matching faces:", error);
    }
  };  

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-5">
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/png"
        className="w-52 h-40 rounded-lg"
      />
      <button onClick={captureSelfie} className="m-2 px-4 py-2 text-white bg-blue-600 rounded">
        Capture Selfie
      </button>
      <button onClick={startRecording} disabled={recording} className={`m-2 px-4 py-2 text-white rounded ${recording ? 'bg-gray-400' : 'bg-blue-600'}`}>
        {recording ? "Recording..." : "Start Recording Video"}
      </button>

      <div className="mt-5 text-center">
        <label className="block mb-2 font-semibold">Upload Aadhaar Image:</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleImageChange(e, setAadharImage)}
          className="mb-5"
        />
        <label className="block mb-2 font-semibold">Upload PAN Image:</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleImageChange(e, setPanImage)}
          className="mb-5"
        />
      </div>

      <button onClick={uploadData} className="m-2 px-4 py-2 text-white bg-blue-600 rounded">
        Upload
      </button>

      {selfie && (
        <div className="mt-5 text-center">
          <h4 className="font-semibold">Selfie Preview</h4>
          <img src={selfie} alt="Selfie" className="w-52 h-auto rounded-lg mt-2" />
        </div>
      )}

      {video && (
        <div className="mt-5 text-center">
          <h4 className="font-semibold">Video Preview</h4>
          <video src={URL.createObjectURL(video)} controls className="w-52 h-auto rounded-lg mt-2" />
        </div>
      )}
    </div>
  );
};

export default App;
