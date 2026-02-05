"""MCP tools for various instrument types - Indices, ETFs, Certificates, Warrants, etc."""

from fastmcp import Context

from .. import mcp
from ..client import AvanzaClient
from ..services import MarketDataService


# === Index Tools ===


@mcp.tool()
async def get_index_info(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get detailed information about a market index.

    Retrieve comprehensive data about market indices like OMXS30, S&P 500, DAX, etc.
    Includes current value, performance over various time periods, and trading data.

    Use search_instruments() with instrument_type="all" and search for index names
    to find the instrument_id for an index.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza index ID from search results

    Returns:
        Index information including:
        - orderbookId: Unique identifier
        - name: Index name
        - quote: Current value, change, changePercent
        - Performance: changeOneWeek, changeOneMonth, changeThreeMonths, changeOneYear, etc.
        - highestPrice/lowestPrice: 52-week high/low
        - currency: Quote currency

    Examples:
        Get OMXS30 info:
        >>> get_index_info(instrument_id="19002")

        Get S&P 500 info:
        >>> get_index_info(instrument_id="18996")
    """
    ctx.info(f"Fetching index info for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            index_info = await service.get_index_info(instrument_id)

        ctx.info(f"Retrieved info for index: {index_info.name}")
        return index_info.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch index info: {str(e)}")
        raise


@mcp.tool()
async def get_index_chart(
    ctx: Context,
    instrument_id: str,
    time_period: str = "one_year",
) -> dict:
    """Get historical chart data for a market index.

    Retrieve time series data for charting and technical analysis of indices.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza index ID
        time_period: Time period for chart data. Options:
            - "today": Intraday data
            - "one_week": Past week
            - "one_month": Past month
            - "three_months": Past 3 months
            - "this_year": Year to date
            - "one_year": Past year (default)
            - "three_years": Past 3 years
            - "five_years": Past 5 years

    Returns:
        Chart data with OHLC values for the index

    Examples:
        Get OMXS30 1-year chart:
        >>> get_index_chart(instrument_id="19002", time_period="one_year")
    """
    ctx.info(f"Fetching index chart for ID: {instrument_id} (time_period={time_period})")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            chart_data = await service.get_index_chart(instrument_id, time_period)

        data_points = len(chart_data.ohlc)
        ctx.info(f"Retrieved {data_points} data points for index chart")
        return chart_data.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch index chart: {str(e)}")
        raise


# === ETF Tools ===


@mcp.tool()
async def get_etf_info(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get information about an Exchange Traded Fund (ETF).

    Retrieve comprehensive ETF data including price, performance, fees,
    and tracking information. Essential for ETF analysis and comparison.

    Use search_instruments() with instrument_type="etf" to find ETF IDs.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza ETF ID from search results

    Returns:
        ETF information including:
        - Basic: name, isin, tickerSymbol, currency
        - Quote: lastPrice, change, changePercent, volume
        - Performance: changeOneWeek through changeFiveYears
        - Fees: managementFee, totalExpenseRatio
        - ETF specific: nav, trackingError, underlyingIndex, fundCompany

    Examples:
        Get info for an ETF:
        >>> get_etf_info(instrument_id="924016")
    """
    ctx.info(f"Fetching ETF info for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            etf_info = await service.get_etf_info(instrument_id)

        ctx.info(f"Retrieved info for ETF: {etf_info.name}")
        return etf_info.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch ETF info: {str(e)}")
        raise


@mcp.tool()
async def get_etf_details(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get detailed ETF information including holdings and allocations.

    Retrieve in-depth ETF data including portfolio holdings, sector allocation,
    country allocation, and fund characteristics. Essential for due diligence.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza ETF ID from search results

    Returns:
        Detailed ETF information including:
        - Description and fund company
        - Holdings: list of top holdings with weights
        - Allocations: country and sector breakdowns
        - Fund details: replicationMethod, distributionPolicy, inceptionDate, domicile
        - Fees: managementFee, totalExpenseRatio

    Examples:
        Get detailed info for an ETF:
        >>> get_etf_details(instrument_id="924016")
    """
    ctx.info(f"Fetching ETF details for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            etf_details = await service.get_etf_details(instrument_id)

        holdings_count = len(etf_details.holdings) if etf_details.holdings else 0
        ctx.info(f"Retrieved ETF details with {holdings_count} holdings")
        return etf_details.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch ETF details: {str(e)}")
        raise


# === Certificate Tools ===


@mcp.tool()
async def get_certificate_info(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get information about a certificate/structured product.

    Retrieve data for leveraged products, tracker certificates, and other
    structured products. Includes leverage, underlying, and barrier information.

    Use search_instruments() with instrument_type="certificate" to find certificate IDs.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza certificate ID from search results

    Returns:
        Certificate information including:
        - Basic: name, isin, tickerSymbol, currency, issuer
        - Quote: lastPrice, buyPrice, sellPrice, spread, volume
        - Product details: leverage, direction (LONG/SHORT)
        - Underlying: underlyingName, underlyingOrderbookId
        - Barriers: strikePrice, barrierLevel, knockOutLevel
        - Dates: endDate

    Examples:
        Get info for a leveraged certificate:
        >>> get_certificate_info(instrument_id="804912")
    """
    ctx.info(f"Fetching certificate info for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            cert_info = await service.get_certificate_info(instrument_id)

        ctx.info(f"Retrieved info for certificate: {cert_info.name}")
        return cert_info.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch certificate info: {str(e)}")
        raise


# === Warrant Tools ===


@mcp.tool()
async def get_warrant_info(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get information about a warrant including option greeks.

    Retrieve comprehensive warrant data including pricing, greeks (delta, gamma,
    theta, vega), and underlying information. Essential for options analysis.

    Use search_instruments() with instrument_type="warrant" to find warrant IDs.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza warrant ID from search results

    Returns:
        Warrant information including:
        - Basic: name, isin, tickerSymbol, currency, issuer
        - Quote: lastPrice, buyPrice, sellPrice, spread
        - Warrant details: warrantType (CALL/PUT), strikePrice, expirationDate
        - Underlying: underlyingName, underlyingPrice
        - Greeks: delta, gamma, theta, vega, rho, impliedVolatility
        - Values: intrinsicValue, timeValue, theoreticalValue

    Examples:
        Get info for a call warrant:
        >>> get_warrant_info(instrument_id="718858")
    """
    ctx.info(f"Fetching warrant info for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            warrant_info = await service.get_warrant_info(instrument_id)

        ctx.info(f"Retrieved info for warrant: {warrant_info.name}")
        return warrant_info.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch warrant info: {str(e)}")
        raise


# === Bond Tools ===


@mcp.tool()
async def get_bond_info(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get information about a bond.

    Retrieve bond data including yield, duration, coupon information,
    and credit rating. Useful for fixed income analysis.

    Use search_instruments() to find bond IDs.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza bond ID from search results

    Returns:
        Bond information including:
        - Basic: name, isin, currency, issuer
        - Quote: lastPrice, buyPrice, sellPrice
        - Coupon: couponRate, couponFrequency
        - Dates: maturityDate, issueDate
        - Yield metrics: yieldToMaturity, duration, modifiedDuration
        - Credit: creditRating, accruedInterest, faceValue

    Examples:
        Get info for a bond:
        >>> get_bond_info(instrument_id="572908")
    """
    ctx.info(f"Fetching bond info for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            bond_info = await service.get_bond_info(instrument_id)

        ctx.info(f"Retrieved info for bond: {bond_info.name}")
        return bond_info.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch bond info: {str(e)}")
        raise


# === Option Tools ===


@mcp.tool()
async def get_option_info(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get information about an option contract.

    Retrieve option data including strike, expiration, greeks, and
    open interest. Essential for options trading and analysis.

    Use search_instruments() to find option IDs.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza option ID from search results

    Returns:
        Option information including:
        - Basic: name, isin, currency
        - Quote: lastPrice, buyPrice, sellPrice
        - Contract: optionType (CALL/PUT), strikePrice, expirationDate, multiplier
        - Underlying: underlyingName, underlyingPrice
        - Greeks: delta, gamma, theta, vega, rho, impliedVolatility
        - Values: intrinsicValue, timeValue, openInterest

    Examples:
        Get info for an option:
        >>> get_option_info(instrument_id="1087813")
    """
    ctx.info(f"Fetching option info for ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            option_info = await service.get_option_info(instrument_id)

        ctx.info(f"Retrieved info for option: {option_info.name}")
        return option_info.model_dump(by_alias=True, exclude_none=True)

    except Exception as e:
        ctx.error(f"Failed to fetch option info: {str(e)}")
        raise


# === News Tools ===


@mcp.tool()
async def get_instrument_news(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get news articles related to an instrument.

    Retrieve recent news, press releases, and market commentary
    for a specific stock, fund, or other instrument.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza instrument ID from search results

    Returns:
        News data with:
        - news: Array of news items, each containing:
            - title: News headline
            - timestamp: Publication time
            - source: News source
            - body/summary: Article content
            - url: Link to full article

    Examples:
        Get news for Volvo B:
        >>> get_instrument_news(instrument_id="5479")
    """
    ctx.info(f"Fetching news for instrument ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            news_items = await service.get_news(instrument_id)

        ctx.info(f"Retrieved {len(news_items)} news items")
        return {
            "news": [item.model_dump(by_alias=True, exclude_none=True) for item in news_items]
        }

    except Exception as e:
        ctx.error(f"Failed to fetch news: {str(e)}")
        raise


# === Forum Tools ===


@mcp.tool()
async def get_instrument_forum(
    ctx: Context,
    instrument_id: str,
) -> dict:
    """Get forum discussions about an instrument.

    Retrieve community discussions and posts about a specific instrument.
    Useful for sentiment analysis and understanding retail investor views.

    Args:
        ctx: MCP context for logging
        instrument_id: Avanza instrument ID from search results

    Returns:
        Forum data with:
        - url: Link to the full forum thread
        - posts: Array of forum posts, each containing:
            - title: Post title
            - content: Post content
            - author: Username
            - timestamp: Post time
            - replies: Comment count
            - likes: Like count
            - url: Direct link to post

    Examples:
        Get forum posts for a stock:
        >>> get_instrument_forum(instrument_id="5479")
    """
    ctx.info(f"Fetching forum posts for instrument ID: {instrument_id}")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            forum_data = await service.get_forum_posts(instrument_id)

        posts_count = len(forum_data.get("posts", []))
        ctx.info(f"Retrieved {posts_count} forum posts")
        return forum_data

    except Exception as e:
        ctx.error(f"Failed to fetch forum posts: {str(e)}")
        raise


# === Batch Tools ===


@mcp.tool()
async def get_multiple_quotes(
    ctx: Context,
    orderbook_ids: str,
) -> dict:
    """Get quotes for multiple instruments in a single request.

    Efficiently retrieve price data for multiple instruments at once.
    Essential for portfolio monitoring and batch analysis.

    Args:
        ctx: MCP context for logging
        orderbook_ids: Comma-separated list of orderbook IDs (e.g., "5479,5269,3323")

    Returns:
        Batch quote data:
        - quotes: Array of quotes, each containing:
            - orderbookId, name
            - lastPrice, change, changePercent
            - buyPrice, sellPrice
            - highestPrice, lowestPrice
            - totalVolumeTraded, totalValueTraded
            - currency, updated

    Examples:
        Get quotes for multiple stocks:
        >>> get_multiple_quotes(orderbook_ids="5479,5269,3323")
    """
    # Parse comma-separated IDs
    ids_list = [id.strip() for id in orderbook_ids.split(",") if id.strip()]

    if not ids_list:
        ctx.error("No valid orderbook IDs provided")
        return {"quotes": [], "error": "No valid orderbook IDs provided"}

    ctx.info(f"Fetching quotes for {len(ids_list)} instruments")

    try:
        async with AvanzaClient() as client:
            service = MarketDataService(client)
            quotes = await service.get_multiple_quotes(ids_list)

        ctx.info(f"Retrieved {len(quotes)} quotes")
        return {"quotes": quotes}

    except Exception as e:
        ctx.error(f"Failed to fetch multiple quotes: {str(e)}")
        raise
