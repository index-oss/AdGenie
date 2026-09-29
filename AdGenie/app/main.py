from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pathlib import Path
from typing import List, Optional

from app.config import PROJECT_TITLE, PROJECT_DESCRIPTION, VERSION, BASE_DIR
from app.models.schemas import (
    Product,
    RecommendRequest,
    RecommendResponse,
    AdGenerationRequest,
    AdBanner,
    TrackEventRequest,
    AnalyticsSummary,
    UserProfile
)
from app.services import recommender, ad_generator, analytics_tracker, user_profiler

app = FastAPI(
    title=PROJECT_TITLE,
    description=PROJECT_DESCRIPTION,
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for universal website integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories for Demo Store and Presentation
DEMO_DIR = BASE_DIR / "demo_store"
PRESENTATION_DIR = BASE_DIR / "presentation"

if DEMO_DIR.exists():
    app.mount("/demo", StaticFiles(directory=str(DEMO_DIR), html=True), name="demo")

if PRESENTATION_DIR.exists():
    app.mount("/presentation", StaticFiles(directory=str(PRESENTATION_DIR), html=True), name="presentation")

@app.get("/")
def root():
    return {
        "project": "AdGenie API",
        "description": "AI-Powered Recommendations & Regional Ad Generation API",
        "team": ["Mohit Sharma", "Rohit Gupta"],
        "institution": "Satyug Darshan Institute of Engineering & Technology",
        "documentation": "/docs",
        "interactive_demo_store": "/demo",
        "interactive_presentation": "/presentation/presentation.html",
        "endpoints": {
            "products": "/api/v1/products",
            "users": "/api/v1/users",
            "recommend": "/api/v1/recommend",
            "generate_ad": "/api/v1/generate-ad",
            "track": "/api/v1/track",
            "analytics": "/api/v1/analytics"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "version": VERSION, "products_count": len(recommender.products)}

@app.get("/api/v1/products", response_model=List[Product])
def get_products():
    return recommender.list_all_products()

@app.get("/api/v1/users", response_model=List[UserProfile])
def get_sample_users():
    return user_profiler.list_sample_users()

@app.post("/api/v1/recommend", response_model=RecommendResponse)
def get_recommendations(req: RecommendRequest):
    recs, algo, segment = recommender.recommend(
        user_id=req.user_id,
        user_profile=req.user_profile,
        search_query=req.search_query,
        current_product_id=req.current_product_id,
        top_k=req.top_k
    )
    return RecommendResponse(
        recommendations=recs,
        algorithm_used=algo,
        user_segment=segment,
        total_found=len(recs)
    )

@app.post("/api/v1/generate-ad", response_model=AdBanner)
def generate_regional_ad(req: AdGenerationRequest):
    banner = ad_generator.generate_ad(
        product_id=req.product_id,
        user_id=req.user_id,
        user_profile=req.user_profile,
        language=req.language or "hinglish",
        tone=req.tone or "witty"
    )
    return banner

@app.post("/api/v1/track")
def track_event(event: TrackEventRequest):
    analytics_tracker.record_event(event)
    return {
        "status": "success",
        "recorded_event": event.event_type,
        "is_personalized": event.is_personalized
    }

@app.get("/api/v1/analytics", response_model=AnalyticsSummary)
def get_analytics():
    return analytics_tracker.get_summary()
