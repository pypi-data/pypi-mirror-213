  ![Alt text](LightningData_logo.PNG?raw=true "Interface")
# LightningData Modules


Pre-packages Pytorch-Lightning datasets.

## Installation

To install this library, simply run the following command:

```sh
pip install lightingdata_modules
```

**Installing the LightningData Modules should automatically install suitable dependencies.**



## Customized Dataset Support
LightningData Modules downloads, installs and prepares customized Pytorch Lightning datamodules with just one line of code.

Example from Domain Adaptation (DomainNet):

```
# import the custom DomainNet module
import lightningdata_modules.domain_adaptation.domainNet_datamodule as domainNet

# initialize the data module with the "real" domain from DomainNet
my_data_module = domainNet.DomainNetDataModule(data_dir="./dataset/", domain="real")

```

The data module can now be passed to the Pytorch Lighting Trainer instance or be used as a standalone
Dataloader:
```
# check if the dataset already exists in the data_dir, download domain-specific lmdb database from cloud storage otherwise
my_data_module.prepare_data()

# initialize the train and test set according to setup properties
my_data_module.setup()

# create the train DataLoader on-the-fly
train_loader = my_data_module.train_dataloader()

```

### List of Available Datasets

| Domain Adaptation | Federated Learning | Meta Learning |
|-------------------|--------------------|---------------|
| DomainNet         | EMNIST             | Omiglot       |
| Office31          |        | Mini Imagenet |
| OfficeHome        |        ||
| Digit-Five        |        ||

### Class Diagram
![Alt text](diag.png?raw=true "Interface")


## Ack
Thanks to TorchMeta: https://github.com/tristandeleu/pytorch-meta