import numpy as np
from datasets import load_dataset
from torch.utils.data import DataLoader

from .proto import DatasetProtocol


class MNIST(DatasetProtocol):
    def __init__(self, batch_size=64, valid_split=0.2) -> None:
        self.batch_size = batch_size

        dataset = load_dataset("ylecun/mnist")
        train_valid = dataset["train"].train_test_split(test_size=valid_split)

        def transform(example):
            example["image"] = np.array(example["image"]) / 255.0
            return example

        self.train_data = train_valid["train"].map(transform).with_format("torch")
        self.valid_data = train_valid["test"].map(transform).with_format("torch")
        self.test_data = dataset["test"].map(transform).with_format("torch")

    def get_train_loader(self) -> DataLoader:
        return DataLoader(self.train_data, batch_size=self.batch_size)

    def get_valid_loader(self) -> DataLoader:
        return DataLoader(self.valid_data, batch_size=self.batch_size)

    def get_test_loader(self) -> DataLoader:
        return DataLoader(self.test_data, batch_size=self.batch_size)
