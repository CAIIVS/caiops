from typing import Callable

import torch
from accelerate import Accelerator
from omegaconf import DictConfig
from torch.nn import Module
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm

from .proto import TrainingProtocol


class MNIST(TrainingProtocol):
    def __init__(self, acc: Accelerator, model: Module, optimizer: Callable[..., Optimizer], loss: _Loss) -> None:
        self.model = acc.prepare_model(model=model)
        self.optimizer = acc.prepare_optimizer(optimizer=optimizer(params=self.model.parameters()))
        self.loss = loss

    def train(self, cfg: DictConfig, acc: Accelerator, dataloader: DataLoader) -> None:
        self.model.train()
        for batch in tqdm(dataloader, desc="Train", leave=False):
            self.optimizer.zero_grad()
            inputs, targets = batch["image"], batch["label"]
            outputs = self.model(inputs)
            loss = self.loss(outputs, targets)
            acc.backward(loss)
            self.optimizer.step()
            acc.log({"train_loss": loss})

    def valid(self, cfg: DictConfig, acc: Accelerator, dataloader: DataLoader) -> None:
        self.model.eval()
        for batch in tqdm(dataloader, desc="Valid", leave=False):
            inputs, targets = batch["image"], batch["label"]
            with torch.no_grad():
                outputs = self.model(inputs)
            loss = self.loss(outputs, targets)
            acc.log({"valid_loss": loss})

    def on_train_end(self, cfg: DictConfig, acc: Accelerator) -> None:
        acc.save_model(self.model, save_directory=acc.project_dir)
