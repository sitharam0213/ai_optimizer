from fastapi import APIRouter, HTTPException
from services.shopify_service import ShopifyService

router = APIRouter()
shopify = ShopifyService()


@router.get("/products")
async def get_products():
    try:
        return await shopify.fetch_products()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/shop")
async def get_shop():
    try:
        return await shopify.fetch_shop()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/policies")
async def get_policies():
    try:
        return await shopify.fetch_policies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections")
async def get_collections():
    try:
        return await shopify.fetch_collections()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_store_data():
    """Fetch all store data in one call"""
    try:
        products, shop, policies, collections = await shopify.fetch_all()
        return {
            "products": products,
            "shop": shop,
            "policies": policies,
            "collections": collections
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
