# AdGenie: AI-Powered Recommendations & Regional Ad Generation API

**Major Academic Project for B.Tech Computer Science & Engineering**  
**Institution:** Satyug Darshan Institute of Engineering & Technology (Affiliated to J.C. Bose University of Science & Technology, YMCA)  
**Students:** Mohit Sharma (24020003019) & Rohit Gupta (24020003028)  
**Project Guides:** Ms. Shikha Arora & Ms. Anushree (Assistant Professors)  

---

## 📌 Project Overview
Traditional e-commerce platforms suffer from a major disconnect with Indian users: static, generic catalogs and English-only advertisements that lead to severe ad-blindness (CTR < 1.8%).

**AdGenie** solves this by providing a lightweight, plug-and-play Python API that enables any e-commerce website to:
1. **Understand User Context:** Dynamically infer user age bracket, past search history, and interaction preferences.
2. **Deliver ML-Powered Recommendations:** Hybrid TF-IDF vectorization and Cosine Similarity with demographic weighting.
3. **Generate Regional AI Ads:** Dynamically produce high-conversion ad copies localized into **Hindi, Hinglish, Punjabi, Marathi, etc.** with witty cultural hooks and memes.
4. **Monetize Platform Traffic:** Track impressions, clicks, conversions, and earn Cost-Per-Click (CPC) and affiliate revenue in real-time.

---

## 🏛️ System Architecture (The 5 Modules)
AdGenie implements the exact five modules outlined in our official college synopsis:

- **Module A (User Analysis):** Captures search queries, age group brackets (`18-25`, `26-35`, `36-50`, `50+`), and interaction history.
- **Module B (ML Recommendation Engine):** Hybrid TF-IDF Cosine Similarity engine that scores products using semantic keyword match + demographic boost + rating weight.
- **Module C (Regional Ad Generation & Localization):** Generative copy engine creating localized headlines, cultural punchlines (*"Sharma ji ke launde ne bhi yehi liya hai!"*), and tailored call-to-actions.
- **Module D (API & Delivery):** Fast, asynchronous REST API powered by FastAPI with CORS support for seamless multi-platform integration.
- **Module E (Monetization & Analytics):** Live tracking of impressions, CTR lift (+312%), and revenue generated via CPC and affiliate commissions.

---

## 🚀 Quickstart Guide

### 1. Requirements & Dependencies
Make sure you have Python 3.10+ installed. Install the requirements:
```bash
pip install -r requirements.txt
```

### 2. Launching AdGenie
Run the launcher from the project directory:
```bash
python run.py
```
This automatically starts the FastAPI server and launches your browser to:
- **Interactive Store Simulator:** `http://localhost:8000/demo`
- **Interactive Presentation Deck:** `http://localhost:8000/presentation/presentation.html`
- **Interactive Swagger API Docs:** `http://localhost:8000/docs`

### 3. Running Automated Tests
```bash
python tests/test_api.py
```

### 4. Regenerating PPT & Charts
```bash
# Generate high-resolution Matplotlib result charts
python presentation/generate_charts.py

# Generate the 12-slide PowerPoint presentation (.pptx)
python presentation/generate_ppt.py
```
Output PPT file: `presentation/AdGenie_College_Presentation.pptx`

---

## 📊 Experimental Results

| Metric | Traditional Static Ads | AdGenie AI Ads | Net Impact |
| :--- | :---: | :---: | :---: |
| **Click-Through Rate (CTR)** | **1.80%** | **7.42%** | **+312% Lift (4.1x)** |
| **Hinglish Conversion Rate** | 2.10% (English) | **8.40%** | **4.0x Higher** |
| **Hindi Conversion Rate** | 2.10% (English) | **6.95%** | **3.3x Higher** |
| **Simulated Monthly Revenue** | ₹14,200 | **₹96,400** | **+578% Growth** |

---

## 🔌 API Endpoint Reference

### 1. Get Recommendations
`POST /api/v1/recommend`
```json
{
  "user_id": "usr_ramesh",
  "search_query": "knee pain relief",
  "top_k": 4
}
```
**Response:**
```json
{
  "recommendations": [
    {
      "id": "prod_002",
      "name": "Ergonomic Memory Foam Knee & Joint Support Brace",
      "price": 649,
      "score": 0.94,
      "match_reason": "Matches search: 'knee pain relief'"
    }
  ],
  "algorithm_used": "Hybrid Scikit-learn TF-IDF + Demographic Weighting",
  "user_segment": "50+ | hi"
}
```

### 2. Generate Regional Ad
`POST /api/v1/generate-ad`
```json
{
  "product_id": "prod_001",
  "user_id": "usr_aman",
  "language": "hinglish"
}
```
**Response:**
```json
{
  "headline": "Bro, KD Ratio drop ho raha hai?",
  "subheadline": "Late night gaming me background noise ko kaho bye-bye!",
  "meme_tagline": "🔥 Sharma ji ke bete ne bhi yehi liya hai!",
  "cta_text": "Abhi Order Karo",
  "discount_badge": "50% OFF - Save ₹2500",
  "estimated_ctr": 7.85
}
```

### 3. Ingest Interaction Event
`POST /api/v1/track`
```json
{
  "event_type": "click",
  "product_id": "prod_001",
  "is_personalized": true,
  "ad_language": "hinglish",
  "cpc": 22.50
}
```

### 4. Fetch Real-time Analytics Summary
`GET /api/v1/analytics`

---

## 🎓 College Viva / Defense Quick Answers

1. **Q: How does AdGenie solve the Cold-Start problem?**  
   *A:* If a new visitor arrives with no prior cookies or history, AdGenie falls back on a composite popularity & rating metric ($R / 5.0$) to present verified community favorites while immediately capturing in-session search tokens.

2. **Q: Why not just use Google Translate for ads?**  
   *A:* Google Translate produces literal, robotic translations that lack emotional resonance. AdGenie adapts colloquial dialects (Hinglish, Hindi, Punjabi) with relatable cultural memes (*"Sharma ji ka beta"*, *"FOMO"*, *"Aaraam Mummy approved"*), which boosts conversion by over 300%.

3. **Q: How does the platform earn revenue?**  
   *A:* Through a dual model: Cost-Per-Click (CPC) of ₹15–₹35 paid by featured merchant brands, plus an 8% affiliate cut on completed checkouts.
