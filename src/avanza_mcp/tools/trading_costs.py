"""MCP tools for Avanza trading cost calculations.

Provides tools to calculate trading costs based on Avanza's courtage classes,
markets, instrument types, and currency exchange fees.

Pricing data last updated: February 2026
"""

from typing import Literal

from fastmcp import Context

from .. import mcp


# === Pricing Data (as of February 2026) ===

COURTAGE_CLASSES = {
    "start": {
        "name": "Start",
        "description": "Free trading for accounts up to 50,000 SEK",
        "monthly_fee": 0,
        "max_account_value": 50000,
        "swedish_stocks": {
            "min_fee": 0,
            "percentage": 0,
            "max_fee": None,
            "breakpoint": None,
        },
    },
    "mini": {
        "name": "Mini",
        "description": "Best for small trades under 400 SEK",
        "monthly_fee": 0,
        "max_account_value": None,
        "swedish_stocks": {
            "min_fee": 1,
            "percentage": 0.25,  # 0.25%
            "max_fee": None,
            "breakpoint": 400,  # Min fee applies up to this amount
        },
    },
    "small": {
        "name": "Small",
        "description": "Best for trades up to 26,000 SEK",
        "monthly_fee": 0,
        "max_account_value": None,
        "swedish_stocks": {
            "min_fee": 39,
            "percentage": 0.15,  # 0.15%
            "max_fee": None,
            "breakpoint": 26000,
        },
    },
    "medium": {
        "name": "Medium",
        "description": "Best for trades up to 100,000 SEK",
        "monthly_fee": 0,
        "max_account_value": None,
        "swedish_stocks": {
            "min_fee": 69,
            "percentage": 0.069,  # 0.069%
            "max_fee": None,
            "breakpoint": 100000,
        },
    },
    "fast_pris": {
        "name": "Fast Pris",
        "description": "Fixed 99 SEK per trade regardless of size",
        "monthly_fee": 0,
        "max_account_value": None,
        "swedish_stocks": {
            "min_fee": 99,
            "percentage": 0,
            "max_fee": 99,
            "breakpoint": None,
        },
    },
}

# Foreign market fees (same across courtage classes)
FOREIGN_MARKETS = {
    "usa": {
        "name": "USA (NYSE, NASDAQ)",
        "currency": "USD",
        "min_fee_local": 1,  # 1 USD minimum
        "percentage": 0.15,  # 0.15%
        "exchange_spread": 0.25,  # 0.25% each way
    },
    "canada": {
        "name": "Canada (TSX)",
        "currency": "CAD",
        "min_fee_local": 1,  # 1 CAD minimum
        "percentage": 0.15,
        "exchange_spread": 0.25,
    },
    "europe_eur": {
        "name": "Europe (EUR markets)",
        "currency": "EUR",
        "min_fee_local": 1,  # 1 EUR minimum
        "percentage": 0.15,
        "exchange_spread": 0.25,
    },
    "europe_gbp": {
        "name": "UK (LSE)",
        "currency": "GBP",
        "min_fee_local": 1,  # 1 GBP minimum
        "percentage": 0.15,
        "exchange_spread": 0.25,
    },
    "denmark": {
        "name": "Denmark (Copenhagen)",
        "currency": "DKK",
        "min_fee_local": 9,  # 9 DKK minimum
        "percentage": 0.15,
        "exchange_spread": 0.15,
    },
    "norway": {
        "name": "Norway (Oslo)",
        "currency": "NOK",
        "min_fee_local": 9,  # 9 NOK minimum
        "percentage": 0.15,
        "exchange_spread": 0.15,
    },
    "finland": {
        "name": "Finland (Helsinki)",
        "currency": "EUR",
        "min_fee_local": 1,
        "percentage": 0.15,
        "exchange_spread": 0.25,
    },
}

