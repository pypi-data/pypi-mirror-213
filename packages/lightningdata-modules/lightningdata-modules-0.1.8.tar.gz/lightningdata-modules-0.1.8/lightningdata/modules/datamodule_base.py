"""LightningDataBase"""
from typing import Any, Callable
from pytorch_lightning import LightningDataModule
from pytorch_lightning.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS


class LightningDataBase(LightningDataModule):
    def __init__(self,
                 val_split: float = 0.1,  # validation split
                 test_split: float = 0.2,  # test split
                 num_workers: int = 0,  # number of workers
                 batch_size: int = 32,  # batch size
                 shuffle: bool = True,  # shuffle training dataset
                 pin_memory: bool = True,  # pin mem
                 drop_last: bool = False,  # drop last (incomplete) batch
                 collate_fn: Callable = None,
                 train_transform_fn: Callable = None,
                 test_transform_fn: Callable = None,
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super(LightningDataBase, self).__init__(*args, **kwargs)
        self.drop_last = drop_last
        self.pin_memory = pin_memory
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.collate_fn = collate_fn
        self.test_split = test_split
        self.val_split = val_split

        self.train_set = None
        self.test_set = None
        self.val_set = None

        self.train_transform = train_transform_fn
        self.test_transform = test_transform_fn

    def get_test_transform(self):
        return self.test_transform

    def get_train_transform(self):
        return self.train_transform

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        print(self.__class__.__name__ + ": train_dataloader not implemented")
        pass

    def test_dataloader(self) -> EVAL_DATALOADERS:
        print(self.__class__.__name__ + ": test_dataloader not implemented")
        pass

    def val_dataloader(self) -> EVAL_DATALOADERS:
        print(self.__class__.__name__ + ": val_dataloader not implemented")
        pass

    def predict_dataloader(self) -> EVAL_DATALOADERS:
        print(self.__class__.__name__ + ": predict_dataloader not implemented")
        pass
