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
  