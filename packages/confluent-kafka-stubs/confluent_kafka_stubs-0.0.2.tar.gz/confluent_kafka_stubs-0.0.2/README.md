# confluent-kafka-stubs

This package only contains type hints for the `confluent-kafka` python package. It may be useful to add type checking for `mypy`, or autocompletion in your *language server*.

This package is not endorsed by Confluent.

## Installation

The package can be installed from [PyPI](https://pypi.org/project/confluent-kafka-stubs/), and needs to be installed in a location that tools like `mypy` can access. In my experience, installing it as a user package works well, at least with `neovim` and the official `mypy` package on `Arch Linux`. You can install it as a user package as follows:

```bash
pip install --user confluent-kafka-stubs
```

## Status

This package should be considered a work in progress.

In the `cimpl` module, I believe all constants have been ported along with the following classes or functions:

- `KafkaError`: class
- `KafkaException`: class
- `Message`: class
- `NewPartitions`: class
- `NewTopic`: class
- `TopicPartition`: class
- `Producer`: class
- `Consumer`: class
- `libversion()`: function
- `version()`: function

Yet to be implemented in the `cimpl` module:

- `_AdminClientImpl`?: class

----

**Note**: unlisted modules have not yet been processed.
