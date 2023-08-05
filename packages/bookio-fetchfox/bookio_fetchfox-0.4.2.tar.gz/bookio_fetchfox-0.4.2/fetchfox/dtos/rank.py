class RankDTO:
    def __init__(self, collection_id: str, asset_id: str, asset_name: str, rank: int):
        self.collection_id: str = collection_id
        self.asset_id: str = asset_id
        self.asset_name: str = asset_name
        self.rank: int = rank

    def __repr__(self) -> str:
        return f"{self.collection_id}/{self.asset_id} : #{self.rank}"
