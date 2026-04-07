### Documentation for News API - https://www.thenewsapi.com/documentation

from __future__ import annotations

import os
from fastmcp import FastMCP
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple
from dotenv import load_dotenv

import requests

load_dotenv()

mcp = FastMCP(name="news", instructions="This server can provide news headlines and articles.")

class TheNewsAPIError(RuntimeError):
    """Raised when TheNewsAPI returns an error or an unexpected response."""


@dataclass(frozen=True)
class Article:
    uuid: str
    title: str
    description: str
    keywords: str
    snippet: str
    url: str
    image_url: str
    language: str
    published_at: str
    source: str
    categories: List[str]
    locale: Optional[str]
    relevance_score: Optional[float]


@dataclass(frozen=True)
class Meta:
    found: int
    returned: int
    limit: int
    page: int


@dataclass(frozen=True)
class NewsResponse:
    meta: Meta
    data: List[Article]


def _call_thenewsapi(
    endpoint_path: str,
    params: Dict[str, Any],
    *,
    api_token: Optional[str],
    timeout_s: float,
) -> Dict[str, Any]:
    token = api_token or os.getenv("THENEWSAPI_TOKEN")
    if not token:
        raise TheNewsAPIError("Missing API token. Provide api_token or set THENEWSAPI_TOKEN env var.")

    url = f"https://api.thenewsapi.com{endpoint_path}"
    params = dict(params)
    params["api_token"] = token

    resp = requests.get(url, params=params, timeout=timeout_s)
    resp.raise_for_status()

    data = resp.json()

    # The docs show error payloads like: {"error": {"code": "...", "message": "..."}} :contentReference[oaicite:3]{index=3}
    if isinstance(data, dict) and "error" in data:
        err = data.get("error") or {}
        raise TheNewsAPIError(f"TheNewsAPI error (code={err.get('code')}): {err.get('message')}")

    if not isinstance(data, dict) or "meta" not in data or "data" not in data:
        raise TheNewsAPIError("Unexpected response shape from TheNewsAPI.")

    return data


def _parse_news_response(payload: Dict[str, Any]) -> NewsResponse:
    m = payload["meta"] or {}
    meta = Meta(
        found=int(m.get("found", 0) or 0),
        returned=int(m.get("returned", 0) or 0),
        limit=int(m.get("limit", 0) or 0),
        page=int(m.get("page", 1) or 1),
    )

    articles: List[Article] = []
    for a in (payload.get("data") or []):
        articles.append(
            Article(
                uuid=str(a.get("uuid", "")),
                title=str(a.get("title", "")),
                description=str(a.get("description", "")),
                keywords=str(a.get("keywords", "")),
                snippet=str(a.get("snippet", "")),
                url=str(a.get("url", "")),
                image_url=str(a.get("image_url", "")),
                language=str(a.get("language", "")),
                published_at=str(a.get("published_at", "")),
                source=str(a.get("source", "")),
                categories=list(a.get("categories") or []),
                locale=a.get("locale", None),
                relevance_score=(None if a.get("relevance_score") is None else float(a["relevance_score"])),
            )
        )

    return NewsResponse(meta=meta, data=articles)


@mcp.tool(name="get_top_stories", description="Get top stories")
def get_top_stories(
    *,
    locale: Optional[str] = None,
    language: Optional[str] = None,
    categories: Optional[str] = None,
    exclude_categories: Optional[str] = None,
    domains: Optional[str] = None,
    exclude_domains: Optional[str] = None,
    source_ids: Optional[str] = None,
    exclude_source_ids: Optional[str] = None,
    search: Optional[str] = None,
    search_fields: Optional[str] = None,
    published_before: Optional[str] = None,
    published_after: Optional[str] = None,
    limit: Optional[int] = None,
    page: int = 1,
    api_token: Optional[str] = None,
    timeout_s: float = 10.0,
) -> NewsResponse:
    """
    Top Stories endpoint: /v1/news/top :contentReference[oaicite:4]{index=4}

    Notes:
      - Pagination uses `limit` and `page`; default page is 1; max result set 20,000. :contentReference[oaicite:5]{index=5}
    """
    params: Dict[str, Any] = {"page": page}
    if limit is not None:
        params["limit"] = limit
    if locale:
        params["locale"] = locale
    if language:
        params["language"] = language
    if categories:
        params["categories"] = categories
    if exclude_categories:
        params["exclude_categories"] = exclude_categories
    if domains:
        params["domains"] = domains
    if exclude_domains:
        params["exclude_domains"] = exclude_domains
    if source_ids:
        params["source_ids"] = source_ids
    if exclude_source_ids:
        params["exclude_source_ids"] = exclude_source_ids
    if search:
        params["search"] = search
    if search_fields:
        params["search_fields"] = search_fields
    if published_before:
        params["published_before"] = published_before
    if published_after:
        params["published_after"] = published_after

    payload = _call_thenewsapi("/v1/news/top", params, api_token=api_token, timeout_s=timeout_s)
    return _parse_news_response(payload)


