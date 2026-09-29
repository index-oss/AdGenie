import sys
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.services import recommender, ad_generator, analytics_tracker, user_profiler
from app.models.schemas import TrackEventRequest

def test_product_catalog():
    products = recommender.list_all_products()
    assert len(products) > 0, "Product catalog should not be empty"
    print(f"PASS: Product catalog loaded successfully with {len(products)} products.")

def test_demographic_recommendations():
    # Test Aman (Student, 21, Gaming)
    recs_aman, algo, segment = recommender.recommend(user_id="usr_aman", top_k=3)
    assert len(recs_aman) == 3, "Should return 3 recommendations"
    categories_aman = [p.category for p in recs_aman]
    assert "Electronics & Gaming" in categories_aman, "Aman should receive gaming/electronics recommendations"
    print(f"PASS: Aman recommendations verified -> {[p.name[:25] for p in recs_aman]}")

    # Test Ramesh Ji (Senior, 54, Health)
    recs_ramesh, algo, segment = recommender.recommend(user_id="usr_ramesh", top_k=3)
    categories_ramesh = [p.category for p in recs_ramesh]
    assert "Health & Wellness" in categories_ramesh, "Ramesh Ji should receive health recommendations"
    print(f"PASS: Ramesh Ji recommendations verified -> {[p.name[:25] for p in recs_ramesh]}")

def test_search_query_intent():
    # Real-time search query
    recs, algo, segment = recommender.recommend(search_query="knee joint pain support", top_k=2)
    assert any("knee" in p.name.lower() or "joint" in p.description.lower() for p in recs), "Search for knee should surface knee support product"
    print(f"PASS: Real-time search query matching verified -> {recs[0].name}")

def test_regional_ad_generation():
    top_prod = recommender.products[0]
    
    # Test Hinglish
    ad_hinglish = ad_generator.generate_ad(product_id=top_prod.id, language="hinglish")
    assert ad_hinglish.headline, "Hinglish ad must have a headline"
    assert ad_hinglish.meme_tagline, "Hinglish ad must have a meme tagline"
    print(f"PASS: Hinglish Ad Generated -> '{ad_hinglish.headline}' | Tagline: '{ad_hinglish.meme_tagline}'")

    # Test Hindi
    ad_hi = ad_generator.generate_ad(product_id=top_prod.id, language="hi")
    assert ad_hi.headline, "Hindi ad must have a headline"
    print(f"PASS: Hindi Ad Generated -> '{ad_hi.headline}'")

    # Test Punjabi
    ad_pa = ad_generator.generate_ad(product_id=top_prod.id, language="pa")
    assert ad_pa.headline, "Punjabi ad must have a headline"
    print(f"PASS: Punjabi Ad Generated -> '{ad_pa.headline}'")

def test_analytics_and_revenue():
    initial_summary = analytics_tracker.get_summary()
    initial_revenue = initial_summary.total_revenue_inr

    # Track a simulated personalized click
    event = TrackEventRequest(
        event_type="click",
        product_id="prod_001",
        is_personalized=True,
        ad_language="hinglish",
        cpc=22.50
    )
    analytics_tracker.record_event(event)

    updated_summary = analytics_tracker.get_summary()
    assert updated_summary.total_clicks > initial_summary.total_clicks, "Click count must increment"
    assert updated_summary.total_revenue_inr > initial_revenue, "Revenue must increase after CPC click"
    print(f"PASS: Analytics Engine verified -> Clicks: {updated_summary.total_clicks}, Revenue: ₹{updated_summary.total_revenue_inr}")

if __name__ == "__main__":
    print("========================================")
    print("Running AdGenie Automated Test Suite...")
    print("========================================")
    test_product_catalog()
    test_demographic_recommendations()
    test_search_query_intent()
    test_regional_ad_generation()
    test_analytics_and_revenue()
    print("========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("========================================")
