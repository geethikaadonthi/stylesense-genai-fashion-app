# StyleSense

StyleSense is a **Generative AI–Powered Fashion Recommendation System** built with FastAPI, HTML, CSS, and JavaScript.

## Features
- Personalized styling advice based on style, occasion, weather, and budget.
- Outfit recommendation generation with trend-aware notes.
- Image upload endpoint for look analysis and improvement tips.
- Interactive web UI for both preference-based and image-based workflows.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000`.

## API overview
- `POST /api/recommend` – preference-based recommendation
- `POST /api/analyze-image` – image-based analysis
- `GET /api/health` – health check
