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


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


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

    def mine(self, beat_completion: float) -> typing.Tuple[str, float]:
        """Mine a benchmark for a better model."""
        network = Net()
        learning_rate = 0.01
        momentum = 0.5
        optimizer = optim.SGD(network.parameters(), lr=learning_rate, momentum=momentum)
        current_completion = 0.0
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
        while current_completion <= beat_completion:
            network.train()
            for _, (data, target) in enumerate(train_loader):
                optimizer.zero_grad()
                output = network(data)
                loss = F.nll_loss(output, target)
                loss.backward()
                optimizer.step()
            network.eval()
            correct = 0
            with torch.no_grad():
                for data, target in self.test_loader:
                    output = network(data)
                    pred = output.data.max(1, keepdim=True)[1]
                    correct += pred.eq(target.data.view_as(pred)).sum()
            current_completion = round((float(correct) / float(len(self.test_loader.dataset))) * 100.0, 4)
            logging.info(f"Current Completion: {current_completion} To Beat: {beat_completion}")
        model_path_index = 0
        model_path = os.path.join(self.provider.cache_folder, f"model_{model_path_index}.pth")
        while os.path.exists(model_path):
            model_path_index += 1
            model_path = os.path.join(self.provider.cache_folder, f"model_{model_path_index}.pth")
        with torch.no_grad():
            data, _ = next(iter(self.test_loader))
            trace = torch.jit.trace(network, data)
            torch.jit.save(trace, model_path)
        new_model_path = self.provider.copy(model_path)
        os.remove(model_path)
        return new_model_path, current_completion