# Derivative pricing
DERIVATIVES = {
    "certificates": {
        "name": "Certificates (Bull/Bear)",
        "avanza_markets_free": True,  # Free for orders >= 1000 SEK on Avanza Markets
        "avanza_markets_min_order": 1000,
        "other_min_fee": 19,
        "follows_courtage_class": True,
    },
    "mini_futures": {
        "name": "Mini Futures",
        "avanza_markets_free": True,
        "avanza_markets_min_order": 1000,
        "other_min_fee": 19,
        "follows_courtage_class": True,
    },
    "index_options": {
        "name": "Index Options (OMXS30)",
        "fee_per_contract": 3.50,
        "clearing_fee_percent": 0.075,  # On exercise
    },
    "stock_options": {
        "name": "Stock Options",
        "percentage": 0.75,
        "min_fee": 1,
        "max_fee": 14,
        "clearing_fee_percent": 0.075,
    },
    "index_futures": {
        "name": "Index Futures",
        "fee_per_contract": 3.50,
        "clearing_fee_percent": 0.075,
    },
    "stock_futures": {
        "name": "Stock Futures",
        "percentage": 0.02,
        "clearing_fee_percent": 0.075,
    },
    "warrants": {
        "name": "Warrants",
        "follows_courtage_class": True,
    },
    "etfs": {
        "name": "ETFs",
        "follows_courtage_class": True,
    },
}


def _calculate_swedish_stock_cost(
    trade_value: float,
    courtage_class: str,
) -> dict:
    """Calculate cost for Swedish stock trade."""
    if courtage_class not in COURTAGE_CLASSES:
        raise ValueError(f"Unknown courtage class: {courtage_class}")

    config = COURTAGE_CLASSES[courtage_class]["swedish_stocks"]

    if courtage_class == "start":
        return {
            "commission": 0,
            "commission_percent": 0,
            "calculation": "Start class: 0 SEK commission",
        }

    if courtage_class == "fast_pris":
        return {
            "commission": 99,
            "commission_percent": (99 / trade_value) * 100 if trade_value > 0 else 0,
            "calculation": "Fast Pris: Fixed 99 SEK",
        }

    min_fee = config["min_fee"]
    percentage = config["percentage"]
    breakpoint = config["breakpoint"]

    if trade_value <= breakpoint:
        commission = min_fee
        calc = f"Trade value {trade_value:.2f} SEK <= breakpoint {breakpoint} SEK: min fee {min_fee} SEK"
    else:
        commission = trade_value * (percentage / 100)
        calc = f"Trade value {trade_value:.2f} SEK > breakpoint {breakpoint} SEK: {percentage}% = {commission:.2f} SEK"

    return {
        "commission": round(commission, 2),
        "commission_percent": (commission / trade_value) * 100 if trade_value > 0 else 0,
        "calculation": calc,
    }


def _calculate_foreign_stock_cost(
    trade_value_local: float,
    market: str,
    include_exchange: bool = True,
) -> dict:
    """Calculate cost for foreign stock trade."""
    if market not in FOREIGN_MARKETS:
        raise ValueError(f"Unknown market: {market}")

    config = FOREIGN_MARKETS[market]
    min_fee = config["min_fee_local"]
    percentage = config["percentage"]
    exchange_spread = config["exchange_spread"]
    currency = config["currency"]

    # Commission
    commission = max(min_fee, trade_value_local * (percentage / 100))

    result = {
        "commission": round(commission, 2),
        "commission_currency": currency,
        "commission_percent": (commission / trade_value_local) * 100 if trade_value_local > 0 else 0,
    }

    # Exchange cost (if applicable)
    if include_exchange:
        exchange_cost = trade_value_local * (exchange_spread / 100)
        result["exchange_cost"] = round(exchange_cost, 2)
        result["exchange_spread_percent"] = exchange_spread
        result["total_cost"] = round(commission + exchange_cost, 2)
        result["total_percent"] = result["commission_percent"] + exchange_spread
        result["calculation"] = (
            f"Commission: max({min_fee} {currency}, {trade_value_local:.2f} × {percentage}%) = {commission:.2f} {currency}. "
            f"Exchange: {trade_value_local:.2f} × {exchange_spread}% = {exchange_cost:.2f} {currency}. "
            f"Total: {result['total_cost']:.2f} {currency}"
        )
    else:
        result["total_cost"] = round(commission, 2)
        result["total_percent"] = result["commission_percent"]
        result["calculation"] = f"Commission: max({min_fee} {currency}, {trade_value_local:.2f} × {percentage}%) = {commission:.2f} {currency}"

    return result


