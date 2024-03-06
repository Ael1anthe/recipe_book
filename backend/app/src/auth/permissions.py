class Permission:
    """Base permission class"""

    __match_args__ = "name"
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, obj: object) -> bool:
        match obj:
            case str():
                return obj == self.name
            case Permission():
                return obj.name == self.name
            case _:
                return False
