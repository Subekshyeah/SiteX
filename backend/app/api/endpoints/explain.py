from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os
import requests
import time
import json
import hashlib

_CACHED_MODEL: str | None = None
_CACHE: dict[str, tuple[float, str]] = {}
_CACHE_TTL_SECONDS = 6 * 60 * 60

def _make_cache_key(request: "ExplainRequest") -> str:
    key_payload = {
        "radius_km": request.radius_km,
        "decay_scale_km": request.decay_scale_km,
        "points": [
            {
                "lat": round(p.lat, 6),
                "lng": round(p.lng, 6),
                "key": p.key,
            }
            for p in request.points
        ],
    }
    raw = json.dumps(key_payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def _get_cached_explanation(cache_key: str) -> str | None:
    item = _CACHE.get(cache_key)
    if not item:
        return None
    ts, text = item
    if (time.time() - ts) > _CACHE_TTL_SECONDS:
        _CACHE.pop(cache_key, None)
        return None
    return text

def _set_cached_explanation(cache_key: str, text: str) -> None:
    _CACHE[cache_key] = (time.time(), text)

def _resolve_gemini_model(api_key: str) -> str:
    global _CACHED_MODEL
    if _CACHED_MODEL:
        return _CACHED_MODEL

    env_model = os.getenv("GEMINI_MODEL")
    if env_model:
        _CACHED_MODEL = env_model
        return env_model

    # Auto-detect a model that supports generateContent
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    resp = requests.get(list_url, timeout=15)
    if resp.ok:
        data = resp.json()
        models = data.get("models", [])
        # Prefer flash models if available
        preferred = [
            "models/gemini-1.5-flash-002",
            "models/gemini-1.5-flash-001",
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro-002",
            "models/gemini-1.5-pro-001",
            "models/gemini-1.5-pro",
            "models/gemini-pro",
        ]
        available = {m.get("name") for m in models if m.get("name")}
        for name in preferred:
            if name in available:
                _CACHED_MODEL = name
                return name
        for m in models:
            if "generateContent" in (m.get("supportedGenerationMethods") or []):
                _CACHED_MODEL = m.get("name")
                return _CACHED_MODEL

    # Fallback
    _CACHED_MODEL = "models/gemini-pro"
    return _CACHED_MODEL

router = APIRouter()

class ExplainPoi(BaseModel):
    name: str
    distance_km: float
    weight: float
    decayed_weight: float
    avg_weight_value: float
    subcategory: str | None = None

class ExplainCategory(BaseModel):
    cat: str
    score: float
    top_pois: List[ExplainPoi] = Field(default_factory=list)

class ExplainPoint(BaseModel):
    key: str
    lat: float
    lng: float
    total_score: float
    per_category: List[ExplainCategory] = Field(default_factory=list)

class ExplainRequest(BaseModel):
    preferred_point_key: str | None = None
    radius_km: float
    decay_scale_km: float
    points: List[ExplainPoint] = Field(default_factory=list)

class ExplainResponse(BaseModel):
    explanation: str

@router.post("/explain/", response_model=ExplainResponse)
def explain_points(request: ExplainRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not set")

    cache_key = _make_cache_key(request)
    cached = _get_cached_explanation(cache_key)
    if cached:
        return ExplainResponse(explanation=cached)

    prompt = (
        "You are an analyst. Explain each candidate point in natural language using the top POI contributors "
        "per category and how they contribute to the final score. Use concise bullet points per point. "
        "Include which point is preferred and why. Write a detailed report with at least 700 words. "
        "For each point and each category, list the top 20 POIs with full details (name, subcategory, distance_km, "
        "weight, decayed_weight, avg_weight_value). Conclude with a final comparative analysis and recommendation. "
        f"Radius: {request.radius_km} km. Decay scale: {request.decay_scale_km} km. "
        "Use the provided data only.\n\n"
        "DATA (JSON):\n"
        f"{request.model_dump_json(indent=2)}"
    )

    model_name = _resolve_gemini_model(api_key)
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2000
        }
    }

    try:
        resp = requests.post(url, json=payload, timeout=25)
        if not resp.ok:
            raise HTTPException(status_code=502, detail=f"Gemini API error: {resp.status_code} {resp.text}")
        data = resp.json()
        text = ""
        candidates = data.get("candidates") or []
        if candidates:
            content = candidates[0].get("content") or {}
            parts = content.get("parts") or []
            if parts:
                text = parts[0].get("text") or ""
        if not text:
            raise HTTPException(status_code=502, detail="Gemini API returned empty response")
        text = text.strip()
        _set_cached_explanation(cache_key, text)
        return ExplainResponse(explanation=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")
