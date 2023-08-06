# apitorch.py

> API Torch client written in python.

**Introduction**

API Torch is a platform that allows you to use, create, and deploy image classifiers.

---

## Getting Started

### Prerequisites

Ensure you register for a free account and have your API key handy. We'll assume your API key is defined at `api_key`.

### Installation

Add to your `requirements.txt` if available:

```
$ echo "apitorch" >> requirements.txt
```

Or install using pip:

```
pip install apitorch
```

### Make your first request

You may test your connection end-to-end, start with a file main.py and add the following code:

```
from apitorch import create_client

api_key = 'YOUR_API_KEY'

client = create_client(api_key)
response = client.ping()
print(f"Got response from API Torch: {response}")
```

Running the code in your terminal `python app.py` should return the string `Got response from API Torch: 1`.

## Documentation

Official API Documentation can be found here:

### Training Sets

#### List training sets

```python
from apitorch import create_client

api_key = 'YOUR_API_KEY'
client = create_client(api_key)

training_sets = client.training_sets.list()
print(training_sets)

# List(...)
```

#### Download training images

```python
from apitorch import create_client

api_key = 'YOUR_API_KEY'
client = create_client(api_key)

training_set_id = 42
training_set = client.training_set.load(training_set_id)
response = training_set.download_images()
print(training_sets)

# Dict(...)
```

#### Add image to training set

> add image

## Development

Use `pyenv` to ensure you install the python version specified in [.python-version](.python-version). 

Install a virtual environemt: `python -v venv venv/`

Activate environment: `source venv/bin/activate`

Install dependencies: `pip install -r requirements-dev.txt`

### Testing

To run unit tests: `pytest`

To skip a test, decorate a function like so:

```
import pytest

@pytest.mark.skip(reason="Not yet implemented")
def test_something():
  # this function will not run
  raise Exception()
```

### Building

Ensure build module is installed: `python -m pip install build`

Build: `python -m build`