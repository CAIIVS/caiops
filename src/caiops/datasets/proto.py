from typing import Protocol, runtime_checkable

from torch.utils.data import DataLoader


@runtime_checkable
class DatasetProtocol(Protocol):
    def get_train_loader(self) -> DataLoader: ...
    def get_valid_loader(self) -> DataLoader: ...
    def get_test_loader(self) -> DataLoader: ...
