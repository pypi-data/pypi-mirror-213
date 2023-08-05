from datetime import datetime


class CampaignDTO:
    def __init__(
        self,
        blockchain: str,
        parlamint_id: str,
        collection_id: str,
        name: str,
        description: str,
        price: int,
        supply: int,
        pricing: str,
        limit: int,
        rarity_chart_url: str,
        start_at: datetime,
    ):
        self.blockchain: str = blockchain

        self.parlamint_id: str = parlamint_id.lower()
        self.collection_id: str = collection_id.lower() if collection_id else None

        self.name: str = name
        self.description: str = description
        self.price: int = price
        self.supply: int = supply
        self.pricing: str = pricing.replace("<br>", "\n").strip()
        self.limit: int = limit
        self.rarity_chart_url: str = rarity_chart_url
        self.start_at: datetime = start_at

    @property
    def new(self) -> bool:
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        return self.start_at > now

    @property
    def parlamint_url(self) -> str:
        return f"https://app.book.io/parlamint/campaigns/{self.parlamint_id}"

    def __repr__(self):
        return f"{self.name} ({self.collection_id})"
