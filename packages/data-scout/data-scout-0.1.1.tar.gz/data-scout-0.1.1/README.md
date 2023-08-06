# Data Scout
This package provides the tools to quickly setup a scalable and readable data preparation pipeline that can be run on different platforms. Currently only vanilla Python is available, but PySpark should be available soon. There is also a user interface available here: [Data Scout server](https://github.com/janthiemen/data_scout_server) that allows you to create data pipelines in a visual editor and then export them as either a JSON file, or just plain old simple Python that can be used anywhere.


## Installation

The easiest and quickest way to install Data Scout is through PyPi, just execute the following command:

```bash
pip install data-scout
```

## Executing a JSON pipeline

Pipeline definitions can be given as JSON files or directly as Python commands. To execute a JSON definition, your code would look somewhat as follows:

```python
from data_scout.executor import PandasExecutor
from data_scout.scout import Scout

scout = Scout()
executor = PandasExecutor({"source": "CSV", "kwargs": {
    "filename": "test.csv",
    "delimiter": ",",
    "encoding": "utf-8",
    "has_header": True
}}, [{"transformation": "data-convert", "kwargs": {"field": "column1", "to": "int"}}], scout)
executor()
```

This will load a CSV file and convert the column named "column1" to an integer using Pandas as a backend.

## Development

For development purposes, install the package using the following command:

```bash
pip install -e .[dev]
```

### Testing

There are some unit tests available. The unit tests are written using the Nose2 framework. The setup.py script should have already installed Nose2, so now you may run the tests as follows:

```bash
nose2 -v
```
