
class CreateWordPairDto:
    def __init__(
        self,
        key: str,
        value: str,
        set_id: int
    ) -> None:
        self.key: str = key
        self.value: str = value
        self.set_id: int = set_id

class UpdateWordPairDto:
    def __init__(
        self,
        id: int,
        key: str,
        value: str,
        set_id: int,
    ) -> None:
        self.id: int = id
        self.key: str = key
        self.value: str = value
        self.set_id: int = set_id