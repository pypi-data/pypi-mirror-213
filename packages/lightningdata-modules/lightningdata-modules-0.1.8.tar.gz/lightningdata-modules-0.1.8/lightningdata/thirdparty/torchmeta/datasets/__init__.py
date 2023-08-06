from lightningdata.thirdparty.torchmeta.datasets.triplemnist import TripleMNIST
from lightningdata.thirdparty.torchmeta.datasets.doublemnist import DoubleMNIST
from lightningdata.thirdparty.torchmeta.datasets.cub import CUB
from lightningdata.thirdparty.torchmeta.datasets.cifar100 import CIFARFS, FC100
from lightningdata.thirdparty.torchmeta.datasets.miniimagenet import MiniImagenet
from lightningdata.thirdparty.torchmeta.datasets.omniglot import Omniglot
from lightningdata.thirdparty.torchmeta.datasets.tieredimagenet import TieredImagenet
from lightningdata.thirdparty.torchmeta.datasets.tcga import TCGA
from lightningdata.thirdparty.torchmeta.datasets.pascal5i import Pascal5i
from lightningdata.thirdparty.torchmeta.datasets.letter import Letter
from lightningdata.thirdparty.torchmeta.datasets.one_hundred_plants_texture import PlantsTexture
from lightningdata.thirdparty.torchmeta.datasets.one_hundred_plants_shape import PlantsShape
from lightningdata.thirdparty.torchmeta.datasets.one_hundred_plants_margin import PlantsMargin
from lightningdata.thirdparty.torchmeta.datasets.bach import Bach

from lightningdata.thirdparty.torchmeta.datasets import helpers
from lightningdata.thirdparty.torchmeta.datasets import helpers_tabular

__all__ = [
    # image data
    'TCGA',
    'Omniglot',
    'MiniImagenet',
    'TieredImagenet',
    'CIFARFS',
    'FC100',
    'CUB',
    'DoubleMNIST',
    'TripleMNIST',
    'Pascal5i',
    'helpers',
    # tabular data
    'Letter',
    'PlantsTexture',
    'PlantsShape',
    'PlantsMargin',
    'Bach',
    'helpers_tabular'
]
