# AdGenie 🧞‍♂️

AI-powered recommendation engine with culturally-adapted ad translation — as a single API.

AdGenie recommends products based on user purchase history/behavior, then generates and localizes ad copy for a target language and region — going beyond word-to-word translation to adapt tone, idioms, and cultural context.

---

## Overview

```
User purchase/behavior data → Recommend product → Generate ad copy → Localize ad (language + culture)
```

AdGenie exposes this as a set of API endpoints that any developer can call using their own API key.

---

## Features

- **Product Recommendation** — content-based / collaborative filtering using user purchase history
- **AI-Powered Localization** — LLM-based translation that adapts tone, idioms, and cultural references (not literal translation)
- **API Key Management** — users sign up, log in, and generate their own API key via the dashboard
- **Combined Pipeline** — single endpoint that runs recommendation → ad generation → localization in one call

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js, deployed on Vercel |
| Auth | Clerk |
| Backend | Python + FastAPI |
| Recommendation (ML) | Pandas, NumPy, Scikit-learn, Surprise |
| Localization (AI) | Claude / OpenAI API |
| Database | SQLite (MVP) → PostgreSQL (scale) |
| Dataset | Kaggle (Retail Rocket / Amazon Reviews) |

---

## Repository Structure

```
AdGenie/
├── frontend/              # Next.js app (deployed on Vercel — Root Directory = frontend)
│   ├── app/
│   ├── components/
│   └── package.json
│
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/        # recommend.py, localize.py, auth.py
│   │   ├── models/         # DB models
│   │   ├── services/       # recommender.py, localizer.py
│   │   ├── core/           # config.py, security.py
│   │   └── db/
│   └── requirements.txt
│
├── ml/
│   ├── data/                # dataset (gitignored)
│   ├── notebooks/           # exploration / training
│   └── train_model.py
│
├── docs/
│   └── API.md
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## API Endpoints (planned)

| Endpoint | Description |
|---|---|
| `POST /recommend` | Returns recommended products for a user |
| `POST /localize-ad` | Localizes ad copy for a target language/region |
| `POST /generate-ad-campaign` | Full pipeline: recommend → generate ad → localize |

All endpoints require an API key passed via header:
```
x-api-key: adg_xxxxxxxxxxxxx
```

---

## Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment Variables

**frontend/.env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
```

**backend/.env**
```
DATABASE_URL=
ANTHROPIC_API_KEY=
CLERK_SECRET_KEY=
```

---

## Status

🚧 In active development.

- [x] Project structure planned
- [x] Frontend repo + Vercel deployment
- [ ] Recommendation model (dataset exploration)
- [ ] Localization module (LLM integration)
- [ ] API key generation + auth flow
- [ ] Combined pipeline endpoint
- [ ] Backend deployment (Render/Railway)

---

## License

TBD
