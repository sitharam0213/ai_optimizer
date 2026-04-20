from fastapi import APIRouter, HTTPException
from services.shopify_service import ShopifyService
from services.analyzer_service import AnalyzerService
from services.groq_service import GroqService

router = APIRouter()
shopify = ShopifyService()
analyzer = AnalyzerService()
groq = GroqService()


@router.post("/full")
async def run_full_analysis():
    """
    Main endpoint: fetches store data, runs analysis, calls Groq AI,
    returns complete AI representation report.
    """
    try:
        # Step 1: Fetch all store data
        products, shop, policies, collections = await shopify.fetch_all()

        # Step 2: Analyze products locally
        analyzed_products = analyzer.analyze_products(products)

        # Step 3: Compute store-level gaps
        gaps = analyzer.compute_gaps(products, policies)

        # Step 4: AI perception via Groq
        ai_result = await groq.analyze_store(products, shop, policies, collections)

        # Step 5: Compute overall score
        avg_gap = sum(g["score"] for g in gaps) / max(len(gaps), 1)
        avg_product = sum(p["score"] for p in analyzed_products) / max(len(analyzed_products), 1)
        ai_score = ai_result.get("overall_score", 50)
        overall = round((avg_gap * 0.5) + (avg_product * 0.3) + (ai_score * 0.2))

        return {
            "overall_score": overall,
            "shop": shop,
            "metrics": {
                "total_products": len(products),
                "missing_descriptions": sum(1 for p in analyzed_products if p["desc_len"] < 100),
                "no_images": sum(1 for p in analyzed_products if p["images"] == 0),
                "weak_tags": sum(1 for p in analyzed_products if p["tags"] < 3),
            },
            "gaps": gaps,
            "products": analyzed_products,
            "ai_perception": {
                "current_perception": ai_result.get("current_perception", ""),
                "ideal_perception": ai_result.get("ideal_perception", ""),
                "agent_summary": ai_result.get("agent_summary", ""),
            },
            "actions": ai_result.get("actions", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
