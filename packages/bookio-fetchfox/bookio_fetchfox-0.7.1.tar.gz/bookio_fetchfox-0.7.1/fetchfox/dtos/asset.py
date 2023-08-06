from fetchfox.constants.specials import GHOST_BIBLE


class AssetDTO:
    def __init__(self, collection_id: str, asset_id: str, metadata: dict):
        self.collection_id: str = collection_id
        self.asset_id: str = asset_id
        self.metadata: dict = metadata

    @property
    def title(self) -> str:
        if "Book Title" in self.metadata:
            return self.metadata["Book Title"][0]

        return self.metadata["name"].split(" #")[0]

    @property
    def number(self) -> str:
        try:
            return int(self.metadata["name"].split(" #")[-1])
        except:
            return None

    @property
    def quantity(self) -> int:
        return int(self.metadata.get("quantity", "1"))

    @property
    def cover_theme(self) -> str:
        attributes = self.metadata.get("attributes") or self.metadata.get("properties") or {}

        if not attributes:
            return "none"

        if "Cover Theme" in attributes:
            return attributes["Cover Theme"].split(" / ")[-1]

        if "Edition" in attributes:
            return attributes["Edition"]

        trait_count = 0

        for attribute in attributes.values():
            if isinstance(attribute, str):
                trait_count += 1
            elif isinstance(attribute, list):
                trait_count += len(attribute)

        return f"Traits: {trait_count}"

    @property
    def cover_variation(self) -> str:
        attributes = self.metadata.get("attributes") or self.metadata.get("properties") or {}

        if not attributes:
            return None

        try:
            return int(attributes["Variation"].split(" / ")[-1])
        except:
            return None

    @property
    def special(self) -> str:
        attributes = self.metadata.get("attributes") or self.metadata.get("properties") or {}

        if not attributes:
            return None

        if self.metadata["name"].startswith("Gutenberg Bible"):
            dots = attributes.get("Dots", [])

            if "Dots_Middle" in dots and "Dots_ADA" not in dots:
                return GHOST_BIBLE

        return attributes.get("Special")

    def __repr__(self) -> str:
        return f"{self.title} {self.number} [{self.cover_theme} / {self.cover_variation}]"
