"""DIGIT5 DATAMODULE"""
from typing import Any, Callable
from torchvision.transforms import transforms
from lightningdata.common.config import LightningDataDefaults
from lightningdata.modules.domain_adaptation.domainAdaptation_base import DomainAdaptationDataModule

DATASET_NAME = "digit5"
AVAILABLE_DOMAINS = ["mnist", "mnistm", "svhn", "syn", "usps"]


class Digit5DataModule(DomainAdaptationDataModule):
    def __init__(
            self,
            data_dir: str,
            domain: str,
            *args: Any,
            **kwargs: Any
    ) -> None:
        super().__init__(root=data_dir, name=DATASET_NAME, domain=domain, *args, **kwargs)
        self.available_domains = AVAILABLE_DOMAINS
        # set remote dataset url
        self.remoteFolder = LightningDataDefaults.DIGIT5_GOOGLE_DRIVE_SHARED_URL
        # indicate that the dataset has pre-splitted train/test datasets
        self.pre_split = True

    @staticmethod
    def get_domain_names():
        return AVAILABLE_DOMAINS

    @staticmethod
    def get_dataset_name():
        return DATASET_NAME

    def _default_train_transforms(self) -> Callable:
        trans = transforms.ToTensor()
        return trans

    def _default_test_transforms(self) -> Callable:
        trans = transforms.ToTensor()
        return trans