# === MCP Tools ===


@mcp.tool()
async def get_courtage_classes(ctx: Context) -> dict:
    """Get all Avanza courtage (commission) classes with pricing details.

    Returns comprehensive information about all available courtage classes
    including fees, breakpoints, and which class is optimal for different
    trade sizes.

    Returns:
        Dictionary containing:
        - classes: All courtage classes with their pricing rules
        - foreign_markets: Pricing for foreign markets (USA, Europe, etc.)
        - derivatives: Pricing for options, futures, certificates
        - optimal_class_guide: Guide showing best class for different trade sizes

    Examples:
        Get all pricing info:
        >>> get_courtage_classes()
    """
    ctx.info("Fetching Avanza courtage class information")

    # Calculate optimal class for various trade sizes
    trade_sizes = [100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 500000]
    optimal_guide = []

    for size in trade_sizes:
        best_class = None
        best_cost = float("inf")

        for class_key in ["mini", "small", "medium", "fast_pris"]:
            cost_info = _calculate_swedish_stock_cost(size, class_key)
            if cost_info["commission"] < best_cost:
                best_cost = cost_info["commission"]
                best_class = class_key

        optimal_guide.append({
            "trade_value_sek": size,
            "optimal_class": best_class,
            "commission_sek": best_cost,
            "commission_percent": round((best_cost / size) * 100, 3),
        })

    return {
        "classes": COURTAGE_CLASSES,
        "foreign_markets": FOREIGN_MARKETS,
        "derivatives": DERIVATIVES,
        "optimal_class_guide": optimal_guide,
        "notes": {
            "start_eligibility": "Start class requires account value <= 50,000 SEK",
            "class_switching": "You can switch courtage class unlimited times per day",
            "avanza_markets": "Certificates and mini futures are commission-free on Avanza Markets for orders >= 1,000 SEK",
            "exchange_costs": "Foreign trades incur 0.25% exchange spread each way (0.50% round trip). Nordic markets (DKK, NOK) have 0.15% spread.",
        },
        "last_updated": "2026-02",
    }


@mcp.tool()
async def calculate_trade_cost(
    ctx: Context,
    trade_value: float,
    courtage_class: Literal["start", "mini", "small", "medium", "fast_pris"] = "mini",
    market: Literal["sweden", "usa", "canada", "europe_eur", "europe_gbp", "denmark", "norway", "finland"] = "sweden",
    instrument_type: Literal["stock", "etf", "certificate", "warrant", "option", "future"] = "stock",
    is_avanza_markets: bool = False,
    include_exchange_cost: bool = True,
) -> dict:
    """Calculate trading cost for a single trade on Avanza.

    Computes commission, exchange fees (for foreign trades), and total cost
    based on the trade parameters.

    Args:
        ctx: MCP context for logging
        trade_value: Trade value in local currency (SEK for Sweden, USD for USA, etc.)
        courtage_class: Your Avanza courtage class (start, mini, small, medium, fast_pris)
        market: Market to trade on (sweden, usa, canada, europe_eur, europe_gbp, denmark, norway, finland)
        instrument_type: Type of instrument (stock, etf, certificate, warrant, option, future)
        is_avanza_markets: True if trading certificates/mini futures via Avanza Markets (commission-free >= 1000 SEK)
        include_exchange_cost: Include currency exchange cost for foreign trades (default True)

    Returns:
        Cost breakdown including:
        - commission: Brokerage commission
        - exchange_cost: Currency exchange cost (foreign markets only)
        - total_cost: Total trading cost
        - commission_percent: Commission as percentage of trade value
        - calculation: Explanation of how cost was calculated

    Examples:
        Swedish stock trade of 10,000 SEK with Mini class:
        >>> calculate_trade_cost(trade_value=10000, courtage_class="mini", market="sweden")

        US stock trade of 5,000 USD:
        >>> calculate_trade_cost(trade_value=5000, market="usa", include_exchange_cost=True)

        Commission-free certificate via Avanza Markets:
        >>> calculate_trade_cost(trade_value=2000, instrument_type="certificate", is_avanza_markets=True)
    """
    ctx.info(f"Calculating trade cost: {trade_value} in {market}, class={courtage_class}, type={instrument_type}")

    result = {
        "trade_value": trade_value,
        "market": market,
        "courtage_class": courtage_class,
        "instrument_type": instrument_type,
    }

    # Handle Avanza Markets (commission-free certificates/mini futures)
    if is_avanza_markets and instrument_type in ["certificate", "mini_future"]:
        if trade_value >= 1000:
            result["commission"] = 0
            result["total_cost"] = 0
            result["commission_percent"] = 0
            result["calculation"] = "Avanza Markets: Commission-free for orders >= 1,000 SEK"
            ctx.info("Avanza Markets commission-free trade")
            return result

    # Swedish market
    if market == "sweden":
        cost_info = _calculate_swedish_stock_cost(trade_value, courtage_class)
        result.update(cost_info)
        result["currency"] = "SEK"
        result["total_cost"] = cost_info["commission"]

    # Foreign markets
    else:
        cost_info = _calculate_foreign_stock_cost(trade_value, market, include_exchange_cost)
        result.update(cost_info)

    ctx.info(f"Calculated cost: {result.get('total_cost', 0)} {result.get('currency', result.get('commission_currency', 'SEK'))}")
    return result


