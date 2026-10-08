"""Emotion detection using the IBM Watson NLP EmotionPredict service."""
import json

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
TIMEOUT_SECONDS = 15


class EmotionServiceError(Exception):
    """Raised when the Watson service cannot be reached or replies unexpectedly."""


def _empty_result():
    """Return the result used for invalid input (all values None)."""
    result = {emotion: None for emotion in EMOTIONS}
    result["dominant_emotion"] = None
    return result


def emotion_detector(text_to_analyse):
    """Analyse text and return emotion scores plus the dominant emotion.

    Returns a dict with anger, disgust, fear, joy, sadness and dominant_emotion.
    For HTTP 400 (blank/invalid text) every value is None.
    Raises EmotionServiceError on connection problems or unexpected replies.
    """
    payload = {"raw_document": {"text": text_to_analyse}}
    try:
        response = requests.post(
            URL, json=payload, headers=HEADERS, timeout=TIMEOUT_SECONDS
        )
    except requests.exceptions.RequestException as error:
        raise EmotionServiceError(
            f"Could not reach the Watson service: {error}"
        ) from error

    if response.status_code == 400:
        return _empty_result()
    if response.status_code != 200:
        raise EmotionServiceError(
            f"Unexpected HTTP status code from Watson: {response.status_code}"
        )

    try:
        data = json.loads(response.text)
        scores = data["emotionPredictions"][0]["emotion"]
        result = {emotion: float(scores[emotion]) for emotion in EMOTIONS}
    except (ValueError, KeyError, IndexError, TypeError) as error:
        raise EmotionServiceError(
            "Unexpected response format from the Watson service."
        ) from error

    result["dominant_emotion"] = max(EMOTIONS, key=lambda emotion: result[emotion])
    return result
