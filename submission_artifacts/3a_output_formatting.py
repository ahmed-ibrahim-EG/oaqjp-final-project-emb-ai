"""Task 3a - formatted output with dominant emotion (standalone version)."""
import json

import requests


def emotion_detector(text_to_analyse):
    """Return a dict of emotion scores and the dominant emotion."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=input_json, headers=headers, timeout=15)
    data = json.loads(response.text)
    scores = data["emotionPredictions"][0]["emotion"]
    result = {
        "anger": scores["anger"],
        "disgust": scores["disgust"],
        "fear": scores["fear"],
        "joy": scores["joy"],
        "sadness": scores["sadness"],
    }
    result["dominant_emotion"] = max(scores, key=scores.get)
    return result
