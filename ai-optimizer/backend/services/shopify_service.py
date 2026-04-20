import httpx
import asyncio
from config import SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION


class ShopifyService:
    def __init__(self):
        self.base_url = f"https://{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}"
        self.headers = {
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

    async def _get(self, endpoint: str) -> dict:
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def fetch_products(self) -> list:
        fields = "id,title,body_html,vendor,tags,images,variants,product_type"
        data = await self._get(f"products.json?limit=50&fields={fields}")
        return data.get("products", [])

    async def fetch_shop(self) -> dict:
        data = await self._get("shop.json")
        return data.get("shop", {})

    async def fetch_policies(self) -> list:
        data = await self._get("policies.json")
        return data.get("policies", [])

    async def fetch_collections(self) -> list:
        data = await self._get("custom_collections.json?limit=10")
        return data.get("custom_collections", [])

    async def fetch_all(self):
        """Fetch all data concurrently"""
        results = await asyncio.gather(
            self.fetch_products(),
            self.fetch_shop(),
            self.fetch_policies(),
            self.fetch_collections(),
            return_exceptions=True
        )
        # Handle partial failures gracefully
        products   = results[0] if not isinstance(results[0], Exception) else []
        shop       = results[1] if not isinstance(results[1], Exception) else {}
        policies   = results[2] if not isinstance(results[2], Exception) else []
        collections = results[3] if not isinstance(results[3], Exception) else []
        return products, shop, policies, collections
