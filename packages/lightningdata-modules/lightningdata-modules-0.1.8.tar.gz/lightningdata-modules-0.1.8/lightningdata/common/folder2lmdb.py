import os
import six
import argparse
import lmdb
from PIL import Image
import torch.utils.data as data
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms
import pickle

""" Source: https://github.com/rmccorm4/PyTorch-LMDB """


class ImageFolderLMDB(data.Dataset):
    def __init__(self, db_path, transform=transforms.ToTensor(), target_transform=None):
        self.db_path = db_path
        self.transform = transform
        self.target_transform = target_transform
        # attributes that are lazy-loaded
        self.classes = []
        self.num_class = 0

        env = lmdb.open(self.db_path, subdir=os.path.isdir(self.db_path),
                        readonly=True, lock=False,
                        readahead=False, meminit=False)
        with env.begin(write=False) as txn:
            self.length = pickle.loads(txn.get(b'__len__'))
            self.keys = pickle.loads(txn.get(b'__keys__'))
            self.classes = pickle.loads(txn.get(b'__classes__'))
            self.num_class = pickle.loads(txn.get(b'__num_classes__'))

    def open_lmdb(self):
        self.env = lmdb.open(self.db_path, subdir=os.path.isdir(self.db_path),
                             readonly=True, lock=False,
                             readahead=False, meminit=False)
        self.txn = self.env.begin(write=False, buffers=True)

    def __getitem__(self, index):
        if not hasattr(self, 'txn'):
            self.open_lmdb()

        img, target = None, None
        byteflow = self.txn.get(self.keys[index])
        unpacked = pickle.loads(byteflow)

        # load image
        if type(unpacked[0]) is tuple:
            imgbuf = unpacked[0][0]
        else:
            imgbuf = unpacked[0]
        buf = six.BytesIO()
        buf.write(imgbuf)
        buf.seek(0)
        img = Image.open(buf)

        # load label
        target = unpacked[1]

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        return self.length

    def __repr__(self):
        return self.__class__.__name__ + ' (' + self.db_path + ')'

    def num_classes(self):
        return self.num_class

    def class_names(self):
        return self.classes

    def label_to_class(self, label):
        if label < self.num_class:
            return self.classes[label]
        return "undefined"


def raw_reader(path):
    with open(path, 'rb') as f:
        bin_data = f.read()
    return bin_data


def dumps_pickle(obj):
    """
    Serialize an object.

    Returns :
        The pickled representation of the object obj as a bytes object
    """
    return pickle.dumps(obj)


def folder2lmdb(path, outpath, map_size=1024000, num_workers=0, write_frequency=100):
    directory = os.path.expanduser(path)
    print("Loading dataset from %s" % directory)
    dataset = ImageFolder(directory, loader=raw_reader)
    data_loader = DataLoader(dataset, num_workers=num_workers)

    lmdb_path = os.path.expanduser(outpath)
    isdir = os.path.isdir(lmdb_path)

    print("Generate LMDB to %s" % lmdb_path)
    db = lmdb.open(lmdb_path, subdir=isdir, readonly=False,
                   meminit=False, map_async=True, map_size=int(map_size))

    print(len(dataset), len(data_loader))
    txn = db.begin(write=True)
    for idx, (data_img, label) in enumerate(data_loader):
        image = data_img
        label = label.numpy()
        txn.put(u'{}'.format(idx).encode('ascii'), dumps_pickle((image, label)))
        if idx % write_frequency == 0:
            print("[%d/%d]" % (idx, len(data_loader)))
            txn.commit()
            txn = db.begin(write=True)

    # finish iterating through dataset
    txn.commit()
    keys = [u'{}'.format(k).encode('ascii') for k in range(idx + 1)]
    classes = [u'{}'.format(cls).encode('ascii') for cls in dataset.classes]
    with db.begin(write=True) as txn:
        txn.put(b'__keys__', dumps_pickle(keys))
        txn.put(b'__len__', dumps_pickle(len(keys)))
        txn.put(b'__classes__', dumps_pickle(classes))
        txn.put(b'__num_classes__', dumps_pickle(len(classes)))

    print("Flushing database ...")
    db.sync()
    db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help="Path to original image dataset folder")
    parser.add_argument("-o", "--outpath", help="Path to output LMDB file")
    parser.add_argument("-m", "--map_size", help="Physically allocated file size in kB")
    parser.add_argument("-w", "--num_workers", help="Number of workers")
    args = parser.parse_args()
    folder2lmdb(args.dataset, args.outpath, args.map_size, int(args.num_workers))
