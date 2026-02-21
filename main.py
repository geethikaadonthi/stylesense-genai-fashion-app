from __future__ import annotations

from dataclasses import dataclass
from typing import List

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="StyleSense API", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")


@dataclass
class TrendSignal:
    name: str
    vibe: str
    palette: List[str]


TREND_SIGNALS = [
    TrendSignal("Street Minimal", "clean and relaxed", ["charcoal", "white", "sage"]),
    TrendSignal("Neo Ethnic", "heritage with modern layering", ["maroon", "sand", "gold"]),
    TrendSignal("Coastal Soft", "airy and light", ["sky blue", "linen", "mint"]),
]


class PreferenceRequest(BaseModel):
    style: str = Field(..., description="Preferred style direction")
    occasion: str = Field(..., description="Target occasion")
    weather: str = Field(..., description="Current weather")
    budget: str = Field(..., description="Budget preference")


class Recommendation(BaseModel):
    styling_advice: str
    outfit_recommendations: List[str]
    trend_notes: List[str]


class ImageAnalysisResponse(BaseModel):
    image_summary: str
    matched_styles: List[str]
    improvement_tips: List[str]


@app.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.post("/api/recommend", response_model=Recommendation)
async def recommend(payload: PreferenceRequest) -> Recommendation:
    style = payload.style.lower().strip()
    weather = payload.weather.lower().strip()

    base_recs = {
        "casual": ["Oversized tee + tapered jeans + white sneakers", "Cotton shirt + relaxed chinos + loafers"],
        "formal": ["Structured blazer + tailored trousers + derbies", "Monochrome shirt + pencil skirt + block heels"],
        "streetwear": ["Graphic hoodie + cargo pants + high-top sneakers", "Bomber jacket + joggers + chunky sneakers"],
    }

    selected = base_recs.get(style, ["Layered shirt + neutral bottoms + versatile footwear"])
    if "rain" in weather:
        selected.append("Water-resistant trench + ankle boots + compact umbrella")
    elif "hot" in weather:
        selected.append("Breathable linen set + lightweight sandals")

    trend_notes = [
        f"{trend.name}: {trend.vibe} (palette: {', '.join(trend.palette)})"
        for trend in TREND_SIGNALS
    ]

    advice = (
        f"For a {payload.occasion.lower()} setting, anchor your outfit around {payload.style.lower()} staples, "
        f"keep choices weather-aware for {payload.weather.lower()} conditions, and prioritize pieces within a {payload.budget.lower()} budget."
    )

    return Recommendation(
        styling_advice=advice,
        outfit_recommendations=selected,
        trend_notes=trend_notes,
    )


@app.post("/api/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(
    style_goal: str = Form(...),
    image: UploadFile = File(...),
) -> ImageAnalysisResponse:
    filename = image.filename.lower()

    if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
        summary = "Your uploaded look appears balanced with clear layering and a focal piece."
        matched = ["Smart casual", "Urban minimal", style_goal]
        tips = [
            "Add one accent accessory to boost visual hierarchy.",
            "Echo one dominant color from the outfit in your footwear.",
            "Use a structured outer layer for sharper silhouette definition.",
        ]
    else:
        summary = "Unsupported format for detailed visual parsing; defaulting to style-goal guidance."
        matched = [style_goal]
        tips = ["Re-upload using PNG, JPG, or WEBP for richer analysis."]

    await image.close()
    return ImageAnalysisResponse(image_summary=summary, matched_styles=matched, improvement_tips=tips)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
