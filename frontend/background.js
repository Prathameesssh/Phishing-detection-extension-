chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "capture_screenshot") {
        chrome.tabs.captureVisibleTab(null, { format: "png" }, (imageUri) => {
            if (imageUri) {
                sendResponse({ screenshot: imageUri });
            } else {
                sendResponse({ error: "Screenshot capture failed." });
            }
        });
        return true; // Required for async sendResponse
    }
});
