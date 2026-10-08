async function runEmotionDetector() {
  const textToAnalyze = document.getElementById("textToAnalyze").value;
  const output = document.getElementById("system_response");

  output.className = "";
  output.textContent = "Analyzing...";

  try {
    const url = "/emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze);
    const response = await fetch(url);
    const message = await response.text();
    output.className = response.ok ? "success" : "error";
    output.textContent = message;
  } catch (error) {
    output.className = "error";
    output.textContent = "Network error: could not reach the server.";
  }
}
