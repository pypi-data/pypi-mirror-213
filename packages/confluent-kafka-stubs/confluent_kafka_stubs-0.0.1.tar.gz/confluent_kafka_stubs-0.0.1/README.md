# confluent-kafka-stubs

This package only contains type hints for the `confluent-kafka` python package. It may be useful to add type checking for `mypy`, or autocompletion in your *language server*.

This package is not endorsed by Confluent.

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
