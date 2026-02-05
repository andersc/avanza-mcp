"""Pydantic models for Avanza API responses."""

from .common import InstrumentType, TimePeriod, Resolution
from .fund import (
    FundChart,
    FundChartPeriod,
    FundDescription,
    FundInfo,
    FundPerformance,
    FundSustainability,
)
from .search import SearchResponse, SearchHit
from .stock import (
    BrokerTradeSummary,
    MarketplaceInfo,
    OrderDepth,
    Quote,
    StockChart,
    StockInfo,
    Trade,
)
from .instruments import (
    IndexInfo,
    IndexQuote,
    ETFInfo,
    ETFDetails,
    ETFHolding,
    CertificateInfo,
    WarrantInfo,
    BondInfo,
    OptionInfo,
    NewsItem,
    NewsResponse,
    ForumPost,
    ForumResponse,
    BatchQuoteItem,
)

__all__ = [
    # Common
    "InstrumentType",
    "TimePeriod",
    "Resolution",
    # Search
    "SearchResponse",
    "SearchHit",
    # Stocks
    "Quote",
    "StockInfo",
    "StockChart",
    "MarketplaceInfo",
    "BrokerTradeSummary",
    "Trade",
    "OrderDepth",
    # Funds
    "FundInfo",
    "FundPerformance",
    "FundChart",
    "FundChartPeriod",
    "FundDescription",
    "FundSustainability",
    # Indices
    "IndexInfo",
    "IndexQuote",
    # ETFs
    "ETFInfo",
    "ETFDetails",
    "ETFHolding",
    # Certificates
    "CertificateInfo",
    # Warrants
    "WarrantInfo",
    # Bonds
    "BondInfo",
    # Options
    "OptionInfo",
    # News
    "NewsItem",
    "NewsResponse",
    # Forum
    "ForumPost",
    "ForumResponse",
    # Batch
    "BatchQuoteItem",
]
