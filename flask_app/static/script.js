document.addEventListener("DOMContentLoaded", () => {
    const imageUpload = document.getElementById("imageUpload");
    const uploadButton = document.getElementById("uploadButton");
    const previewSection = document.getElementById("preview-section");
    const imagePreview = document.getElementById("imagePreview");
    const filterSelect = document.getElementById("filterSelect");
    const downloadButton = document.getElementById("downloadButton");
  
    let uploadedImage = null;
  
    uploadButton.addEventListener("click", () => {
      const file = imageUpload.files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          uploadedImage = e.target.result;
          imagePreview.src = uploadedImage;
          previewSection.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
      } else {
        alert("Please upload a valid image file.");
      }
    });
  
    filterSelect.addEventListener("change", () => {
      const filter = filterSelect.value;
      imagePreview.style.filter = filter === "none" ? "" : filter;
    });
  
    downloadButton.addEventListener("click", () => {
      if (uploadedImage) {
        const link = document.createElement("a");
        link.download = "processed-image.png";
        link.href = imagePreview.src;
        link.click();
      } else {
        alert("No image to download.");
      }
    });
  });

  document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
  
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
  
    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      const resultDiv = document.getElementById('result');
  
      if (result.url) {
        resultDiv.innerHTML = `<p>File uploaded! <a href="${result.url}" target="_blank">View Image</a></p>`;
      } else {
        resultDiv.innerHTML = `<p>Error: ${result.error}</p>`;
      }
    } catch (error) {
      console.error(error);
    }
  });
  
  // Example for processing the image
  async function processImage(filename, filter) {
    try {
      const response = await fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename, filter }),
      });
      const result = await response.json();
  
      if (result.url) {
        console.log(`Processed image URL: ${result.url}`);
      } else {
        console.error(result.error);
      }
    } catch (error) {
      console.error(error);
    }
  }