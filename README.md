# SOTAMoon

A cryptocurrency whose Proof of Work is solving for the state of the art machine learning benchmarks.

## Raison D'être :thought_balloon:

Machine Learning is a constantly evolving field that can be measured by standardised benchmarks. The progress against those benchmarks is very similar to a Bitcoin inflation curve, where the work becomes harder as more blocks are mined. Unlike Bitcoins use of hashing for Proof of Work, this proposes a system that uses the state of the art benchmark where miners compete to create new machine learning models, and if they beat the current state of the art on a benchmark a new block can be created and verified by the network. This will function as both a cryptocurrency and a network that can produce increasingly better machine learning models for solving real world problems.

## Architecture :triangular_ruler:

`SOTAMoon` has the following key features:

- **Blockchain** Uses the blockchain to create a distributed truth over what the state of the current blockchain is. The proof of work required to write to the blockchain (creating a new model) is significantly bigger than the work required to validate the blockchain (testing inference of models).
- **BitTorrent** In order to decentralise the distribution of the data necessary to validate and mine new blocks, the network uses BitTorrent to download and seed the necessary models and data relevant to inference.
- **Machine Learning** The nodes can use AutoML and other brute force techniques to find better solutions to the current state of the art performance of models.
- **Synthetic Data** Each node generates a private set of synthetic data in order to prevent an overfitted model being submitted to the network.

## Dependencies :globe_with_meridians:

- [pycryptodome](https://github.com/Legrandin/pycryptodome)
- [torch](https://github.com/pytorch/pytorch)
- [torchvision](https://github.com/pytorch/vision)
- [libtorrent](https://www.libtorrent.org/)
- [snappy](http://google.github.io/snappy/)
- [brotli](https://github.com/google/brotli)
- [PyBluez](https://pybluez.github.io/)
- [zeroconf](https://github.com/jstasiak/python-zeroconf)
- [faker](https://pypi.org/project/Faker/)
- [lightblue](https://pypi.org/project/python-lightblue/)

## Installation :inbox_tray:

`SOTAMoon` is a [python](https://www.python.org/) project, to install and run it, it is first recommended to add a virtual environment like so:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

Then perform the installation:

```shell
$ xcode-select --install
$ brew install boost-build boost openssl@1.1 boost-python3
$ cd libraries/libtorrent && python setup.py build && python setup.py install
$ python setup.py install
```

This has only been tested on macOS but should work on Linux or Windows with minor alterations.

## Usage example :eyes:

To run the node, use the following command:

```shell
$ sotamoon
```

## License :memo:

The project is available under the [GPL 2.0 License](LICENSE).