@mcp.tool()
async def calculate_portfolio_trade_cost(
    ctx: Context,
    trades: str,
    courtage_class: Literal["start", "mini", "small", "medium", "fast_pris"] = "mini",
) -> dict:
    """Calculate total trading cost for multiple trades (portfolio rebalancing).

    Computes the total cost of executing multiple trades, useful for portfolio
    rebalancing, building positions, or estimating transaction costs.

    Args:
        ctx: MCP context for logging
        trades: JSON string of trades, each with: value (required), market (optional, default "sweden"), instrument_type (optional, default "stock")
               Example: '[{"value": 10000}, {"value": 5000, "market": "usa"}, {"value": 2000, "market": "sweden"}]'
        courtage_class: Avanza courtage class to use for all trades

    Returns:
        Portfolio cost breakdown including:
        - trades: Individual trade cost breakdowns
        - summary: Total costs by currency
        - total_trades: Number of trades
        - total_cost_sek_estimate: Estimated total in SEK (foreign currencies converted at approximate rates)

    Examples:
        Calculate cost for 3 Swedish stock trades:
        >>> calculate_portfolio_trade_cost(trades='[{"value": 5000}, {"value": 10000}, {"value": 25000}]', courtage_class="small")

        Mixed portfolio with Swedish and US stocks:
        >>> calculate_portfolio_trade_cost(trades='[{"value": 15000, "market": "sweden"}, {"value": 3000, "market": "usa"}]')
    """
    import json

    ctx.info(f"Calculating portfolio trade costs with courtage class: {courtage_class}")

    try:
        trade_list = json.loads(trades)
    except json.JSONDecodeError as e:
        ctx.error(f"Invalid JSON: {e}")
        return {"error": f"Invalid trades JSON: {e}"}

    if not isinstance(trade_list, list):
        return {"error": "trades must be a JSON array"}

    # Approximate exchange rates for SEK conversion
    exchange_rates = {
        "SEK": 1.0,
        "USD": 10.5,
        "EUR": 11.5,
        "GBP": 13.5,
        "CAD": 7.5,
        "DKK": 1.55,
        "NOK": 1.0,
    }

    results = []
    totals_by_currency = {}
    total_sek_estimate = 0

    for i, trade in enumerate(trade_list):
        if not isinstance(trade, dict) or "value" not in trade:
            results.append({"trade_index": i, "error": "Missing 'value' field"})
            continue

        value = trade["value"]
        market = trade.get("market", "sweden")
        instrument_type = trade.get("instrument_type", "stock")
        is_avanza_markets = trade.get("is_avanza_markets", False)

        # Calculate individual trade cost
        if market == "sweden":
            cost_info = _calculate_swedish_stock_cost(value, courtage_class)
            currency = "SEK"
            total_cost = cost_info["commission"]
        else:
            cost_info = _calculate_foreign_stock_cost(value, market, include_exchange=True)
            currency = FOREIGN_MARKETS.get(market, {}).get("currency", "USD")
            total_cost = cost_info.get("total_cost", cost_info["commission"])

        # Handle Avanza Markets
        if is_avanza_markets and instrument_type in ["certificate", "mini_future"] and value >= 1000:
            total_cost = 0
            cost_info = {"commission": 0, "calculation": "Avanza Markets: Free"}

        results.append({
            "trade_index": i,
            "trade_value": value,
            "market": market,
            "instrument_type": instrument_type,
            "cost": total_cost,
            "currency": currency,
            "details": cost_info,
        })

        # Aggregate by currency
        if currency not in totals_by_currency:
            totals_by_currency[currency] = 0
        totals_by_currency[currency] += total_cost

        # Estimate SEK equivalent
        rate = exchange_rates.get(currency, 1.0)
        total_sek_estimate += total_cost * rate

    ctx.info(f"Calculated costs for {len(results)} trades, estimated total: {total_sek_estimate:.2f} SEK")

    return {
        "trades": results,
        "summary": {
            "total_trades": len(results),
            "costs_by_currency": {k: round(v, 2) for k, v in totals_by_currency.items()},
            "total_cost_sek_estimate": round(total_sek_estimate, 2),
            "note": "SEK estimate uses approximate exchange rates",
        },
        "courtage_class_used": courtage_class,
    }


