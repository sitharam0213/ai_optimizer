import re


class AnalyzerService:

    def _strip_html(self, html: str) -> str:
        return re.sub(r"<[^>]+>", "", html or "").strip()

    def analyze_products(self, products: list) -> list:
        return [self._score_product(p) for p in products]

    def _score_product(self, product: dict) -> dict:
        score = 0
        issues = []

        # Title quality (15 pts)
        title = product.get("title", "")
        if len(title) > 10:
            score += 15
        else:
            issues.append("Weak or missing title")

        # Description quality (25 pts)
        desc = self._strip_html(product.get("body_html", ""))
        desc_len = len(desc)
        if desc_len > 200:
            score += 25
        elif desc_len > 50:
            score += 10
            issues.append("Short description — needs more detail")
        else:
            issues.append("Missing or very short description")

        # Image coverage (20 pts)
        images = len(product.get("images", []))
        if images >= 3:
            score += 20
        elif images >= 1:
            score += 10
            issues.append("Few images — add more angles/lifestyle shots")
        else:
            issues.append("No product images")

        # Tag coverage (15 pts)
        raw_tags = product.get("tags", "")
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else []
        tag_count = len(tags)
        if tag_count >= 5:
            score += 15
        elif tag_count >= 2:
            score += 7
            issues.append("Few tags — add more for AI discoverability")
        else:
            issues.append("Missing tags — AI agents can't categorize this product")

        # Pricing / variants (15 pts)
        variants = product.get("variants", [])
        if variants and float(variants[0].get("price", 0) or 0) > 0:
            score += 15
        else:
            issues.append("Missing or zero price")

        # Vendor / brand (10 pts)
        vendor = product.get("vendor", "")
        if vendor and len(vendor) > 2:
            score += 10
        else:
            issues.append("Missing vendor/brand name")

        return {
            "id": product.get("id"),
            "title": title,
            "score": min(score, 100),
            "issues": issues,
            "desc_len": desc_len,
            "images": images,
            "tags": tag_count,
            "vendor": vendor,
            "product_type": product.get("product_type", "")
        }

    def compute_gaps(self, products: list, policies: list) -> list:
        total = max(len(products), 1)
        gaps = []

        # 1. Description quality
        with_desc = sum(1 for p in products if len(self._strip_html(p.get("body_html", ""))) > 100)
        gaps.append({
            "name": "Product Description Quality",
            "score": round((with_desc / total) * 100),
            "desc": f"{with_desc}/{len(products)} products have detailed descriptions (>100 chars)"
        })

        # 2. Visual content
        with_imgs = sum(1 for p in products if len(p.get("images", [])) >= 2)
        gaps.append({
            "name": "Visual Content Coverage",
            "score": round((with_imgs / total) * 100),
            "desc": f"{with_imgs}/{len(products)} products have 2+ images"
        })

        # 3. Tag coverage
        with_tags = sum(1 for p in products if len([t for t in (p.get("tags","")).split(",") if t.strip()]) >= 3)
        gaps.append({
            "name": "Structured Tag Coverage",
            "score": round((with_tags / total) * 100),
            "desc": f"{with_tags}/{len(products)} products have 3+ tags for AI discovery"
        })

        # 4. Policy completeness
        meaningful_policies = sum(1 for p in policies if len(p.get("body", "")) > 50)
        gaps.append({
            "name": "Policy & Trust Signals",
            "score": min(round((meaningful_policies / 4) * 100), 100),
            "desc": f"{meaningful_policies}/4 key policies defined (refund, shipping, privacy, terms)"
        })

        # 5. Brand clarity
        with_vendor = sum(1 for p in products if len(p.get("vendor", "")) > 2)
        gaps.append({
            "name": "Brand & Vendor Clarity",
            "score": round((with_vendor / total) * 100),
            "desc": f"{with_vendor}/{len(products)} products have vendor/brand attribution"
        })

        # 6. Metadata richness
        with_meta = sum(1 for p in products if len(self._strip_html(p.get("body_html", ""))) > 300)
        gaps.append({
            "name": "SEO & Metadata Richness",
            "score": round((with_meta / total) * 100),
            "desc": f"{with_meta}/{len(products)} products have rich metadata (>300 chars)"
        })

        return gaps
