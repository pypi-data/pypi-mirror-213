"""DOMAIN_NET DATAMODULE"""
from typing import Callable, Any
from lightningdata.common import pre_process as preprocessor
from lightningdata.common.config import LightningDataDefaults
from lightningdata.modules.domain_adaptation.domainAdaptation_base import DomainAdaptationDataModule

DATASET_NAME = "domainNet"
AVAILABLE_DOMAINS = ["infograph", "quickdraw", "real", "sketch", "clipart"]


class DomainNetDataModule(DomainAdaptationDataModule):
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
        self.remoteFolder = LightningDataDefaults.DOMAIN_NET_GOOGLE_DRIVE_SHARED_URL

    @staticmethod
    def get_domain_names():
        return AVAILABLE_DOMAINS

    @staticmethod
    def get_dataset_name():
        return DATASET_NAME

    def _default_train_transforms(self) -> Callable:
        trans = preprocessor.image_train(resize_size=self.resize_size, crop_size=self.crop_size)
        return trans

    def _default_test_transforms(self) -> Callable:
        trans = preprocessor.image_test(resize_size=self.resize_size, crop_size=self.crop_size)
        return trans
