# AI Representation Optimizer
> Track 5 (Advanced) — Kasparro Shopify Hackathon

Diagnose how AI shopping agents perceive your Shopify store and get a ranked action plan to improve it.

---

## Project Structure

```
ai-optimizer/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # ← PASTE YOUR API KEYS HERE
│   ├── routers/
│   │   ├── shopify.py           # Shopify data endpoints
│   │   └── analyze.py           # Full analysis endpoint
│   └── services/
│       ├── shopify_service.py   # Shopify Admin API calls
│       ├── analyzer_service.py  # Local scoring logic
│       └── groq_service.py      # Groq LLM AI analysis
├── frontend/
│   ├── templates/
│   │   └── index.html           # Main UI template
│   └── static/
│       ├── css/style.css        # Styles
│       └── js/app.js            # Frontend logic
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Paste your API keys in `backend/config.py`
```python
SHOPIFY_STORE_URL    = "yourstore.myshopify.com"
SHOPIFY_ACCESS_TOKEN = "shpat_xxxxxxxxxxxx"
GROQ_API_KEY         = "gsk_xxxxxxxxxxxx"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
cd backend
python main.py
```

### 4. Open in browser
```
http://localhost:8000
```

---

## How It Works

1. **Fetches** products, policies, collections from Shopify Admin API
2. **Scores** each product across 6 dimensions (description, images, tags, price, vendor, title)
3. **Computes** store-level AI readiness gaps
4. **Calls Groq** (Llama 3.3 70B) to simulate an AI shopping agent perceiving your store
5. **Returns** an overall score + ranked action plan

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Frontend UI |
| POST | `/api/analyze/full` | Run full analysis |
| GET | `/api/shopify/products` | Raw products |
| GET | `/api/shopify/shop` | Shop info |
| GET | `/api/shopify/policies` | Store policies |
| GET | `/api/shopify/all` | All store data |
| GET | `/health` | Health check |
