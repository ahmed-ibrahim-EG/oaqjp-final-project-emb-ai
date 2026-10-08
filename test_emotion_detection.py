"""Unit tests for the EmotionDetection package (Watson API is mocked)."""
import json
import unittest
from unittest.mock import MagicMock, patch

import requests

from EmotionDetection import emotion_detector, EmotionServiceError

POST_TARGET = "EmotionDetection.emotion_detection.requests.post"


def make_response(dominant, status_code=200):
    """Build a fake requests.Response whose top score is `dominant`."""
    scores = {name: 0.05 for name in ("anger", "disgust", "fear", "joy", "sadness")}
    scores[dominant] = 0.90
    body = {"emotionPredictions": [{"emotion": scores}]}
    response = MagicMock()
    response.status_code = status_code
    response.text = json.dumps(body)
    return response


class TestEmotionDetector(unittest.TestCase):
    """Tests for emotion_detector."""

    def check_dominant(self, sentence, expected):
        """Mock Watson to favour `expected` and verify the dominant emotion."""
        with patch(POST_TARGET, return_value=make_response(expected)):
            result = emotion_detector(sentence)
        self.assertEqual(result["dominant_emotion"], expected)

    def test_joy(self):
        """Joy is detected as dominant."""
        self.check_dominant("I am glad this happened", "joy")

    def test_anger(self):
        """Anger is detected as dominant."""
        self.check_dominant("I am really mad about this", "anger")

    def test_disgust(self):
        """Disgust is detected as dominant."""
        self.check_dominant("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Sadness is detected as dominant."""
        self.check_dominant("I am so sad about this", "sadness")

    def test_fear(self):
        """Fear is detected as dominant."""
        self.check_dominant("I am really afraid that this will happen", "fear")

    def test_http_400_returns_none(self):
        """HTTP 400 returns None for every value."""
        response = MagicMock()
        response.status_code = 400
        response.text = ""
        with patch(POST_TARGET, return_value=response):
            result = emotion_detector("")
        for key in ("anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"):
            self.assertIsNone(result[key])

    def test_connection_error_raises(self):
        """Connection problems raise EmotionServiceError."""
        with patch(POST_TARGET, side_effect=requests.exceptions.ConnectionError()):
            with self.assertRaises(EmotionServiceError):
                emotion_detector("hello")

    def test_unexpected_format_raises(self):
        """A malformed 200 response raises EmotionServiceError."""
        response = MagicMock()
        response.status_code = 200
        response.text = "not json"
        with patch(POST_TARGET, return_value=response):
            with self.assertRaises(EmotionServiceError):
                emotion_detector("hello")


if __name__ == "__main__":
    unittest.main()
