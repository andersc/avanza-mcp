"""Models for various instrument types - Indices, ETFs, Certificates, Warrants, etc."""

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


# Standard model config for all models
MODEL_CONFIG = ConfigDict(
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    extra="allow",  # Don't fail on extra fields from API
)


# === Index Models ===


class IndexQuote(BaseModel):
    """Index quote data."""

    model_config = MODEL_CONFIG

    last: float | None = None
    change: float | None = None
    changePercent: float | None = None
    highest: float | None = None
    lowest: float | None = None
    totalValueTraded: float | None = None
    updated: int | None = None


class IndexInfo(BaseModel):
    """Index information from Avanza."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str
    isin: str | None = None
    instrumentId: str | None = None
    currency: str | None = None
    flagCode: str | None = None
    tradable: str | None = None  # String like "BUYABLE_AND_SELLABLE"
    quote: IndexQuote | None = None
    changeOneWeek: float | None = None
    changeOneMonth: float | None = None
    changeThreeMonths: float | None = None
    changeSixMonths: float | None = None
    changeOneYear: float | None = None
    changeThreeYears: float | None = None
    changeFiveYears: float | None = None
    changeThisYear: float | None = None
    highestPrice: float | None = None
    lowestPrice: float | None = None
    numberOfPriceAlerts: int | None = None
    pushPermitted: bool | None = None


# === ETF Models ===


class ETFHolding(BaseModel):
    """Single holding in an ETF."""

    model_config = MODEL_CONFIG

    name: str | None = None
    weight: float | None = None
    countryCode: str | None = None
    isin: str | None = None
    orderbookId: str | None = None


class ETFInfo(BaseModel):
    """ETF information from Avanza."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str
    isin: str | None = None
    instrumentId: str | None = None
    currency: str | None = None
    flagCode: str | None = None
    tradable: str | None = None  # String like "BUYABLE_AND_SELLABLE"
    shortName: str | None = None
    tickerSymbol: str | None = None
    # Quote data
    lastPrice: float | None = None
    change: float | None = None
    changePercent: float | None = None
    highestPrice: float | None = None
    lowestPrice: float | None = None
    totalValueTraded: float | None = None
    totalVolumeTraded: int | None = None
    # Performance
    changeOneWeek: float | None = None
    changeOneMonth: float | None = None
    changeThreeMonths: float | None = None
    changeSixMonths: float | None = None
    changeOneYear: float | None = None
    changeThreeYears: float | None = None
    changeFiveYears: float | None = None
    changeThisYear: float | None = None
    # ETF specific
    nav: float | None = None
    managementFee: float | None = None
    totalExpenseRatio: float | None = None
    trackingError: float | None = None
    underlyingIndex: str | None = None
    fundCompany: str | None = None
    prospectusLink: str | None = None
    productType: str | None = None
    # Market info
    marketPlaceName: str | None = None
    countryCode: str | None = None
    numberOfPriceAlerts: int | None = None
    pushPermitted: bool | None = None


class ETFDetails(BaseModel):
    """Detailed ETF information including holdings."""

    model_config = MODEL_CONFIG

    orderbookId: str | None = None
    name: str | None = None
    isin: str | None = None
    description: str | None = None
    fundCompany: str | None = None
    managementFee: float | None = None
    totalExpenseRatio: float | None = None
    nav: float | None = None
    trackingError: float | None = None
    underlyingIndex: str | None = None
    replicationMethod: str | None = None
    distributionPolicy: str | None = None
    inceptionDate: str | None = None
    domicile: str | None = None
    holdings: list[ETFHolding] = []
    countryAllocation: list[dict] | None = None
    sectorAllocation: list[dict] | None = None


# === Certificate Models ===


class CertificateInfo(BaseModel):
    """Certificate/structured product information."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str
    isin: str | None = None
    instrumentId: str | None = None
    currency: str | None = None
    flagCode: str | None = None
    tradable: str | None = None  # String like "BUYABLE_AND_SELLABLE"
    shortName: str | None = None
    tickerSymbol: str | None = None
    # Quote data
    lastPrice: float | None = None
    change: float | None = None
    changePercent: float | None = None
    highestPrice: float | None = None
    lowestPrice: float | None = None
    buyPrice: float | None = None
    sellPrice: float | None = None
    spread: float | None = None
    spreadPercent: float | None = None
    totalValueTraded: float | None = None
    totalVolumeTraded: int | None = None
    # Certificate specific
    leverage: float | None = None
    direction: str | None = None  # LONG/SHORT
    underlyingName: str | None = None
    underlyingOrderbookId: str | None = None
    underlyingCurrency: str | None = None
    strikePrice: float | None = None
    barrierLevel: float | None = None
    knockOutLevel: float | None = None
    endDate: str | None = None
    issuer: str | None = None
    productType: str | None = None
    # Market info
    marketPlaceName: str | None = None
    countryCode: str | None = None
    numberOfPriceAlerts: int | None = None
    pushPermitted: bool | None = None


# === Warrant Models ===


class WarrantInfo(BaseModel):
    """Warrant information including greeks."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str
    isin: str | None = None
    instrumentId: str | None = None
    currency: str | None = None
    flagCode: str | None = None
    tradable: str | None = None  # String like "BUYABLE_AND_SELLABLE"
    shortName: str | None = None
    tickerSymbol: str | None = None
    # Quote data
    lastPrice: float | None = None
    change: float | None = None
    changePercent: float | None = None
    highestPrice: float | None = None
    lowestPrice: float | None = None
    buyPrice: float | None = None
    sellPrice: float | None = None
    spread: float | None = None
    spreadPercent: float | None = None
    totalValueTraded: float | None = None
    totalVolumeTraded: int | None = None
    # Warrant specific
    warrantType: str | None = None  # CALL/PUT
    strikePrice: float | None = None
    endDate: str | None = None
    expirationDate: str | None = None
    multiplier: float | None = None
    parity: float | None = None
    underlyingName: str | None = None
    underlyingOrderbookId: str | None = None
    underlyingCurrency: str | None = None
    underlyingPrice: float | None = None
    issuer: str | None = None
    # Greeks
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    rho: float | None = None
    impliedVolatility: float | None = None
    intrinsicValue: float | None = None
    timeValue: float | None = None
    theoreticalValue: float | None = None
    # Market info
    marketPlaceName: str | None = None
    countryCode: str | None = None
    numberOfPriceAlerts: int | None = None
    pushPermitted: bool | None = None


