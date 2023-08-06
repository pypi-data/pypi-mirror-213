"""META LEARNING BASE - based on torchmeta from https://arxiv.org/abs/1909.06576 """
from pytorch_lightning.utilities.types import TRAIN_DATALOADERS, EVAL_DATALOADERS
#from lightningdata.thirdparty.torchmeta.transforms import ClassSplitter

from lightningdata.modules.datamodule_base import LightningDataBase
from typing import Any, Optional
from lightningdata.thirdparty.torchmeta.utils.data.dataloader import BatchMetaDataLoader


class MetaLearningDataModule(LightningDataBase):
    def __init__(self,
                 num_classes_per_task=None,
                 dataset_transform=None,
                 target_transform=None,
                 class_augmentations=None,
                 resize_size: int = 28,  # resize WxH
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.num_classes_per_task = num_classes_per_task
        self.dataset_transform = dataset_transform
        self.target_transform = target_transform
        self.class_augmentations = class_augmentations
        self.resize_size = resize_size

        # autofilled by this class
        self.num_classes = 0

        # filled by child class
        self.name = None
        self.dataset = None

    def prepare_data(self) -> None:
        pass

    def setup(self, stage: Optional[str] = None) -> None:
        # set the number of classes and class names
        self.num_classes = self.train_set.dataset.num_classes

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        if self.train_set and len(self.train_set) > 0:
            return BatchMetaDataLoader(dataset=self.train_set,
                                       batch_size=self.batch_size,
                                       shuffle=self.shuffle,
                                       num_workers=self.num_workers,
                                       pin_memory=self.pin_memory,
                                       drop_last=self.drop_last)
        print("Failed to create train loader")
        return None

    def val_dataloader(self) -> EVAL_DATALOADERS:
        if self.train_set and len(self.train_set) > 0:
            return BatchMetaDataLoader(dataset=self.train_set,
                                       batch_size=self.batch_size,
                                       shuffle=False,
                                       num_workers=self.num_workers,
                                       pin_memory=self.pin_memory,
                                       drop_last=self.drop_last)
        print("Failed to create val loader")
        return None

    def test_dataloader(self) -> EVAL_DATALOADERS:
        if self.train_set and len(self.train_set) > 0:
            return BatchMetaDataLoader(dataset=self.train_set,
                                       batch_size=self.batch_size,
                                       shuffle=False,
                                       num_workers=self.num_workers,
                                       pin_memory=self.pin_memory,
                                       drop_last=self.drop_last)
        print("Failed to create test loader")
        return None

    def teardown(self) -> None:
        # clean up after fit or test
        # called on every process in DDP
        print("Teardown")