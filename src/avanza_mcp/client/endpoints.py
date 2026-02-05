"""Avanza API endpoint definitions.

All endpoints are public and require no authentication.
"""

from enum import Enum


class PublicEndpoint(Enum):
    """Public Avanza API endpoints - no authentication required."""

    # Search
    SEARCH = "/_api/search/filtered-search"

    # Market data - Stocks
    STOCK_INFO = "/_api/market-guide/stock/{id}"
    STOCK_ANALYSIS = "/_api/market-guide/stock/{id}/analysis"
    STOCK_QUOTE = "/_api/market-guide/stock/{id}/quote"
    STOCK_MARKETPLACE = "/_api/market-guide/stock/{id}/marketplace"
    STOCK_ORDERDEPTH = "/_api/market-guide/stock/{id}/orderdepth"
    STOCK_TRADES = "/_api/market-guide/stock/{id}/trades"
    STOCK_BROKER_TRADES = "/_api/market-guide/stock/{id}/broker-trade-summaries"
    STOCK_CHART = "/_api/price-chart/stock/{id}"  # Requires timePeriod param

    # Market data - Funds
    FUND_INFO = "/_api/fund-guide/guide/{id}"
    FUND_SUSTAINABILITY = "/_api/fund-reference/sustainability/{id}"
    FUND_CHART = "/_api/fund-guide/chart/{id}/{time_period}"  # time_period: three_years, etc.
    FUND_CHART_PERIODS = "/_api/fund-guide/chart/timeperiods/{id}"
    FUND_DESCRIPTION = "/_api/fund-guide/description/{id}"

    # Market data - Indices (uses stock endpoint - works for indices)
    INDEX_INFO = "/_api/market-guide/stock/{id}"
    INDEX_CHART = "/_api/price-chart/stock/{id}"

    # Market data - ETFs (uses stock endpoint - works for all tradeable instruments)
    ETF_INFO = "/_api/market-guide/stock/{id}"
    ETF_DETAILS = "/_api/market-etf/{id}/details"

    # Market data - Certificates (uses stock endpoint)
    CERTIFICATE_INFO = "/_api/market-guide/stock/{id}"
    CERTIFICATE_DETAILS = "/_api/market-guide/stock/{id}/details"

    # Market data - Warrants (uses stock endpoint)
    WARRANT_INFO = "/_api/market-guide/stock/{id}"

    # Market data - Bonds (uses stock endpoint)
    BOND_INFO = "/_api/market-guide/stock/{id}"

    # Market data - Options (uses stock endpoint)
    OPTION_INFO = "/_api/market-guide/stock/{id}"

    # Market data - Futures/Forwards
    FUTURE_FORWARD_INFO = "/_api/market-guide/stock/{id}"

    # News
    NEWS = "/_api/market-guide/news/{id}"

    # Forum/Social
    FORUM = "/_api/market-guide/forum/{id}"

    # Generic instrument endpoint
    INSTRUMENT = "/_api/market-guide/{instrument_type}/{id}"
    INSTRUMENT_DETAILS = "/_api/market-guide/{instrument_type}/{id}/details"

    # Multiple orderbooks
    ORDERBOOKS = "/_api/trading-critical/rest/orderbook/list"

    def format(self, **kwargs: str | int) -> str:
        """Format endpoint path with variables.

        Args:
            **kwargs: Variables to format into the endpoint path

        Returns:
            Formatted endpoint path
        """
        return self.value.format(**kwargs)