# === Bond Models ===


class BondInfo(BaseModel):
    """Bond information."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str
    isin: str | None = None
    instrumentId: str | None = None
    currency: str | None = None
    flagCode: str | None = None
    tradable: str | None = None  # String like "BUYABLE_AND_SELLABLE"
    shortName: str | None = None
    # Quote data
    lastPrice: float | None = None
    change: float | None = None
    changePercent: float | None = None
    highestPrice: float | None = None
    lowestPrice: float | None = None
    buyPrice: float | None = None
    sellPrice: float | None = None
    # Bond specific
    couponRate: float | None = None
    couponFrequency: str | None = None
    maturityDate: str | None = None
    issueDate: str | None = None
    yieldToMaturity: float | None = None
    duration: float | None = None
    modifiedDuration: float | None = None
    accruedInterest: float | None = None
    faceValue: float | None = None
    creditRating: str | None = None
    issuer: str | None = None
    # Market info
    marketPlaceName: str | None = None
    countryCode: str | None = None


# === Option Models ===


class OptionInfo(BaseModel):
    """Option information."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str
    isin: str | None = None
    instrumentId: str | None = None
    currency: str | None = None
    tradable: str | None = None  # String like "BUYABLE_AND_SELLABLE"
    shortName: str | None = None
    # Quote data
    lastPrice: float | None = None
    change: float | None = None
    changePercent: float | None = None
    buyPrice: float | None = None
    sellPrice: float | None = None
    # Option specific
    optionType: str | None = None  # CALL/PUT
    strikePrice: float | None = None
    expirationDate: str | None = None
    multiplier: float | None = None
    underlyingName: str | None = None
    underlyingOrderbookId: str | None = None
    underlyingPrice: float | None = None
    # Greeks
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    rho: float | None = None
    impliedVolatility: float | None = None
    intrinsicValue: float | None = None
    timeValue: float | None = None
    openInterest: int | None = None


# === News Models ===


class NewsItem(BaseModel):
    """Single news item."""

    model_config = MODEL_CONFIG

    newsId: str | None = Field(None, alias="id")
    title: str | None = Field(None, alias="headline")
    timestamp: int | str | None = Field(None, alias="timePublishedMillis")
    publishedDate: str | None = Field(None, alias="timePublished")
    source: str | None = Field(None, alias="newsSource")
    vignette: str | None = None
    articleType: str | None = None
    category: str | None = None
    body: str | None = None
    summary: str | None = Field(None, alias="intro")
    url: str | None = Field(None, alias="fullArticleLink")
    imageUrl: str | None = None
    externalLink: bool | None = None
    instrumentIds: list[str] = []
    tickers: list[str] = []
    isSponsored: bool | None = None
    type: str | None = None


class NewsResponse(BaseModel):
    """News response from Avanza."""

    model_config = MODEL_CONFIG

    news: list[NewsItem] = []
    total: int | None = None
    hasMore: bool | None = None


# === Forum/Social Models ===


class ForumPost(BaseModel):
    """Forum post about an instrument."""

    model_config = MODEL_CONFIG

    postId: str | None = Field(None, alias="id")
    title: str | None = None
    body: str | None = Field(None, alias="content")
    author: str | None = None
    authorId: str | None = None
    timestamp: int | str | None = None
    createdAt: str | None = None
    numberOfComments: int | None = Field(None, alias="replies")
    numberOfLikes: int | None = Field(None, alias="likes")
    url: str | None = None
    isPinned: bool | None = None


class ForumResponse(BaseModel):
    """Forum response from Avanza."""

    model_config = MODEL_CONFIG

    posts: list[ForumPost] = []
    total: int | None = None


# === Batch Quote Models ===


class BatchQuoteItem(BaseModel):
    """Quote data for batch requests."""

    model_config = MODEL_CONFIG

    orderbookId: str
    name: str | None = None
    lastPrice: float | None = None
    change: float | None = None
    changePercent: float | None = None
    buyPrice: float | None = None
    sellPrice: float | None = None
    highestPrice: float | None = None
    lowestPrice: float | None = None
    totalVolumeTraded: int | None = None
    totalValueTraded: float | None = None
    currency: str | None = None
    updated: int | None = None
