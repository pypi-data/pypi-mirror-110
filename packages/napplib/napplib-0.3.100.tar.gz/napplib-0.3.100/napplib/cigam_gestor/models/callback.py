class callback:
    id: str
    id_platform: str
    id_integration: str
    type: str

    def __init__(self, id: str, id_platform: str, id_integration: str, type: str) -> None:
        self.id = id
        self.id_platform = id_platform
        self.id_integration = id_integration
        self.type = type
