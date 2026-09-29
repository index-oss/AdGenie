// BharatMart Demo Store - AdGenie Integration Client

const API_BASE = window.location.origin;

let state = {
  isAdGenieActive: true,
  currentUserId: "usr_aman",
  currentLang: "hinglish",
  users: {},
  allProducts: [],
  recommendedProducts: [],
  currentAd: null,
  sessionRevenue: 0.0,
  sessionClicks: 0
};

// DOM Elements
const toggle = document.getElementById("adgenieToggle");
const personaSelect = document.getElementById("personaSelect");
const langSelect = document.getElementById("langSelect");
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const bannerSection = document.getElementById("bannerSection");
const recProductGrid = document.getElementById("recProductGrid");
const allProductGrid = document.getElementById("allProductGrid");
const hudRevenue = document.getElementById("hudRevenue");
const hudCtr = document.getElementById("hudCtr");
const revToast = document.getElementById("revToast");
const userAvatar = document.getElementById("userAvatar");
const userName = document.getElementById("userName");
const userMeta = document.getElementById("userMeta");
const userInterests = document.getElementById("userInterests");
const adgenieStatus = document.getElementById("adgenieStatus");
const statusText = document.getElementById("statusText");
const algoBadge = document.getElementById("algoBadge");
const analyticsBtn = document.getElementById("analyticsBtn");
const analyticsModal = document.getElementById("analyticsModal");
const closeModalBtn = document.getElementById("closeModalBtn");

// Initialize application
async function init() {
  setupEventListeners();
  await loadInitialData();
  renderUserStrip();
  await refreshExperience();
  await updateAnalyticsHUD();
}

function setupEventListeners() {
  toggle.addEventListener("change", async (e) => {
    state.isAdGenieActive = e.target.checked;
    updateModeIndicators();
    await refreshExperience();
  });

  personaSelect.addEventListener("change", async (e) => {
    state.currentUserId = e.target.value;
    const user = state.users[state.currentUserId];
    if (user && user.preferred_language) {
      state.currentLang = user.preferred_language;
      langSelect.value = user.preferred_language;
    }
    renderUserStrip();
    await refreshExperience();
  });

  langSelect.addEventListener("change", async (e) => {
    state.currentLang = e.target.value;
    await refreshExperience();
  });

  searchBtn.addEventListener("click", async () => {
    await refreshExperience();
  });

  searchInput.addEventListener("keypress", async (e) => {
    if (e.key === "Enter") {
      await refreshExperience();
    }
  });

  analyticsBtn.addEventListener("click", openAnalyticsModal);
  closeModalBtn.addEventListener("click", () => analyticsModal.classList.remove("open"));
  analyticsModal.addEventListener("click", (e) => {
    if (e.target === analyticsModal) analyticsModal.classList.remove("open");
  });
}

function updateModeIndicators() {
  const labelStatic = document.getElementById("labelStatic");
  const labelAi = document.getElementById("labelAi");

  if (state.isAdGenieActive) {
    labelStatic.classList.remove("active");
    labelAi.classList.add("active-ai");
    adgenieStatus.classList.remove("static-mode");
    statusText.innerText = "AdGenie AI Personalization Active";
    algoBadge.style.display = "block";
    algoBadge.innerText = "⚡ Model: Hybrid TF-IDF + Demographic";
  } else {
    labelStatic.classList.add("active");
    labelAi.classList.remove("active-ai");
    adgenieStatus.classList.add("static-mode");
    statusText.innerText = "Traditional Static Mode (No Personalization)";
    algoBadge.style.display = "block";
    algoBadge.innerText = "⚠️ Static Fixed Catalog Order";
  }
}

async function loadInitialData() {
  try {
    // 1. Fetch Users
    const usersRes = await fetch(`${API_BASE}/api/v1/users`);
    const usersData = await usersRes.json();
    usersData.forEach(u => state.users[u.user_id] = u);

    // 2. Fetch All Products
    const prodRes = await fetch(`${API_BASE}/api/v1/products`);
    state.allProducts = await prodRes.json();
    renderAllProducts(state.allProducts);
  } catch (err) {
    console.error("Failed to load initial data:", err);
  }
}

