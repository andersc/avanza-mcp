"""Market data service for retrieving stock and fund information."""

from typing import Any

from ..client.base import AvanzaClient
from ..client.endpoints import PublicEndpoint
from ..models.fund import (
    FundChart,
    FundChartPeriod,
    FundDescription,
    FundInfo,
    FundSustainability,
)
from ..models.stock import (
    BrokerTradeSummary,
    MarketplaceInfo,
    OrderDepth,
    Quote,
    StockChart,
    StockInfo,
    Trade,
)
from ..models.instruments import (
    IndexInfo,
    ETFInfo,
    ETFDetails,
    CertificateInfo,
    WarrantInfo,
    BondInfo,
    OptionInfo,
    NewsItem,
)


class MarketDataService:
    """Service for retrieving market data."""

    def __init__(self, client: AvanzaClient) -> None:
        """Initialize market data service.

        Args:
            client: Avanza HTTP client
        """
        self._client = client

    async def get_stock_info(self, instrument_id: str) -> StockInfo:
        """Fetch detailed stock information.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Detailed stock information

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return StockInfo.model_validate(raw_data)

    async def get_fund_info(self, instrument_id: str) -> FundInfo:
        """Fetch detailed fund information.

        Args:
            instrument_id: Avanza fund ID

        Returns:
            Detailed fund information

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.FUND_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return FundInfo.model_validate(raw_data)

    async def get_order_depth(self, instrument_id: str) -> OrderDepth:
        """Fetch real-time order book depth data.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Order book depth with buy and sell levels

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_ORDERDEPTH.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return OrderDepth.model_validate(raw_data)

    async def get_chart_data(
        self,
        instrument_id: str,
        time_period: str = "one_year",
    ) -> StockChart:
        """Fetch historical chart data with OHLC values.

        Args:
            instrument_id: Avanza instrument ID
            time_period: Time period - one_week, one_month, three_months, one_year, etc.

        Returns:
            Chart data with OHLC values

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_CHART.format(id=instrument_id)
        params = {"timePeriod": time_period}
        raw_data = await self._client.get(endpoint, params=params)
        return StockChart.model_validate(raw_data)

    async def get_marketplace_info(self, instrument_id: str) -> MarketplaceInfo:
        """Fetch marketplace status and trading hours.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Marketplace information including open/close times

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_MARKETPLACE.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return MarketplaceInfo.model_validate(raw_data)

    async def get_trades(self, instrument_id: str) -> list[Trade]:
        """Fetch recent trades for an instrument.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            List of recent trades

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_TRADES.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return [Trade.model_validate(trade) for trade in raw_data]

    async def get_broker_trades(self, instrument_id: str) -> list[BrokerTradeSummary]:
        """Fetch broker trade summaries.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            List of broker trade summaries with buy/sell volumes

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_BROKER_TRADES.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return [BrokerTradeSummary.model_validate(trade) for trade in raw_data]

    async def get_stock_analysis(self, instrument_id: str) -> dict[str, Any]:
        """Fetch stock analysis with key ratios by year and quarter.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Stock analysis data with key ratios grouped by time periods

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_ANALYSIS.format(id=instrument_id)
        return await self._client.get(endpoint)

    async def get_dividends(self, instrument_id: str) -> dict[str, Any]:
        """Fetch dividend history from stock analysis data.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Dividend data by year including:
            - dividend: Dividend amount per share
            - exDate: Ex-dividend date
            - paymentDate: Payment date
            - yield: Dividend yield percentage

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_ANALYSIS.format(id=instrument_id)
        analysis = await self._client.get(endpoint)
        return {
            "dividendsByYear": analysis.get("dividendsByYear", []),
        }

    async def get_company_financials(self, instrument_id: str) -> dict[str, Any]:
        """Fetch company financial data from stock analysis.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Company financials by year and quarter including revenue,
            profit margins, earnings, and other financial metrics

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_ANALYSIS.format(id=instrument_id)
        analysis = await self._client.get(endpoint)
        return {
            "companyFinancialsByYear": analysis.get("companyFinancialsByYear", []),
            "companyFinancialsByQuarter": analysis.get("companyFinancialsByQuarter", []),
            "companyFinancialsByQuarterTTM": analysis.get(
                "companyFinancialsByQuarterTTM", []
            ),
        }

    async def get_stock_quote(self, instrument_id: str) -> Quote:
        """Fetch real-time stock quote with current pricing.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Real-time quote with buy, sell, last price, and trading volumes

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.STOCK_QUOTE.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return Quote.model_validate(raw_data)

    async def get_fund_sustainability(self, instrument_id: str) -> FundSustainability:
        """Fetch fund sustainability and ESG metrics.

        Args:
            instrument_id: Avanza fund ID

        Returns:
            Sustainability metrics including ESG scores and environmental data

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.FUND_SUSTAINABILITY.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return FundSustainability.model_validate(raw_data)

    async def get_fund_chart(
        self, instrument_id: str, time_period: str = "three_years"
    ) -> FundChart:
        """Fetch fund chart data for a specific time period.

        Args:
            instrument_id: Avanza fund ID
            time_period: Time period (e.g., three_years, five_years, etc.)

        Returns:
            Fund chart with historical performance data

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.FUND_CHART.format(
            id=instrument_id, time_period=time_period
        )
        raw_data = await self._client.get(endpoint)
        return FundChart.model_validate(raw_data)

    async def get_fund_chart_periods(self, instrument_id: str) -> list[FundChartPeriod]:
        """Fetch available fund chart periods with performance data.

        Args:
            instrument_id: Avanza fund ID

        Returns:
            List of time periods with performance changes

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.FUND_CHART_PERIODS.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return [FundChartPeriod.model_validate(period) for period in raw_data]

    async def get_fund_description(self, instrument_id: str) -> FundDescription:
        """Fetch fund description and category information.

        Args:
            instrument_id: Avanza fund ID

        Returns:
            Fund description with detailed category information

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.FUND_DESCRIPTION.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return FundDescription.model_validate(raw_data)

    # === Index Methods ===

    async def get_index_info(self, instrument_id: str) -> IndexInfo:
        """Fetch index information.

        Args:
            instrument_id: Avanza index ID

        Returns:
            Index information with quote and performance data

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.INDEX_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return IndexInfo.model_validate(raw_data)

    async def get_index_chart(
        self, instrument_id: str, time_period: str = "one_year"
    ) -> StockChart:
        """Fetch index chart data.

        Args:
            instrument_id: Avanza index ID
            time_period: Time period for chart

        Returns:
            Chart data with OHLC values

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.INDEX_CHART.format(id=instrument_id)
        params = {"timePeriod": time_period}
        raw_data = await self._client.get(endpoint, params=params)
        return StockChart.model_validate(raw_data)

    # === ETF Methods ===

    async def get_etf_info(self, instrument_id: str) -> ETFInfo:
        """Fetch ETF information.

        Args:
            instrument_id: Avanza ETF ID

        Returns:
            ETF information with quote and performance data

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.ETF_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return ETFInfo.model_validate(raw_data)

    async def get_etf_details(self, instrument_id: str) -> ETFDetails:
        """Fetch detailed ETF information including holdings.

        Args:
            instrument_id: Avanza ETF ID

        Returns:
            Detailed ETF information with holdings and allocations

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.ETF_DETAILS.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return ETFDetails.model_validate(raw_data)

    # === Certificate Methods ===

    async def get_certificate_info(self, instrument_id: str) -> CertificateInfo:
        """Fetch certificate/structured product information.

        Args:
            instrument_id: Avanza certificate ID

        Returns:
            Certificate information with quote and product details

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.CERTIFICATE_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return CertificateInfo.model_validate(raw_data)

    # === Warrant Methods ===

    async def get_warrant_info(self, instrument_id: str) -> WarrantInfo:
        """Fetch warrant information including greeks.

        Args:
            instrument_id: Avanza warrant ID

        Returns:
            Warrant information with greeks and underlying data

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.WARRANT_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return WarrantInfo.model_validate(raw_data)

    # === Bond Methods ===

    async def get_bond_info(self, instrument_id: str) -> BondInfo:
        """Fetch bond information.

        Args:
            instrument_id: Avanza bond ID

        Returns:
            Bond information with yield and duration data

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.BOND_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return BondInfo.model_validate(raw_data)

    # === Option Methods ===

    async def get_option_info(self, instrument_id: str) -> OptionInfo:
        """Fetch option information.

        Args:
            instrument_id: Avanza option ID

        Returns:
            Option information with greeks

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.OPTION_INFO.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return OptionInfo.model_validate(raw_data)

    # === News Methods ===

    async def get_news(self, instrument_id: str) -> list[NewsItem]:
        """Fetch news for an instrument.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            List of news items related to the instrument

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.NEWS.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        # Handle both list and dict response formats
        if isinstance(raw_data, list):
            return [NewsItem.model_validate(item) for item in raw_data]
        elif isinstance(raw_data, dict):
            # Avanza returns "articles" for news
            news_list = raw_data.get("articles", raw_data.get("news", raw_data.get("items", [])))
            return [NewsItem.model_validate(item) for item in news_list]
        return []

    # === Forum Methods ===

    async def get_forum_posts(self, instrument_id: str) -> dict[str, Any]:
        """Fetch forum posts for an instrument.

        Args:
            instrument_id: Avanza instrument ID

        Returns:
            Forum data with URL and list of posts

        Raises:
            AvanzaError: If request fails
        """
        endpoint = PublicEndpoint.FORUM.format(id=instrument_id)
        raw_data = await self._client.get(endpoint)
        return raw_data

    # === Batch Methods ===

    async def get_multiple_quotes(
        self, orderbook_ids: list[str]
    ) -> list[dict[str, Any]]:
        """Fetch quotes for multiple instruments.

        Falls back to individual requests if batch endpoint not available.

        Args:
            orderbook_ids: List of orderbook IDs

        Returns:
            List of quote data for each instrument

        Raises:
            AvanzaError: If request fails
        """
        try:
            endpoint = PublicEndpoint.ORDERBOOKS.value
            payload = {"orderbookIds": orderbook_ids}
            raw_data = await self._client.post(endpoint, json=payload)
            # Handle response format
            if isinstance(raw_data, list):
                return raw_data
            elif isinstance(raw_data, dict):
                return raw_data.get("orderbooks", raw_data.get("items", []))
            return []
        except Exception:
            # Batch endpoint not available, fall back to individual requests
            results = []
            for oid in orderbook_ids:
                try:
                    quote = await self.get_stock_quote(oid)
                    results.append(quote.model_dump(by_alias=True, exclude_none=True))
                except Exception:
                    results.append({"orderbookId": oid, "error": "Failed to fetch"})
            return results

