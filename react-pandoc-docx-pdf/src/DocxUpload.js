import React, { useState } from "react";

const DocxUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [htmlFileUrl, setHtmlFileUrl] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:8000/convert-docx-to-html/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.html_file) {
        console.log("✅ File uploaded:", data.html_file);
        setHtmlFileUrl(data.html_file);
      } else {
        console.error("❌ Error:", data.error);
      }
    } catch (error) {
      console.error("❌ Upload failed:", error);
    }
  };

  return (
    <div>
      <h2>Upload DOCX File</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Convert to HTML</button>

      {htmlFileUrl && (
        <iframe src={htmlFileUrl} title="Converted HTML" width="100%" height="500px"></iframe>
      )}
    </div>
  );
};

export default DocxUpload;
