document.addEventListener("DOMContentLoaded", () => {
    const scanBtn = document.getElementById("scan-btn");
    const screenshotImg = document.getElementById("screenshot");
    const resultText = document.getElementById("result");

    scanBtn.addEventListener("click", () => {
        chrome.runtime.sendMessage({ action: "capture_screenshot" }, (response) => {
            if (response && response.screenshot) {
                screenshotImg.src = response.screenshot;
                screenshotImg.style.display = "block";
                sendToBackend(response.screenshot);
            } else {
                resultText.textContent = "Failed to capture screenshot.";
                resultText.style.color = "red";
            }
        });
    });

    async function sendToBackend(imageUri) {
        const blob = await fetch(imageUri).then(res => res.blob());
        const formData = new FormData();
        formData.append("file", blob, "screenshot.png");

        try {
            const response = await fetch("http://localhost:5000/predict", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            resultText.textContent = `Result: ${data.prediction} (Confidence: ${data.confidence.toFixed(2)})`;
            resultText.style.color = data.prediction === "Phishing" ? "red" : "green";
        } catch (error) {
            console.error("Error:", error);
            resultText.textContent = "Error analyzing the image.";
            resultText.style.color = "red";
        }
    }
});
