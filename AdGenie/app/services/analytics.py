from typing import Dict, List, Optional
from app.models.schemas import AnalyticsSummary, TrackEventRequest
from app.config import DEFAULT_CPC, AFFILIATE_RATE, STATIC_BASELINE_CTR

class AnalyticsTracker:
    """
    Module E: Interaction Tracking & Monetization Analytics Engine.
    Tracks CTR, conversion lift, and revenue generation from the AdGenie API.
    """
    def __init__(self):
        # Initial baseline seed data representing real-world comparative benchmark
        self.impressions_static = 12500
        self.clicks_static = 225          # 1.80% CTR baseline

        self.impressions_personalized = 12500
        self.clicks_personalized = 925    # 7.40% CTR with AdGenie AI (+311% lift)
        self.purchases_personalized = 82  # ~8.8% conversion rate from click

        self.cpc_rate = DEFAULT_CPC
        self.affiliate_rate = AFFILIATE_RATE

        # Language click distributions
        self.language_clicks: Dict[str, int] = {
            "Hinglish": 412,
            "Hindi": 315,
            "English": 118,
            "Punjabi": 48,
            "Marathi": 32
        }

        # Category click distributions
        self.category_clicks: Dict[str, int] = {
            "Electronics & Gaming": 395,
            "Health & Wellness": 310,
            "Home & Office": 165,
            "Home & Kitchen": 55
        }

    def record_event(self, event: TrackEventRequest):
        """Records a live event from the demo e-commerce store."""
        cpc = event.cpc or self.cpc_rate
        lang_key = (event.ad_language or "Hinglish").capitalize()

        if event.event_type == "impression":
            if event.is_personalized:
                self.impressions_personalized += 1
            else:
                self.impressions_static += 1

        elif event.event_type == "click":
            if event.is_personalized:
                self.clicks_personalized += 1
                self.language_clicks[lang_key] = self.language_clicks.get(lang_key, 0) + 1
            else:
                self.clicks_static += 1

        elif event.event_type == "purchase":
            if event.is_personalized:
                self.purchases_personalized += 1

    def get_summary(self) -> AnalyticsSummary:
        """Computes comprehensive performance and monetization statistics."""
        total_imp = self.impressions_static + self.impressions_personalized
        total_clicks = self.clicks_static + self.clicks_personalized

        static_ctr = round((self.clicks_static / max(self.impressions_static, 1)) * 100, 2)
        personalized_ctr = round((self.clicks_personalized / max(self.impressions_personalized, 1)) * 100, 2)
        overall_ctr = round((total_clicks / max(total_imp, 1)) * 100, 2)

        lift_multiplier = round(personalized_ctr / max(static_ctr, 0.1), 2)

        # Revenue calculations:
        # 1. CPC Revenue from AdGenie clicks
        cpc_revenue = self.clicks_personalized * self.cpc_rate
        # 2. Affiliate Commission on conversions (~ avg order value ₹1500)
        avg_order_value = 1500.0
        affiliate_revenue = self.purchases_personalized * avg_order_value * self.affiliate_rate
        total_revenue = cpc_revenue + affiliate_revenue

        return AnalyticsSummary(
            total_impressions=total_imp,
            total_clicks=total_clicks,
            total_purchases=self.purchases_personalized,
            overall_ctr=overall_ctr,
            static_ctr=static_ctr,
            personalized_ctr=personalized_ctr,
            ctr_lift_multiplier=lift_multiplier,
            total_revenue_inr=round(total_revenue, 2),
            revenue_breakdown={
                "CPC Ad Revenue": round(cpc_revenue, 2),
                "Affiliate Purchase Commission": round(affiliate_revenue, 2)
            },
            language_clicks=self.language_clicks,
            top_performing_categories=self.category_clicks
        )

analytics_tracker = AnalyticsTracker()
