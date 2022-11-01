class BaseConfigException(BaseException):
    pass


class InboundNotFoundException(BaseConfigException):
    def __init__(self, tag, *args: object) -> None:
        self.tag = tag
        super().__init__(*args)

    def __str__(self) -> str:
        return f"inbound not found (tag={self.tag})"


class ProtocolNotSupportedException(BaseConfigException):
    def __init__(self, tag, proto, *args: object) -> None:
        self.tag = tag
        self.proto = proto
        super().__init__(*args)

    def __str__(self) -> str:
        return f"this operation protocol doesn't support {self.proto} protocol in {self.tag} inbound"
