document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("imageInput");
    const status = document.getElementById("status");
    const result = document.getElementById("result");
    const outputImage = document.getElementById("outputImage");
    const downloadLink = document.getElementById("downloadLink");

    if (!fileInput.files[0]) {
        alert("Please upload an image.");
        return;
    }

    formData.append("image", fileInput.files[0]);

    status.textContent = "Processing...";
    result.style.display = "none";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            status.textContent = "Conversion Successful!";
            result.style.display = "block";
            outputImage.src = data.output_url;
            downloadLink.href = data.output_url;
        } else {
            status.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        status.textContent = `Error: ${error.message}`;
    }
});
