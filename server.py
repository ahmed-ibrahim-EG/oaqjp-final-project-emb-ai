"""Flask web application for Emotion Detection."""
from flask import Flask, render_template, request

from EmotionDetection import emotion_detector, EmotionServiceError

app = Flask(  # pylint: disable=invalid-name
    __name__, template_folder="templates", static_folder="static"
)

INVALID_TEXT_MESSAGE = "Invalid text! Please try again!"
SERVICE_ERROR_MESSAGE = (
    "The emotion analysis service is temporarily unavailable. "
    "Please try again later."
)


@app.route("/")
def render_index_page():
    """Render the main page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emot_detector():
    """Analyse the text sent in the textToAnalyze query parameter."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return INVALID_TEXT_MESSAGE, 400

    try:
        result = emotion_detector(text_to_analyze)
    except EmotionServiceError:
        return SERVICE_ERROR_MESSAGE, 503

    if result["dominant_emotion"] is None:
        return INVALID_TEXT_MESSAGE, 400

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
