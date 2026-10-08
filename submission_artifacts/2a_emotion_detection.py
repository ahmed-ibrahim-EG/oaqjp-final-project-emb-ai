"""Task 2a - basic emotion detection (returns the raw response text)."""
import requests


def emotion_detector(text_to_analyse):
    """Send text to Watson EmotionPredict and return response.text."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=input_json, headers=headers, timeout=15)
    return response.text
