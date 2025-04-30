from typing import Any

from .proto import TransformProtocol


class Compose(TransformProtocol):
    """A transform that composes multiple transform objects and chaining them
    together.

    Attributes:
        transforms (list[transforms]): A list of transform objects to be composed.
    """

    def __init__(self, transforms: list[TransformProtocol]):
        self.transforms = transforms

    def __call__(self, input: Any) -> Any:
        for transform in self.transforms:
            input = transform(input)
        return input


class Identity(TransformProtocol):
    """A transform class that returns the input as is, without any
    modifications."""

    def __call__(self, input: Any) -> Any:
        return input


class ExtractDict(TransformProtocol):
    """A transform class that extracts keys from an input dictionary.

    Attributes:
        keys (str | list[str]): The keys to be extracted from the input dictionary.
    """

    def __init__(self, keys: str | list[str]):
        if isinstance(keys, str):
            self.keys = [keys]
        else:
            self.keys = keys

    def __call__(self, input: dict[str, Any]) -> tuple[Any]:
        return tuple(input[key] for key in self.keys)
