from typing import Optional
import re
import html

from price_parser import Price
from base.items import CategoryItem, ProductItem
from web_poet import Returns, WebPage, field, handle_urls


@handle_urls("books.toscrape.com")
class BooksToscrapeComProductItemPage(WebPage, Returns[ProductItem]):
    @field
    def name(self) -> Optional[str]:
        title = self.css("div.product_main h1::text").get()
        if not title:
            return None
        title = title.strip()
        return title if title else None

    @field
    def price(self) -> Optional[float]:
        text = self.css("p.price_color::text").get()
        if not text:
            return None
        text = text.strip()
        # Try using price_parser first
        parsed = Price.fromstring(text)
        amount = parsed.amount_float
        if amount is not None:
            return float(amount)
        # Fallback: extract first numeric token and normalize comma thousands separators
        m = re.search(r"(\d+(?:[.,]\d+)?)" , text)
        if not m:
            return None
        num_text = m.group(1).replace(",", "")
        try:
            return float(num_text)
        except ValueError:
            return None

    @field
    def sku(self) -> Optional[str]:
        sku_text = self.xpath(
            '//th[normalize-space(text())="UPC"]/following-sibling::td[1]/text()'
        ).get()
        if not sku_text:
            return None
        return sku_text.strip()

    @field
    def url(self) -> Optional[str]:
        page_url = getattr(self.response, "url", None)
        if page_url is None:
            return None
        return str(page_url)


@handle_urls("books.toscrape.com")
class BooksToscrapeComCategoryItemPage(WebPage, Returns[CategoryItem]):
    @field
    def book_urls(self) -> list[str]:
        hrefs = self.css(
            "ol.row li article.product_pod h3 a::attr(href)"
        ).getall()
        if not hrefs:
            return []
        results: list[str] = []
        seen: set[str] = set()
        for raw in hrefs:
            if not raw:
                continue
            href = html.unescape(raw).strip()
            try:
                absolute = self.urljoin(href)
            except Exception:
                # Skip invalid hrefs; keep extraction robust
                continue
            if absolute in seen:
                continue
            seen.add(absolute)
            results.append(absolute)
        return results

    @field
    def next_page_url(self) -> Optional[str]:
        href = self.css("ul.pager li.next a::attr(href)").get()
        if not href:
            href = self.css("li.next a::attr(href)").get()
        if not href:
            return None
        try:
            return self.urljoin(href)
        except Exception:
            return None
