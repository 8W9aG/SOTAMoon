"""The MNIST benchmark."""
import os
import typing
from pathlib import Path
import os
import logging

import torch
import torchvision
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
import numpy as np

from .benchmark import Benchmark
from .model import Model
from ..fs.provider import Provider


MNIST_BENCHMARK_IDENTIFIER = "mnist"
MNIST_BATCH_SIZE_TEST = 1000
MNIST_MAGNET_URL = "magnet:?xt=urn:btih:ce990b28668abf16480b8b906640a6cd7e3b8b21&tr=http%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969"


class MNISTBenchmark(Benchmark):
    """The class representing an MNIST benchmark."""
    def __init__(self, provider: Provider):
        super().__init__(MNIST_BENCHMARK_IDENTIFIER, provider)

    def download(self) -> None:
        """Downloads the dataset."""
        self.provider.path("", link=MNIST_MAGNET_URL, skip_check=True)
        mnist_folder = os.path.join(self.provider.cache_folder, "mnist")
        raw_folder = os.path.join(mnist_folder, "raw")
        if not os.path.exists(raw_folder):
            files = [x.absolute() for x in Path(mnist_folder).iterdir() if x.is_file()]
            os.makedirs(raw_folder, exist_ok = True)
            for raw_file in files:
                os.symlink(raw_file, os.path.join(raw_folder, os.path.basename(raw_file)))
        self.test_loader = torch.utils.data.DataLoader(
            torchvision.datasets.MNIST(
                self.provider.cache_folder,
                train=False,
                download=True, # This is dumb, we need to set this for processing
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize(
                        (0.1307,), (0.3081,))
                    ])
            ),
            batch_size=MNIST_BATCH_SIZE_TEST,
            shuffle=False)

    def evaluate(self, model: Model) -> float:
        """Evaluate a model against the benchmark."""
        correct = 0
        with torch.no_grad():
            for data, target in self.test_loader:
                pred = np.argmax(model.infer(data), axis=1)
                correct += np.sum(pred == target.numpy())
        return round((float(correct) / float(len(self.test_loader.dataset))) * 100.0, 4)

    def example_data(self) -> np.array:
        """Produce some example data for tracing the models."""
        data, _ = next(iter(self.test_loader))
        return data

    def example_output(self) -> np.array:
        """Produce some example output for comparing the models."""
        _, output = next(iter(self.test_loader))
        return output

    def training_data(self) -> typing.Generator[typing.Tuple[np.array, np.array], None, None]:
        """Produce the data needed for training."""
        train_loader = torch.utils.data.DataLoader(
            torchvision.datasets.MNIST(
                self.provider.cache_folder,
                train=True,
                download=True,
                transform=torchvision.transforms.Compose([
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize((0.1307,), (0.3081,))
                ])
            ),
            batch_size=64,
            shuffle=True)
        for _, (data, target) in enumerate(train_loader):
            yield data, target
