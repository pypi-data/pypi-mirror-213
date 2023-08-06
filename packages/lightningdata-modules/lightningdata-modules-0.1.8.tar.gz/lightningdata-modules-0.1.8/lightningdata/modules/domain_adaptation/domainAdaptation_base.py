"""DOMAIN ADAPTATION BASE"""
import os
import os.path
import py7zr
from pytorch_lightning.utilities.types import TRAIN_DATALOADERS, EVAL_DATALOADERS
from lightningdata.modules.datamodule_base import LightningDataBase
from torch.utils.data import DataLoader, random_split
from lightningdata.common.config import LightningDataDefaults
from lightningdata.common.folder2lmdb import ImageFolderLMDB
from lightningdata.common.utils import gdrive_download_domain_dataset
from typing import Any, Optional
from pathlib import Path


class DomainAdaptationDataModule(LightningDataBase):
    def __init__(self,
                 root: str,  # root dataset path
                 name: str,  # dataset name
                 domain: str,  # domain string
                 resize_size: int = 256,  # resize WxH
                 crop_size: int = 224,  # crop size WxH
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.domain = domain
        self.resize_size = resize_size
        self.crop_size = crop_size
        # set root data directory
        self.data_dir = root
        self.data_dir_domain = os.path.join(root, name, domain)

        # auto-filled
        self.num_classes = 0
        self.classes = []
        self.remoteFolder = None
        self.available_domains = []
        self.pre_split = False

    def get_train_transform(self):
        if self.train_transform:
            print("Using user-defined training data augmentation")
            return self.train_transform
        else:
            print("Using default training data augmentation")
            return self._default_train_transforms()

    def get_test_transform(self):
        if self.test_transform:
            print("Using user-defined test data augmentation")
            return self.test_transform
        else:
            print("Using default test data augmentation")
            return self._default_test_transforms()

    def __prepare_dataset(self, root: str, remote_folder: str, ds_name: str, domain: str, split: bool) -> bool:
        print("Domain " + domain + " available")
        dataset_path = os.path.join(root, ds_name)
        # collect the subsets
        subsets = []
        if split:
            subsets.append((os.path.join(root, ds_name), domain + "_train"))
            subsets.append((os.path.join(root, ds_name), domain + "_test"))
        else:
            subsets.append((os.path.join(root, ds_name), domain))

        # iterate over subsets
        for subset in subsets:
            if not os.path.isfile(os.path.join(subset[0], subset[1], "data.mdb")):
                # create path to dataset if it does not exist
                Path(dataset_path).mkdir(parents=True, exist_ok=True)
                # try to download the domain dataset from google drive
                apiKey = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') if LightningDataDefaults.GOOGLE_DRIVE_API == "" else LightningDataDefaults.GOOGLE_DRIVE_API
                if not gdrive_download_domain_dataset(remote_folder=remote_folder,
                                                      local_dir=subset[0],
                                                      domain=subset[1],
                                                      gdrive_api_key= apiKey):
                    print("Download of dataset " + ds_name + " and domain " + domain + " failed")
                    return False
                else:
                    # unzip 7z file
                    archive_path = os.path.join(subset[0], subset[1], "data.7z")
                    if os.path.isfile(archive_path):
                        print("Extracting " + archive_path)
                        with py7zr.SevenZipFile(archive_path, mode='r') as z:
                            z.extractall(path=os.path.join(subset[0], subset[1]))
                        if not os.path.isfile(os.path.join(subset[0], subset[1], "data.mdb")):
                            print("Could not extract without error")
                            return False
                        else:
                            # remove downloaded 7zip file
                            os.remove(archive_path)
                            print("Download and extract success")
                    else:
                        print("Archive does not exist")
                        return False
        return os.path.exists(os.path.join(subsets[0][0], subsets[0][1]))

    def prepare_data(self) -> None:
        if self.domain in self.available_domains:
            retVal = self.__prepare_dataset(root=self.data_dir,
                                            remote_folder=self.remoteFolder,
                                            ds_name=self.name,
                                            domain=self.domain,
                                            split=self.pre_split)
            if retVal:
                print("Success preparing dataset")
            else:
                print("Failed preparing datasets")
        else:
            print("Domain " + self.domain + " not available in datamodule " + self.name)

    def setup(self, stage: Optional[str] = None) -> None:
        if self.pre_split:
            # pre-splitted dataset handling
            dataset_full = ImageFolderLMDB(db_path=self.data_dir_domain + "_train",
                                           transform=self.get_train_transform())

            # set the number of classes and class names once
            self.num_classes = dataset_full.num_classes()
            self.classes = dataset_full.class_names()

            # split the full set in train and validation
            val_len = int(self.val_split * len(dataset_full))
            train_len = int(len(dataset_full) - val_len)
            self.train_set, self.val_set = random_split(dataset_full, [train_len, val_len])
        else:
            # non pre-splitted dataset handling
            dataset_full = ImageFolderLMDB(db_path=self.data_dir_domain,
                                           transform=self.get_train_transform())

            # set the number of classes and class names once
            self.num_classes = dataset_full.num_classes()
            self.classes = dataset_full.class_names()

            # split the full set in train, test and validation
            val_len = int(self.val_split * len(dataset_full))
            test_len = int(self.test_split * len(dataset_full))
            train_len = int(len(dataset_full) - (val_len + test_len))
            self.train_set, self.val_set, self.test_set = random_split(dataset_full, [train_len, val_len, test_len])

        if self.pre_split:
            self.test_set = ImageFolderLMDB(db_path=self.data_dir_domain + "_test",
                                            transform=self.get_test_transform())

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return DataLoader(dataset=self.train_set,
                          batch_size=self.batch_size,
                          shuffle=self.shuffle,
                          num_workers=self.num_workers,
                          pin_memory=self.pin_memory,
                          collate_fn=self.collate_fn,
                          drop_last=self.drop_last)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(dataset=self.val_set,
                          batch_size=self.batch_size,
                          shuffle=False,
                          num_workers=self.num_workers,
                          pin_memory=self.pin_memory,
                          collate_fn=self.collate_fn,
                          drop_last=self.drop_last)

    def test_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(dataset=self.test_set,
                          batch_size=self.batch_size,
                          shuffle=False,
                          num_workers=self.num_workers,
                          pin_memory=self.pin_memory,
                          collate_fn=self.collate_fn,
                          drop_last=self.drop_last)

    def teardown(self, stage) -> None:
        # clean up after fit or test
        # called on every process in DDP
        print("Teardown")

    def label_to_class(self, label) -> str:
        if label < self.num_classes:
            return self.classes[label]
        return "undefined"