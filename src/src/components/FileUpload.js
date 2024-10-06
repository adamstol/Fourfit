import React, { useRef, useState } from "react";
import spinner from "../media/spinner.svg";

function FileUpload({ setOutput }) {
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState("");
  const [imagePreview, setImagePreview] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFileName(selectedFile.name);

      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result;
        setImagePreview(base64);
        handleUpload(base64);
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async (base64) => {
    setIsUploading(true);
    try {
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
    } finally {
      setIsUploading(false);
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

      {!isUploading && !imagePreview && (
        <button
          onClick={triggerFileInput}
          className="bg-buttonbg text-white px-4 py-2 rounded hover:bg-red-600"
        >
          {fileName ? `Selected: ${fileName}` : "Upload Image"}
        </button>
      )}

      {isUploading && (
        <div className="flex justify-center items-center h-full">
          <img
            src={spinner}
            alt="Loading..."
            className="w-12 h-12 animate-spin"
          />
        </div>
      )}

      {!isUploading && imagePreview && (
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
