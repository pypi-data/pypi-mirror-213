"""FEDERATED LEARNING BASE"""
from pytorch_lightning.utilities.types import TRAIN_DATALOADERS, EVAL_DATALOADERS
from lightningdata.modules.datamodule_base import LightningDataBase
from typing import Any, Optional
from torch.utils.data import DataLoader


class FederatedLearningDataModule(LightningDataBase):
    def __init__(self,
                 split: str,
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)
        # dataset split type
        self.split = split

        # auto-filled
        self.num_classes = 0
        self.classes = []
        self.name = None
        self.dataset = None

    def prepare_data(self) -> None:
        # preload train and test dataset
        self.dataset(root=self.data_dir,
                     train=True,
                     split=self.split,
                     download=True)
        self.dataset(root=self.data_dir,
                     train=False,
                     split=self.split,
                     download=True)

    def setup(self, stage: Optional[str] = None) -> None:
        # assign prepared datasets
        self.train_set = self.dataset(root=self.data_dir,
                                      split=self.split,
                                      train=True,
                                      download=False,
                                      transform=self._default_train_transforms())
        self.test_set = self.dataset(root=self.data_dir,
                                     split=self.split,
                                     train=False,
                                     download=False,
                                     transform=self._default_test_transforms())
        # set the number of classes and class names
        self.num_classes = len(self.train_set.classes)
        self.classes = self.train_set.classes

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        if self.train_set and len(self.train_set) > 0:
            return DataLoader(dataset=self.train_set,
                              batch_size=self.batch_size,
                              shuffle=self.shuffle,
                              num_workers=self.num_workers,
                              pin_memory=self.pin_memory,
                              collate_fn=self.collate_fn,
                              drop_last=self.drop_last)

        print("Failed to create train loader")
        return None

    def val_dataloader(self) -> EVAL_DATALOADERS:
        if self.val_set and len(self.val_set) > 0:
            return DataLoader(dataset=self.val_set,
                              batch_size=self.batch_size,
                              shuffle=False,
                              num_workers=self.num_workers,
                              pin_memory=self.pin_memory,
                              collate_fn=self.collate_fn,
                              drop_last=self.drop_last)
        print("Failed to create val loader")
        return None

    def test_dataloader(self) -> EVAL_DATALOADERS:
        if self.test_set and len(self.test_set) > 0:
            return DataLoader(dataset=self.test_set,
                              batch_size=self.batch_size,
                              shuffle=False,
                              num_workers=self.num_workers,
                              pin_memory=self.pin_memory,
                              collate_fn=self.collate_fn,
                              drop_last=self.drop_last)
        print("Failed to create test loader")
        return None

    def teardown(self) -> None:
        # clean up after fit or test
        # called on every process in DDP
        print("Teardown")

    def label_to_class(self, label) -> str:
        if label < self.num_classes:
            return self.classes[label]
        return "undefined"

