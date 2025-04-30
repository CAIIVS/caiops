from os import environ

import hydra
from accelerate.accelerator import Accelerator
from hydra.utils import instantiate
from omegaconf import DictConfig
from tqdm import tqdm

from caiops.datasets.proto import DatasetProtocol
from caiops.trainings.proto import TrainingProtocol
from caiops.util import has_method


@hydra.main(version_base=None, config_path=environ["CONF_DIR"], config_name="config")
def main(cfg: DictConfig) -> None:
    # ------------------------------
    # instantiate objects
    # ------------------------------
    acc: Accelerator = instantiate(
        cfg.accelerate,
        project_dir=hydra.core.hydra_config.HydraConfig.get().runtime.output_dir,
    )
    acc.init_trackers(project_name=cfg.project)

    dataset: DatasetProtocol = instantiate(cfg.dataset)
    dataloader_train = acc.prepare(dataset.get_train_loader())
    dataloader_valid = acc.prepare(dataset.get_valid_loader())
    dataloader_test = acc.prepare(dataset.get_test_loader())

    training: TrainingProtocol = instantiate(cfg.training, acc=acc)

    # ------------------------------
    # training loop
    # ------------------------------
    for _ in tqdm(range(cfg.num_epochs), desc="Epoch", leave=True):
        if has_method(training, "train") and dataloader_train:
            training.train(cfg=cfg, acc=acc, dataloader=dataloader_train)
        if has_method(training, "valid") and dataloader_valid:
            training.valid(cfg=cfg, acc=acc, dataloader=dataloader_valid)

    # test
    if has_method(training, "test") and dataloader_test:
        training.test(cfg=cfg, acc=acc, dataloader=dataloader_valid)

    # cleanup
    if has_method(training, "on_train_end"):
        training.on_train_end(cfg=cfg, acc=acc)
    acc.end_training()
