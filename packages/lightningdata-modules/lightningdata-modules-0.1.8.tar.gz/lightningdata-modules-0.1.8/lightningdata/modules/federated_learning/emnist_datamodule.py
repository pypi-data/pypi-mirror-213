"""EMNIST DATAMODULE"""
from typing import Callable, Any
import torchvision.datasets
from torchvision import transforms
from lightningdata.modules.federated_learning.federatedLearning_base import FederatedLearningDataModule

class EmnistDataModule(FederatedLearningDataModule):
    def __init__(
            self,
            data_dir: str,
            split: str,
            *args: Any,
            **kwargs: Any
    ) -> None:
        # split = byclass, bymerge, balanced, letters, digits and mnist
        if split is None:
            split = "mnist"
        super().__init__(split=split, *args, **kwargs)

        # fill name and dataset
        self.name = "emnist"
        self.dataset = torchvision.datasets.EMNIST
        # set root data directory
        self.data_dir = data_dir

    def _default_train_transforms(self) -> Callable:
        trans = transforms.ToTensor()
        return trans

    def _default_test_transforms(self) -> Callable:
        trans = transforms.ToTensor()
        return trans