@mcp.tool()
async def find_optimal_courtage_class(
    ctx: Context,
    trade_value: float,
    market: Literal["sweden", "usa", "canada", "europe_eur", "europe_gbp", "denmark", "norway", "finland"] = "sweden",
) -> dict:
    """Find the optimal courtage class for a given trade size.

    Compares costs across all courtage classes and recommends the cheapest
    option for your trade.

    Args:
        ctx: MCP context for logging
        trade_value: Trade value in local currency
        market: Market to trade on

    Returns:
        Comparison of all courtage classes with:
        - recommended: The optimal courtage class
        - comparison: Cost breakdown for each class
        - savings: How much you save vs the worst option

    Examples:
        Find best class for 15,000 SEK Swedish trade:
        >>> find_optimal_courtage_class(trade_value=15000, market="sweden")
    """
    ctx.info(f"Finding optimal courtage class for {trade_value} trade in {market}")

    if market != "sweden":
        # Foreign markets have fixed pricing regardless of courtage class
        cost_info = _calculate_foreign_stock_cost(trade_value, market, include_exchange=True)
        return {
            "trade_value": trade_value,
            "market": market,
            "note": "Foreign markets have fixed pricing regardless of courtage class",
            "cost": cost_info,
        }

    # Compare all Swedish courtage classes
    comparisons = []
    for class_key in ["start", "mini", "small", "medium", "fast_pris"]:
        cost_info = _calculate_swedish_stock_cost(trade_value, class_key)
        comparisons.append({
            "class": class_key,
            "class_name": COURTAGE_CLASSES[class_key]["name"],
            "commission": cost_info["commission"],
            "commission_percent": round(cost_info["commission_percent"], 4),
            "calculation": cost_info["calculation"],
        })

    # Sort by cost
    comparisons.sort(key=lambda x: x["commission"])
    best = comparisons[0]
    worst = comparisons[-1]

    # Note about Start class eligibility
    notes = []
    if best["class"] == "start":
        notes.append("Start class requires account value <= 50,000 SEK")
        # Also show best non-Start option
        non_start_best = next(c for c in comparisons if c["class"] != "start")
        notes.append(f"Best option if not eligible for Start: {non_start_best['class_name']} ({non_start_best['commission']} SEK)")

    ctx.info(f"Optimal class: {best['class_name']} at {best['commission']} SEK")

    return {
        "trade_value": trade_value,
        "market": market,
        "currency": "SEK",
        "recommended": {
            "class": best["class"],
            "class_name": best["class_name"],
            "commission": best["commission"],
            "commission_percent": best["commission_percent"],
        },
        "comparison": comparisons,
        "savings_vs_worst": round(worst["commission"] - best["commission"], 2),
        "notes": notes if notes else None,
    }
