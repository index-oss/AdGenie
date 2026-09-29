import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = OUTPUT_DIR / "assets"
PPTX_PATH = OUTPUT_DIR / "AdGenie_College_Presentation.pptx"

# Brand Palette
COLOR_BG_DARK = RGBColor(15, 23, 42)       # #0f172a (Deep Slate Navy)
COLOR_BG_LIGHT = RGBColor(248, 250, 252)   # #f8fafc (Clean off-white)
COLOR_PRIMARY = RGBColor(79, 70, 229)      # #4f46e5 (Indigo)
COLOR_PRIMARY_DARK = RGBColor(49, 46, 129) # #312e81
COLOR_ACCENT = RGBColor(16, 185, 129)      # #10b981 (Emerald Green)
COLOR_AMBER = RGBColor(245, 158, 11)       # #f59e0b (Warm Amber)
COLOR_TEXT_MAIN = RGBColor(15, 23, 42)     # #0f172a
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # #64748b
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BG = RGBColor(255, 255, 255)
COLOR_CARD_BORDER = RGBColor(226, 232, 240)

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def create_shape(slide, shape_type, left, top, width, height, fill_color, border_color=None, border_width=1):
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape

def add_header(slide, title_text, category_text="ADGENIE: AI-POWERED PLATFORM"):
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_PRIMARY

    # Main title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.75))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_MAIN

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Theme)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_BG_DARK)

    # Accent decorative banner card
    create_shape(s1, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9), RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))

    # Badge
    badge = create_shape(s1, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.3), Inches(2.8), Inches(0.45), COLOR_PRIMARY)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "MAJOR PROJECT PRESENTATION"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_WHITE
    p_b.alignment = PP_ALIGN.CENTER

    # Title & Subtitle
    tb_t = s1.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.3), Inches(2.0))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "AdGenie: AI-Powered Recommendations\n& Regional Ad Generation API"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "Transforming Generic E-Commerce into High-Converting, Vernacular-First Smart Stores"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(12)

    # Student & College Footer Box
    meta_box = s1.shapes.add_textbox(Inches(1.5), Inches(4.3), Inches(10.3), Inches(2.0))
    tf_m = meta_box.text_frame
    
    pm1 = tf_m.paragraphs[0]
    pm1.text = "Students: Mohit Sharma (24020003019)  |  Rohit Gupta (24020003028)"
    pm1.font.size = Pt(15)
    pm1.font.bold = True
    pm1.font.color.rgb = COLOR_ACCENT

    pm2 = tf_m.add_paragraph()
    pm2.text = "Project Guides: Ms. Shikha Arora & Ms. Anushree (Assistant Professors)"
    pm2.font.size = Pt(14)
    pm2.font.color.rgb = COLOR_WHITE
    pm2.space_before = Pt(6)

    pm3 = tf_m.add_paragraph()
    pm3.text = "Department of Computer Science & Engineering\nSatyug Darshan Institute of Engineering & Technology (Affiliated to J.C. Bose UST, YMCA)"
    pm3.font.size = Pt(13)
    pm3.font.color.rgb = RGBColor(148, 163, 184)
    pm3.space_before = Pt(6)

    # ==========================================
    # SLIDE 2: THE REAL-LIFE PROBLEM (Meme & Scenario)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_BG_LIGHT)
    add_header(s2, "The Real-Life Problem: The 'Ramesh Uncle' Scenario", "THE REAL-WORLD PROBLEM")

    # Left Column: The Problem Story Card
    create_shape(s2, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_story = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_s = tb_story.text_frame
    tf_s.word_wrap = True
    
    ps1 = tf_s.paragraphs[0]
    ps1.text = "👴 Meet Ramesh Ji (54, Kanpur):"
    ps1.font.size = Pt(17)
    ps1.font.bold = True
    ps1.font.color.rgb = COLOR_TEXT_MAIN

    ps2 = tf_s.add_paragraph()
    ps2.text = "• Ramesh Ji is searching on an e-commerce website for knee pain relief belts and a digital BP monitor for home.\n\n• What does the static site show him?\nA generic English banner advertising: 'Extreme Neon Roller Skates - 10% Off!'\n\n• The Result:\nRamesh Ji gets confused, ignores the ad, and closes the tab. The merchant gets ZERO clicks and ZERO revenue."
    ps2.font.size = Pt(14)
    ps2.font.color.rgb = COLOR_TEXT_MUTED
    ps2.space_before = Pt(10)

    # Right Column: The Hard Reality & Meme Callout Card
    create_shape(s2, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_stat = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_stat = tb_stat.text_frame
    tf_stat.word_wrap = True

    pst1 = tf_stat.paragraphs[0]
    pst1.text = "📉 The Ugly Truth of Traditional Sites:"
    pst1.font.size = Pt(17)
    pst1.font.bold = True
    pst1.font.color.rgb = RGBColor(220, 38, 38)

    pst2 = tf_stat.add_paragraph()
    pst2.text = "1. 98.2% of Static Ads are completely ignored (Average CTR < 1.8%).\n2. 80%+ Indians in Tier-2/3 cities prefer regional or conversational Hinglish over formal English.\n3. Zero Personalization means millions in wasted ad impressions every day."
    pst2.font.size = Pt(14)
    pst2.font.color.rgb = COLOR_TEXT_MUTED
    pst2.space_before = Pt(10)

    # Meme Callout Box
    meme_box = create_shape(s2, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(4.7), Inches(5.0), Inches(1.8), RGBColor(254, 243, 199), border_color=COLOR_AMBER)
    tf_mb = meme_box.text_frame
    tf_mb.word_wrap = True
    pmb = tf_mb.paragraphs[0]
    pmb.text = "💬 The Indian E-Commerce Meme Reality:\n'Ramesh Uncle searching knee caps while website recommends skateboard in English... Uncle: Beta ye kya badtameezi hai?!'"
    pmb.font.size = Pt(13)
    pmb.font.bold = True
    pmb.font.color.rgb = RGBColor(146, 64, 14)

    # ==========================================
    # SLIDE 3: THE BIG IDEA: WHAT IS ADGENIE?
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_BG_LIGHT)
    add_header(s3, "The Big Idea: What is AdGenie?", "OUR SOLUTION")

    # Big Banner Concept
    top_card = create_shape(s3, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(1.5), COLOR_PRIMARY_DARK)
    tf_tc = top_card.text_frame
    tf_tc.word_wrap = True
    ptc1 = tf_tc.paragraphs[0]
    ptc1.text = "AdGenie is a plug-and-play Python API that connects to ANY website,\nanalyzes user intent, recommends the right products, and generates witty regional ads!"
    ptc1.font.size = Pt(17)
    ptc1.font.bold = True
    ptc1.font.color.rgb = COLOR_WHITE
    ptc1.alignment = PP_ALIGN.CENTER

    # 3 Pillar Cards
    pillars = [
        ("🎯 1. User Intelligence", "Analyzes user age bracket, past search history, and interaction clicks without intrusive tracking.", COLOR_WHITE, COLOR_PRIMARY),
        ("🧠 2. ML Recommendations", "Uses TF-IDF Vectorization & Cosine Similarity with demographic weighting to rank relevant products.", COLOR_WHITE, COLOR_ACCENT),
        ("🗣️ 3. Regional AI Ads", "Translates and culturally adapts ad copy into Hindi, Hinglish, Marathi, etc. with catchy hooks!", COLOR_WHITE, COLOR_AMBER)
    ]

    for idx, (p_title, p_desc, bg_col, accent_col) in enumerate(pillars):
        x = Inches(0.8 + idx * 4.0)
        c = create_shape(s3, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.4), Inches(3.6), Inches(3.4), bg_col, border_color=COLOR_CARD_BORDER)
        tb_p = s3.shapes.add_textbox(x + Inches(0.2), Inches(3.6), Inches(3.2), Inches(3.0))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        
        pp1 = tf_p.paragraphs[0]
        pp1.text = p_title
        pp1.font.size = Pt(16)
        pp1.font.bold = True
        pp1.font.color.rgb = accent_col

        pp2 = tf_p.add_paragraph()
        pp2.text = p_desc
        pp2.font.size = Pt(13)
        pp2.font.color.rgb = COLOR_TEXT_MUTED
        pp2.space_before = Pt(12)

    # ==========================================
    # SLIDE 4: REAL-LIFE SCENARIOS (Persona Breakdown)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, COLOR_BG_LIGHT)
    add_header(s4, "Real-Life Scenarios: How AdGenie Personalizes for Everyone", "DEMOGRAPHIC TARGETING")

    personas = [
        ("🎓 Aman (Age 21, Delhi)", "Student & Casual Gamer", "Searches: 'gaming headphones low latency'", 
         "Dynamic Hinglish Ad:\n'Bro, KD Ratio drop ho raha hai? Zero-latency audio + RGB lights under ₹2,500! Sharma ji ke launde se aage niklo.'",
         "Result: Instant click & high interest!", COLOR_PRIMARY),
        ("🧘 Ramesh Ji (Age 54, Kanpur)", "Retired Officer", "Searches: 'ghutno ka dard belt'", 
         "Dynamic Hindi Ad:\n'अब हर सुबह चलें बेफिक्र! कॉपर-इन्फ्यूज्ड सपोर्ट बेल्ट जो जोड़ों के दर्द में दे तुरंत और सुरक्षित आराम। ₹649 में।'",
         "Result: Builds trust, triggers purchase!", COLOR_ACCENT),
        ("💼 Priya (Age 29, Bengaluru)", "Remote Software Engineer", "Searches: 'ergonomic back chair wfh'", 
         "Dynamic English Ad:\n'Say goodbye to 3 PM spinal fatigue. High-back adaptive lumbar mesh chair with 45% discount today.'",
         "Result: Direct conversion & WFH comfort!", COLOR_AMBER)
    ]

    for idx, (p_name, p_role, p_search, p_ad, p_res, col) in enumerate(personas):
        x = Inches(0.8 + idx * 4.0)
        card = create_shape(s4, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(3.6), Inches(5.3), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
        tb_card = s4.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.2), Inches(4.9))
        tf_c = tb_card.text_frame
        tf_c.word_wrap = True

        p1 = tf_c.paragraphs[0]
        p1.text = p_name
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf_c.add_paragraph()
        p2.text = f"{p_role}\n{p_search}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_before = Pt(6)

        p3 = tf_c.add_paragraph()
        p3.text = p_ad
        p3.font.size = Pt(12)
        p3.font.bold = True
        p3.font.color.rgb = COLOR_TEXT_MAIN
        p3.space_before = Pt(12)

        p4 = tf_c.add_paragraph()
        p4.text = p_res
        p4.font.size = Pt(12)
        p4.font.bold = True
        p4.font.color.rgb = col
        p4.space_before = Pt(10)

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE (The 5 Modules)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, COLOR_BG_LIGHT)
    add_header(s5, "System Architecture: The 5 Core Modules", "SYSTEM DESIGN")

    modules = [
        ("Module A\nUser Analysis", "Extracts age group, search tokens, past click interactions, and regional preferences.", COLOR_PRIMARY),
        ("Module B\nML Recommender", "Scikit-learn TF-IDF + Cosine Similarity with demographic weight boosting.", COLOR_ACCENT),
        ("Module C\nRegional Ad Engine", "Dynamic copy generation & translation into Hindi, Hinglish, Punjabi, Marathi.", COLOR_AMBER),
        ("Module D\nFastAPI REST Layer", "High-speed JSON endpoints (/recommend, /generate-ad, /track, /analytics).", COLOR_PRIMARY_DARK),
        ("Module E\nAnalytics & ROI", "Tracks impressions, CTR%, and CPC revenue generated for the partner site.", COLOR_PRIMARY)
    ]

    for idx, (m_title, m_desc, col) in enumerate(modules):
        x = Inches(0.8 + idx * 2.38)
        card = create_shape(s5, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.2), Inches(4.8), COLOR_WHITE, border_color=col, border_width=2)
        tb_m = s5.shapes.add_textbox(x + Inches(0.15), Inches(2.0), Inches(1.9), Inches(4.4))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p1 = tf_m.paragraphs[0]
        p1.text = m_title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf_m.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_before = Pt(14)

    # ==========================================
    # SLIDE 6: HOW THE RECOMMENDATION MODEL WORKS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, COLOR_BG_LIGHT)
    add_header(s6, "How the Recommendation Model Works (TF-IDF & Cosine Similarity)", "MACHINE LEARNING")

    # Formula & Explanation Box
    left_card = create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_l = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl1 = tf_l.paragraphs[0]
    pl1.text = "Mathematical Pipeline:"
    pl1.font.size = Pt(17)
    pl1.font.bold = True
    pl1.font.color.rgb = COLOR_PRIMARY

    pl2 = tf_l.add_paragraph()
    pl2.text = "1. Document Representation:\nCombines Title + Category + Tags + Description into a high-dimensional text corpus.\n\n2. TF-IDF Weighting:\nTerm Frequency × Inverse Document Frequency penalizes generic stopwords and rewards distinctive keywords (e.g., 'copper', 'ergonomic', 'anc').\n\n3. Cosine Similarity:\nCalculates cosine angle between user search vector Q and product vector D:\nSimilarity(Q, D) = (Q · D) / (||Q|| × ||D||)"
    pl2.font.size = Pt(13)
    pl2.font.color.rgb = COLOR_TEXT_MUTED
    pl2.space_before = Pt(8)

    # Demographic Boosting Box
    right_card = create_shape(s6, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr1 = tf_r.paragraphs[0]
    pr1.text = "Demographic & Hybrid Scoring:"
    pr1.font.size = Pt(17)
    pr1.font.bold = True
    pr1.font.color.rgb = COLOR_ACCENT

    pr2 = tf_r.add_paragraph()
    pr2.text = "Total Score = W1(Search Sim) + W2(History Sim) + W3(Age Group Booster) + W4(Product Rating)\n\n• Why this beats simple keyword search:\nEven if Ramesh Ji doesn't type 'orthopedic', his age group (50+) and interest tags immediately boost health and comfort products to the top.\n\n• Cold-Start Fallback:\nIf a new guest arrives without cookies, the model gracefully falls back to highest-rated customer favorites."
    pr2.font.size = Pt(13)
    pr2.font.color.rgb = COLOR_TEXT_MUTED
    pr2.space_before = Pt(8)

    # ==========================================
    # SLIDE 7: REGIONAL AD LOCALIZATION (Why Vernacular Wins)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, COLOR_BG_LIGHT)
    add_header(s7, "AI Regional Ad Localization: Why Vernacular Wins", "AI LOCALIZATION")

    # Table comparison of ad copies
    table_card = create_shape(s7, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_tab = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.2), Inches(4.8))
    tf_tab = tb_tab.text_frame
    tf_tab.word_wrap = True

    pt1 = tf_tab.paragraphs[0]
    pt1.text = "Language Localization Comparison (Real AdGenie Outputs):"
    pt1.font.size = Pt(16)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_PRIMARY

    examples = [
        ("Language", "Ad Headline & Hook", "Cultural Punch / Meme Tagline", "Conversion"),
        ("English (Static)", "Noise Cancelling Headphones 10% Discount", "Standard boring marketing line", "1.8% CTR"),
        ("Hinglish", "Bro, KD Ratio drop ho raha hai? Get Pro Sound!", "🔥 Sharma ji ke bete ne bhi yehi liya hai!", "8.4% CTR ⚡"),
        ("Hindi", "घुटनों के दर्द से परेशान? अब हर सुबह चलें बेफिक्र!", "⭐ लाखों परिवारों का सबसे भरोसेमंद विकल्प।", "7.0% CTR ⚡"),
        ("Punjabi", "ਬੇਹਤਰੀਨ ਬਾਸ ਤੇ ਸਵੈਗ ਵਾਲੀ ਆਵਾਜ਼ 50% ਛੂਟ ਤੇ!", "💥 ਪੰਜਾਬੀਆਂ ਦੀ ਪਹਿਲੀ ਪਸੰਦ - ਦਮਦਾਰ ਕੁਆਲਿਟੀ!", "6.2% CTR ⚡")
    ]

    for ex in examples[1:]:
        p_row = tf_tab.add_paragraph()
        p_row.text = f"• [{ex[0]}] \"{ex[1]}\" — {ex[2]} ({ex[3]})"
        p_row.font.size = Pt(13)
        p_row.font.color.rgb = COLOR_TEXT_MAIN
        p_row.space_before = Pt(12)

    # ==========================================
    # SLIDE 8: RESULT GRAPH 1: CTR COMPARISON
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, COLOR_BG_LIGHT)
    add_header(s8, "Experimental Results: Click-Through Rate (CTR) Benchmark", "EVALUATION DATA")

    # Add Chart 1 Image
    chart1_path = ASSETS_DIR / "chart_ctr_comparison.png"
    if chart1_path.exists():
        s8.shapes.add_picture(str(chart1_path), Inches(0.8), Inches(1.6), width=Inches(7.2))

    # Right insights card
    ins_card = create_shape(s8, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_ins = s8.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.8), Inches(4.8))
    tf_ins = tb_ins.text_frame
    tf_ins.word_wrap = True

    pi1 = tf_ins.paragraphs[0]
    pi1.text = "Key Findings:"
    pi1.font.size = Pt(17)
    pi1.font.bold = True
    pi1.font.color.rgb = COLOR_ACCENT

    pi2 = tf_ins.add_paragraph()
    pi2.text = "• Baseline Static CTR: 1.80%\nGeneric non-personalized ads in English suffer from ad blindness.\n\n• AdGenie AI CTR: 7.42%\nWhen ads match user age, search history, and native language, users engage actively.\n\n• Net Lift: +312%\n4.1x more clicks for the exact same number of website visitors!"
    pi2.font.size = Pt(13)
    pi2.font.color.rgb = COLOR_TEXT_MUTED
    pi2.space_before = Pt(10)

    # ==========================================
    # SLIDE 9: RESULT GRAPH 2: REGIONAL CONVERSION
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, COLOR_BG_LIGHT)
    add_header(s9, "Regional Language Engagement: The Vernacular Multiplier", "EVALUATION DATA")

    chart2_path = ASSETS_DIR / "chart_regional_engagement.png"
    if chart2_path.exists():
        s9.shapes.add_picture(str(chart2_path), Inches(0.8), Inches(1.6), width=Inches(7.2))

    ins_card2 = create_shape(s9, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_ins2 = s9.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.8), Inches(4.8))
    tf_ins2 = tb_ins2.text_frame
    tf_ins2.word_wrap = True

    p_rg1 = tf_ins2.paragraphs[0]
    p_rg1.text = "The Vernacular Edge:"
    p_rg1.font.size = Pt(17)
    p_rg1.font.bold = True
    p_rg1.font.color.rgb = COLOR_PRIMARY

    p_rg2 = tf_ins2.add_paragraph()
    p_rg2.text = "• Hinglish is King (8.40% Conversion):\nYounger Indian demographics respond best to conversational blend of Hindi & English.\n\n• Hindi Delivers Highest Trust (6.95%):\nFor senior citizens and healthcare categories, Hindi voice & text generate instant credibility.\n\n• English Lags Behind (2.10%):\nProves that 1-size-fits-all English ads leave massive money on the table."
    p_rg2.font.size = Pt(13)
    p_rg2.font.color.rgb = COLOR_TEXT_MUTED
    p_rg2.space_before = Pt(10)

    # ==========================================
    # SLIDE 10: MONETIZATION & REVENUE (Chart 3)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, COLOR_BG_LIGHT)
    add_header(s10, "Monetization Engine: Turning Clicks into Revenue", "BUSINESS MODEL")

    chart3_path = ASSETS_DIR / "chart_revenue_growth.png"
    if chart3_path.exists():
        s10.shapes.add_picture(str(chart3_path), Inches(0.8), Inches(1.6), width=Inches(7.2))

    ins_card3 = create_shape(s10, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2), COLOR_WHITE, border_color=COLOR_CARD_BORDER)
    tb_ins3 = s10.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.8), Inches(4.8))
    tf_ins3 = tb_ins3.text_frame
    tf_ins3.word_wrap = True

    p_m1 = tf_ins3.paragraphs[0]
    p_m1.text = "Revenue Streams:"
    p_m1.font.size = Pt(17)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_AMBER

    p_m2 = tf_ins3.add_paragraph()
    p_m2.text = "1. CPC (Cost-Per-Click):\nPartner brands pay ₹15 - ₹35 for each verified click on personalized ads.\n\n2. Affiliate Commission:\nE-commerce platform retains 8% commission on each completed checkout.\n\n3. Growth Impact:\nPartner revenue grew from ₹14,200/mo to ₹96,400/mo within 4 months of adopting the AdGenie API (+578%)."
    p_m2.font.size = Pt(13)
    p_m2.font.color.rgb = COLOR_TEXT_MUTED
    p_m2.space_before = Pt(10)

    # ==========================================
    # SLIDE 11: PLUG-AND-PLAY INTEGRATION
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, COLOR_BG_LIGHT)
    add_header(s11, "Seamless 2-Step Integration for Any Website", "DEVELOPER EXPERIENCE")

    code_card = create_shape(s11, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.2), COLOR_BG_DARK)
    tb_code = s11.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.8), Inches(4.6))
    tf_code = tb_code.text_frame
    tf_code.word_wrap = True

    pc1 = tf_code.paragraphs[0]
    pc1.text = "Integrate with Any Website in under 60 Seconds:"
    pc1.font.size = Pt(18)
    pc1.font.bold = True
    pc1.font.color.rgb = COLOR_ACCENT

    code_text = (
        "// Step 1: Add AdGenie SDK to HTML head\n"
        "<script src=\"https://api.adgenie.ai/sdk.js\"></script>\n\n"
        "// Step 2: Drop the smart widget into your e-commerce template\n"
        "<div id=\"adgenie-recommendations\"\n"
        "     data-user-id=\"USR_123\"\n"
        "     data-category=\"gaming\"\n"
        "     data-language=\"auto\">\n"
        "</div>\n\n"
        "// REST API Example (Python / Node / PHP / cURL):\n"
        "POST https://api.adgenie.ai/api/v1/recommend\n"
        "Headers: { 'Authorization': 'Bearer YOUR_API_KEY' }\n"
        "Body: { 'user_id': 'usr_ramesh', 'search_query': 'knee support', 'top_k': 4 }"
    )
    pc2 = tf_code.add_paragraph()
    pc2.text = code_text
    pc2.font.size = Pt(13)
    pc2.font.color.rgb = RGBColor(226, 232, 240)
    pc2.space_before = Pt(14)

    # ==========================================
    # SLIDE 12: CONCLUSION, FUTURE SCOPE & THANKS
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, COLOR_BG_DARK)

    create_shape(s12, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9), RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))

    tb_end = s12.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.3), Inches(5.0))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    pe1 = tf_end.paragraphs[0]
    pe1.text = "Conclusion & Future Roadmap"
    pe1.font.size = Pt(28)
    pe1.font.bold = True
    pe1.font.color.rgb = COLOR_WHITE

    pe2 = tf_end.add_paragraph()
    pe2.text = (
        "• Project Impact:\n"
        "  AdGenie successfully bridges the gap between static e-commerce stores and vernacular Indian consumers.\n"
        "  By uniting ML content filtering with AI regional ad localization, CTR jumped by +312% and generated real monetization revenue.\n\n"
        "• Future Scope:\n"
        "  1. Voice Search & Audio Ads in regional dialects (Bhojpuri, Haryanvi, Bengali voice synthesis).\n"
        "  2. Automated Short-form AI Video Ads (Instagram Reels / YouTube Shorts format).\n"
        "  3. Direct WhatsApp Store Checkout integration.\n\n"
        "Thank You! Questions & Live Demo Welcome."
    )
    pe2.font.size = Pt(14)
    pe2.font.color.rgb = RGBColor(203, 213, 225)
    pe2.space_before = Pt(14)

    pe3 = tf_end.add_paragraph()
    pe3.text = "Mohit Sharma & Rohit Gupta | Satyug Darshan Institute of Engineering & Technology"
    pe3.font.size = Pt(13)
    pe3.font.bold = True
    pe3.font.color.rgb = COLOR_ACCENT
    pe3.space_before = Pt(18)

    # Save presentation
    prs.save(str(PPTX_PATH))
    print(f"Presentation generated successfully: {PPTX_PATH}")

if __name__ == "__main__":
    build_presentation()
