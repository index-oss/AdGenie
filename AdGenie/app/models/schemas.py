from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UserProfile(BaseModel):
    user_id: Optional[str] = "guest"
    name: Optional[str] = "Guest User"
    age: Optional[int] = 25
    age_group: Optional[str] = "18-25"
    city: Optional[str] = "Delhi"
    preferred_language: Optional[str] = "hinglish"
    interests: List[str] = Field(default_factory=list)
    search_history: List[str] = Field(default_factory=list)
    recent_clicks: List[str] = Field(default_factory=list)

class Product(BaseModel):
    id: str
    name: str
    category: str
    sub_category: Optional[str] = ""
    price: float
    original_price: float
    rating: float
    reviews_count: int
    age_groups: List[str]
    tags: List[str]
    description: str
    image_url: str
    sponsor: Optional[str] = "AdGenie Merchant"

class ScoredProduct(Product):
    score: float = Field(default=0.0, description="Recommendation relevance score (0.0 to 1.0)")
    match_reason: str = Field(default="Trending Product", description="Human-interpretable explanation")

class RecommendRequest(BaseModel):
    user_id: Optional[str] = None
    user_profile: Optional[UserProfile] = None
    search_query: Optional[str] = None
    current_product_id: Optional[str] = None
    top_k: int = 4

class RecommendResponse(BaseModel):
    recommendations: List[ScoredProduct]
    algorithm_used: str
    user_segment: str
    total_found: int

class AdGenerationRequest(BaseModel):
    product_id: str
    user_id: Optional[str] = None
    user_profile: Optional[UserProfile] = None
    language: Optional[str] = "hinglish"
    tone: Optional[str] = "witty"  # witty, urgency, emotional, value

class AdBanner(BaseModel):
    product_id: str
    product_name: str
    headline: str
    subheadline: str
    hook_tag: str
    cta_text: str
    language: str
    language_display: str
    discount_badge: str
    image_url: str
    price: float
    original_price: float
    sponsor: str
    meme_tagline: str
    estimated_ctr: float

class TrackEventRequest(BaseModel):
    event_type: str = Field(description="'impression', 'click', or 'purchase'")
    product_id: str
    is_personalized: bool = True
    ad_language: Optional[str] = "hinglish"
    user_id: Optional[str] = "guest"
    cpc: Optional[float] = 22.50

class AnalyticsSummary(BaseModel):
    total_impressions: int
    total_clicks: int
    total_purchases: int
    overall_ctr: float
    static_ctr: float
    personalized_ctr: float
    ctr_lift_multiplier: float
    total_revenue_inr: float
    revenue_breakdown: Dict[str, float]
    language_clicks: Dict[str, int]
    top_performing_categories: Dict[str, int]
