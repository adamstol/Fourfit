import React, { useRef, useState } from "react";

function FileUpload({ setOutput }) {
  // Accept setOutput as a prop
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState("");
  const [imagePreview, setImagePreview] = useState(""); // State for image preview
  const [isUploaded, setIsUploaded] = useState(false); // New state to track upload status

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFileName(selectedFile.name);

      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result;
        setImagePreview(base64); // Set the base64 string for image preview
        handleUpload(base64);
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async (base64) => {
    try {
      setIsUploaded(true);
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file: base64 }),
      });

      if (response.ok) {
        const responseJSON = await response.json();
        setOutput(responseJSON["feedback"]);
      } else {
        alert("Failed to upload file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 space-y-4">
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />

      {!isUploaded && (
        <button
          onClick={triggerFileInput}
          className="bg-buttonbg text-white px-4 py-2 rounded hover:bg-red-600"
        >
          {fileName ? `Selected: ${fileName}` : "Upload Image"}
        </button>
      )}

      {imagePreview && (
        <img
          src={imagePreview}
          alt="Preview"
          className="mt-4 max-w-xs max-h-64 rounded shadow"
        />
      )}
    </div>
  );
}

export default FileUpload;