function renderUserStrip() {
  const user = state.users[state.currentUserId] || {
    name: "Guest Visitor",
    age: 25,
    city: "Mumbai",
    preferred_language: "hinglish",
    interests: ["Browsing"],
    persona_desc: "New visitor"
  };

  const avatars = {
    usr_aman: "🎓",
    usr_ramesh: "🧘",
    usr_priya: "💼",
    usr_harpreet: "⚡",
    usr_rohit_guest: "👤"
  };

  userAvatar.innerText = avatars[state.currentUserId] || "👤";
  userName.innerText = user.name;
  userMeta.innerText = `(Age ${user.age} | ${user.city} | ${user.preferred_language.toUpperCase()})`;
  userInterests.innerText = user.interests.length 
    ? `Interests: ${user.interests.join(", ")}` 
    : "Interests: Exploring popular trends";
}

async function refreshExperience() {
  const query = searchInput.value.trim();

  if (state.isAdGenieActive) {
    // 1. Fetch Recommendations from AdGenie
    try {
      const recRes = await fetch(`${API_BASE}/api/v1/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: state.currentUserId,
          search_query: query,
          top_k: 4
        })
      });
      const recData = await recRes.json();
      state.recommendedProducts = recData.recommendations;
      renderRecommendations(state.recommendedProducts);

      // 2. Fetch AI Localized Regional Ad Banner for top recommended item
      const topProduct = state.recommendedProducts[0] || state.allProducts[0];
      const adRes = await fetch(`${API_BASE}/api/v1/generate-ad`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          product_id: topProduct.id,
          user_id: state.currentUserId,
          language: state.currentLang,
          tone: "witty"
        })
      });
      state.currentAd = await adRes.json();
      renderAdBanner(state.currentAd, true);

      // Track impression
      trackEvent("impression", topProduct.id, true);
    } catch (err) {
      console.error("AdGenie API error:", err);
    }
  } else {
    // Static Store Mode: Fixed un-personalized order
    state.recommendedProducts = state.allProducts.slice(0, 4);
    renderRecommendations(state.recommendedProducts, false);
    renderAdBanner(null, false);
    trackEvent("impression", "generic_banner", false);
  }
}

function renderAdBanner(ad, isAi) {
  if (isAi && ad) {
    bannerSection.innerHTML = `
      <div class="adgenie-banner" onclick="handleAdClick('${ad.product_id}', true, '${ad.language}')">
        <div class="banner-content">
          <div class="banner-top-tags">
            <span class="tag-hook">${ad.hook_tag}</span>
            <span class="tag-discount">${ad.discount_badge}</span>
            <span class="tag-lang-badge">🗣️ ${ad.language_display} Ad</span>
          </div>
          <h2 class="banner-headline">${ad.headline}</h2>
          <p class="banner-subhead">${ad.subheadline}</p>
          <div class="banner-meme-tagline">${ad.meme_tagline}</div>
          <div class="banner-actions">
            <button class="banner-btn-cta">✨ ${ad.cta_text} →</button>
            <div class="banner-price-box">
              <span class="banner-price">₹${ad.price}</span>
              <span class="banner-orig-price">₹${ad.original_price}</span>
            </div>
          </div>
        </div>
        <div class="banner-image-box">
          <img src="${ad.image_url}" alt="${ad.product_name}" />
        </div>
        <div class="banner-watermark">ADGENIE</div>
      </div>
    `;
  } else {
    // Boring Static Banner
    bannerSection.innerHTML = `
      <div class="static-banner" onclick="handleAdClick('prod_generic', false, 'en')">
        <div>
          <div class="static-headline">Generic Static Shoe Advertisement (Unpersonalized)</div>
          <div class="static-subhead">Standard footwear collection for everyone. Flat 10% discount on cart.</div>
          <button class="static-btn">Buy Shoes Now</button>
        </div>
        <div>
          <span style="font-size: 11px; color: #94a3b8; font-weight: 700;">Traditional 1.8% CTR Banner</span>
        </div>
      </div>
    `;
  }
}

function renderRecommendations(products, isPersonalized = true) {
  const container = recProductGrid;
  container.innerHTML = "";

  products.forEach(p => {
    const card = document.createElement("div");
    card.className = "product-card";
    const discount = Math.round(((p.original_price - p.price) / p.original_price) * 100);
    const reason = isPersonalized ? (p.match_reason || "AI Recommended") : "Fixed Catalog Item";

    card.innerHTML = `
      <div class="card-reason-badge">${reason}</div>
      <div class="card-img-wrapper">
        <img src="${p.image_url}" alt="${p.name}" loading="lazy" />
      </div>
      <div>
        <div class="card-category">${p.category}</div>
        <h3 class="card-title">${p.name}</h3>
        <div class="card-rating">★ ${p.rating} <span>(${p.reviews_count} reviews)</span></div>
      </div>
      <div>
        <div class="card-price-row">
          <span class="price-current">₹${p.price}</span>
          <span class="price-original">₹${p.original_price}</span>
          <span class="price-discount">${discount}% off</span>
        </div>
        <button class="card-btn" onclick="handleProductBuy('${p.id}', ${p.price})">🛒 Quick View / Buy</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderAllProducts(products) {
  const container = allProductGrid;
  container.innerHTML = "";

  products.forEach(p => {
    const card = document.createElement("div");
    card.className = "product-card";
    const discount = Math.round(((p.original_price - p.price) / p.original_price) * 100);

    card.innerHTML = `
      <div class="card-img-wrapper">
        <img src="${p.image_url}" alt="${p.name}" loading="lazy" />
      </div>
      <div>
        <div class="card-category">${p.category}</div>
        <h3 class="card-title">${p.name}</h3>
        <div class="card-rating">★ ${p.rating} <span>(${p.reviews_count})</span></div>
      </div>
      <div>
        <div class="card-price-row">
          <span class="price-current">₹${p.price}</span>
          <span class="price-original">₹${p.original_price}</span>
          <span class="price-discount">${discount}% off</span>
        </div>
        <button class="card-btn" onclick="handleProductBuy('${p.id}', ${p.price})">🛒 Quick View / Buy</button>
      </div>
    `;
    container.appendChild(card);
  });
}

// Interaction Tracking & Revenue HUD
async function handleAdClick(productId, isPersonalized, lang) {
  await trackEvent("click", productId, isPersonalized, lang);

  if (isPersonalized) {
    state.sessionRevenue += 22.50;
    triggerRevenueToast("+₹22.50 CPC");
  } else {
    triggerRevenueToast("+₹5.00 Base");
  }

  state.sessionClicks += 1;
  await updateAnalyticsHUD();
}

async function handleProductBuy(productId, price) {
  await trackEvent("purchase", productId, state.isAdGenieActive);
  const commission = Math.round(price * 0.08);
  state.sessionRevenue += commission;
  triggerRevenueToast(`+₹${commission} Commission!`);
  await updateAnalyticsHUD();
}

async function trackEvent(eventType, productId, isPersonalized = true, lang = "hinglish") {
  try {
    await fetch(`${API_BASE}/api/v1/track`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event_type: eventType,
        product_id: productId,
        is_personalized: isPersonalized,
        ad_language: lang,
        user_id: state.currentUserId
      })
    });
  } catch (err) {
    console.error("Tracking error:", err);
  }
}

function triggerRevenueToast(text) {
  revToast.innerText = text;
  revToast.classList.add("show");
  setTimeout(() => revToast.classList.remove("show"), 1200);
}

async function updateAnalyticsHUD() {
  try {
    const res = await fetch(`${API_BASE}/api/v1/analytics`);
    const data = await res.json();

    hudRevenue.innerText = `₹${data.total_revenue_inr.toLocaleString('en-IN')}`;
    hudCtr.innerText = state.isAdGenieActive ? `${data.personalized_ctr}%` : `${data.static_ctr}%`;
  } catch (err) {
    console.error("HUD update error:", err);
  }
}

async function openAnalyticsModal() {
  try {
    const res = await fetch(`${API_BASE}/api/v1/analytics`);
    const data = await res.json();

    document.getElementById("mStaticCtr").innerText = `${data.static_ctr}%`;
    document.getElementById("mAiCtr").innerText = `${data.personalized_ctr}%`;
    document.getElementById("mRevenue").innerText = `₹${data.total_revenue_inr.toLocaleString('en-IN')}`;
    document.getElementById("mClicks").innerText = `${data.total_clicks.toLocaleString('en-IN')}`;

    // Language bars
    const langBars = document.getElementById("langBars");
    langBars.innerHTML = "";
    const maxClicks = Math.max(...Object.values(data.language_clicks));

    for (const [lang, clicks] of Object.entries(data.language_clicks)) {
      const pct = Math.round((clicks / maxClicks) * 100);
      const row = document.createElement("div");
      row.className = "bar-row";
      row.innerHTML = `
        <span class="bar-label">${lang}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${pct}%"></div>
        </div>
        <span class="bar-count">${clicks}</span>
      `;
      langBars.appendChild(row);
    }

    analyticsModal.classList.add("open");
  } catch (err) {
    console.error("Modal load error:", err);
  }
}

// Start
window.addEventListener("DOMContentLoaded", init);