@mcp.tool(name="get_all_news", description="Get all news")
def get_all_news(
    *,
    locale: Optional[str] = None,
    language: Optional[str] = None,
    categories: Optional[str] = None,
    exclude_categories: Optional[str] = None,
    domains: Optional[str] = None,
    exclude_domains: Optional[str] = None,
    source_ids: Optional[str] = None,
    exclude_source_ids: Optional[str] = None,
    search: Optional[str] = None,
    search_fields: Optional[str] = None,
    published_before: Optional[str] = None,
    published_after: Optional[str] = None,
    limit: Optional[int] = None,
    page: int = 1,
    api_token: Optional[str] = None,
    timeout_s: float = 10.0,
) -> NewsResponse:
    """
    All News endpoint: /v1/news/all :contentReference[oaicite:6]{index=6}

    Notes:
      - Supports advanced `search` syntax (+, |, -, quotes, etc.) and must be URL-encoded when using special chars. :contentReference[oaicite:7]{index=7}
      - Pagination uses `limit` and `page`; default page is 1; max result set 20,000. :contentReference[oaicite:8]{index=8}
    """
    params: Dict[str, Any] = {"page": page}
    if limit is not None:
        params["limit"] = limit
    if locale:
        params["locale"] = locale
    if language:
        params["language"] = language
    if categories:
        params["categories"] = categories
    if exclude_categories:
        params["exclude_categories"] = exclude_categories
    if domains:
        params["domains"] = domains
    if exclude_domains:
        params["exclude_domains"] = exclude_domains
    if source_ids:
        params["source_ids"] = source_ids
    if exclude_source_ids:
        params["exclude_source_ids"] = exclude_source_ids
    if search:
        params["search"] = search
    if search_fields:
        params["search_fields"] = search_fields
    if published_before:
        params["published_before"] = published_before
    if published_after:
        params["published_after"] = published_after

    payload = _call_thenewsapi("/v1/news/all", params, api_token=api_token, timeout_s=timeout_s)
    return _parse_news_response(payload)


def iter_all_news_pages(
    *,
    limit: int = 50,
    max_pages: Optional[int] = None,
    api_token: Optional[str] = None,
    timeout_s: float = 10.0,
    **kwargs: Any,
) -> Iterable[NewsResponse]:
    """
    Convenience generator to iterate pages until exhaustion (when meta.returned < meta.limit). :contentReference[oaicite:9]{index=9}
    Pass any get_all_news(...) filters via kwargs (e.g., search="apple", language="en").
    """
    page = 1
    while True:
        resp = get_all_news(limit=limit, page=page, api_token=api_token, timeout_s=timeout_s, **kwargs)
        yield resp

        if resp.meta.returned < resp.meta.limit:
            break
        page += 1
        if max_pages is not None and page > max_pages:
            break


# Example:
# os.environ["THENEWSAPI_TOKEN"] = "<your_token>"
# top = get_top_stories(locale="in", language="en", limit=5)
# alln = get_all_news(search='forex + (usd | gbp) -cad', language="en", categories="business,tech", limit=10)
# for page_resp in iter_all_news_pages(search="AI", language="en", limit=50, max_pages=3):
#     print(page_resp.meta.page, len(page_resp.data))

# top = get_top_stories(locale="in", language="en", limit=5)
# print(top)

# alln = get_all_news(search='iran', language="en", categories="general", limit=10)
# print(alln)


# Run the MCP server with streamable-http transport
# if __name__ == "__main__":
#     mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)

# Run MCP server with stdio transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
