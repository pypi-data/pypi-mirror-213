"""MINI IMAGENET DATAMODULE"""
from typing import Callable, Any, Optional
from lightningdata.thirdparty.torchmeta.datasets.helpers import miniimagenet
from torchvision import transforms
from lightningdata.modules.meta_learning.metaLearning_base import MetaLearningDataModule


class MiniImageNetDataModule(MetaLearningDataModule):
    def __init__(
            self,
            data_dir: str,
            ways=None,
            shots=None,
            test_shots=None,
            meta_split="train",
            *args: Any,
            **kwargs: Any
    ) -> None:

        super().__init__(*args, **kwargs)

        self.ways = ways
        self.shots = shots
        self.test_shots = test_shots
        self.meta_split = meta_split

        # fill name and dataset
        self.name = "mini_imagenet"
        self.dataset = miniimagenet
        # set root data directory
        self.data_dir = data_dir

    def prepare_data(self) -> None:
        # preload train set
        self.dataset(folder=self.data_dir,
                     ways=self.ways,
                     shots=self.shots,
                     test_shots=self.test_shots,
                     meta_split=self.meta_split,
                     download=True,
                     seed=42)

    def setup(self, stage: Optional[str] = None) -> None:
        self.train_set = self.dataset(folder=self.data_dir,
                                      ways=self.ways,
                                      shots=self.shots,
                                      test_shots=self.test_shots,
                                      meta_split=self.meta_split,
                                      download=False,
                                      seed=42)
        MetaLearningDataModule.setup(self, stage)

    def _default_train_transforms(self) -> Callable:
        # default transformations are done in the helper class
        trans = transforms.ToTensor()
        return trans

    def _default_test_transforms(self) -> Callable:
        # default transformations are done in the helper class
        trans = transforms.ToTensor()
        return trans
