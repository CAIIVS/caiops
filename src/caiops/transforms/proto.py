from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TransformProtocol(Protocol):
    def __call__(self, input: Any) -> Any: ...
