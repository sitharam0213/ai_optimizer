import httpx
import json
import re
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_MAX_TOKENS, GROQ_TEMPERATURE


class GroqService:
    def __init__(self):
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

    async def _call(self, system: str, user: str) -> dict:
        payload = {
            "model": GROQ_MODEL,
            "temperature": GROQ_TEMPERATURE,
            "max_tokens": GROQ_MAX_TOKENS,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "response_format": {"type": "json_object"}
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            raw = data["choices"][0]["message"]["content"]
            return json.loads(raw)

    async def analyze_store(
        self,
        products: list,
        shop: dict,
        policies: list,
        collections: list
    ) -> dict:
        # Build a compact product sample for the prompt
        sample = []
        for p in products[:10]:
            desc = re.sub(r"<[^>]+>", "", p.get("body_html", ""))[:200]
            sample.append({
                "title": p.get("title"),
                "description": desc,
                "tags": p.get("tags"),
                "images": len(p.get("images", [])),
                "price": p.get("variants", [{}])[0].get("price"),
                "vendor": p.get("vendor")
            })

        policy_names = ", ".join(p["title"] for p in policies) or "None"

        system_prompt = (
            "You are an expert AI shopping agent analyst. "
            "Analyze Shopify store data and respond ONLY with valid JSON. "
            "No markdown, no text outside the JSON object."
        )

        user_prompt = f"""Analyze this Shopify store for AI representation quality.

Store info:
- Name: {shop.get("name", "Unknown")}
- Domain: {shop.get("domain", "Unknown")}
- Total products: {len(products)}
- Collections: {len(collections)}
- Policies available: {policy_names}

Product sample (first 10):
{json.dumps(sample, indent=2)}

Return this exact JSON structure:
{{
  "overall_score": <integer 0-100>,
  "current_perception": "<2-3 sentences: how an AI shopping agent currently perceives this store>",
  "ideal_perception": "<2-3 sentences: how the merchant ideally wants AI agents to represent them>",
  "agent_summary": "<A realistic 3-4 sentence summary an AI shopping agent might give a customer about this store>",
  "actions": [
    {{
      "title": "<short action title>",
      "description": "<specific, actionable description>",
      "impact": "High|Medium|Low",
      "effort": "Low|Medium|High",
      "category": "Products|Policies|SEO|Trust|Content"
    }}
  ]
}}

Generate exactly 6 actions, ranked by descending impact. Be specific and merchant-friendly."""

        return await self._call(system_prompt, user_prompt)
