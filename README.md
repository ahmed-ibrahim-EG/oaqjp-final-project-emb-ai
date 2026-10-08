# Final Project

Emotion Detection web application built for the IBM Skills Network final project.
The app sends text to the IBM Watson NLP EmotionPredict service and shows the scores
for anger, disgust, fear, joy and sadness, together with the dominant emotion.

Repository name: `oaqjp-final-project-emb-ai`

## Technologies

- Python 3.9+
- Flask
- Requests
- IBM Watson NLP EmotionPredict API
- unittest and unittest.mock
- Pylint

## Project structure

```text
oaqjp-final-project-emb-ai/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── templates/index.html
├── static/mywebscript.js
├── server.py
├── test_emotion_detection.py
├── requirements.txt
├── README.md
├── .gitignore
└── submission_artifacts/
```

## Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the application

```bash
python server.py
```

Open http://localhost:5000 in your browser. The Watson service is only reachable
from the IBM Skills Network lab environment.

## Run the unit tests

The tests mock the Watson API, so no internet connection is needed.

```bash
python -m unittest test_emotion_detection.py -v
```

## Run Pylint

```bash
pylint server.py
```

## Error handling

- Blank or whitespace-only input returns "Invalid text! Please try again!" (HTTP 400).
- Watson HTTP 400 returns `None` for every emotion value.
- Connection failures or unexpected responses show a friendly error (HTTP 503)
  without crashing the app.
