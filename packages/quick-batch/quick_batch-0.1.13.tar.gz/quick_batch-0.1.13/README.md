[![Python application](https://github.com/jermwatt/quick_batch/actions/workflows/python-app.yml/badge.svg)](https://github.com/jermwatt/quick_batch/actions/workflows/python-app.yml)
[![Upload Python Package](https://github.com/jermwatt/quick_batch/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jermwatt/quick_batch/actions/workflows/python-publish.yml)

# quick_batch

`quick_batch` is an ultra-simple command-line tool for large batch python-driven processing and transformation.  It was designed to be fast to deploy, transparent, and portable.  This allows you to scale any `processor` function that needs to be run over a large set of input data, enabling batch/parallel processing of the input with minimal setup and teardown.


- [quick\_batch](#quick_batch)
- [Getting started](#getting-started)
  - [Usage](#usage)
  - [Scaling](#scaling)
  - [Installation](#installation)
  - [The `processor.py` file](#the-processorpy-file)
- [Why use quick\_batch](#why-use-quick_batch)

# Getting started

All you need to scale batch transformations with `quick_batch` is a

- transformation function(s) in a `processor.py` file
- `Dockerfile` containing a container build appropriate to y our processor
- an optional `requirements.txt` file containing required python modules

Document paths to these objects as well as other parameters in a `config.yaml` config file of the form below.  

Under `processor` you can either define a `dockerfile_path` to your Dockerfile or an `image_name` to a pre-built image to be pulled. 


```yaml
data:
  input_path: /path/to/your/input/data
  output_path: /path/to/your/output/data
  log_path: /path/to/your/log/file

queue:
  feed_rate: <int - number of examples processed per processor instance>
  order_files: <boolean - whether or not to order input files by size>

processor:
  dockerfile_path: /path/to/your/Dockerfile OR
  image_name: <image_name_to_pull>
  requirements_path: /path/to/your/requirements.txt
  processor_path: /path/to/your/processor/processor.py
  num_processors: <int - instances of processor to run in parallel>

```

`quick_batch` will point your `processor.py` at the `input_path` defined in this `config.yaml` and process the files listed in it in parallel at a scale given by your choice of `num_processors`.  

Output will be written to the `output_path` specified in the configuration file.

You can see the `examples` directory for examples of valid configs, processors, requirements, and dockerfiles.


## Usage

To start processing with your `config.yaml` use `quick_batch`'s `config` command at the terminal by typing

```bash
quick_batch config /path/to/your/config.yaml
```

This will start the build and deploy process for processing your data as defined in your `config.yaml`.

## Scaling

Use the `scale` commoand to manually scale the number of processors / containers running your process

```bash
quick_batch scale <num_processors> 
```

Here `<num_processors>` is an integer >= 1.   For example, to scale to 3 parallel processors / containers: `quick_batch scale 3`

## Installation

To install quick_batch, simply use `pip`:

```bash
pip install quick-batch
```

## The `processor.py` file

Create a `processor.py` file with the following basic pattern:

```python
import ...

def processor(todos):
  for file_name in todos.file_paths_to_process:
    # processing code
```

The `todos` object will carry in `feed_rate` number of file names to process in `.file_paths_to_process`.  

Note: the function name `processor` is mandatory.


# Why use quick_batch

quick_batch aims to be

- **dead simple to use:** versus standard cloud service batch transformation services that require significant configuration / service understanding

- **ultra fast setup:** versus setup of heavier orchestration tools like `airflow` or `mlflow`, which may be a hinderance due to time / familiarity / organisational constraints

- **100% portable:** - use quick_batch on any machine, anywhere

- **processor-invariant:** quick_batch works with arbitrary processes, not just machine learning or deep learning tasks.

- **transparent and open source:** quick_batch uses Docker under the hood and only abstracts away the not-so-fun stuff - including instantiation, scaling, and teardown.  you can still monitor your processing using familiar Docker command-line arguments (like `docker service ls`, `docker service logs`, etc.).

