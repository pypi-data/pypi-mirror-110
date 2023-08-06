# What is this ?

This package provides the following
- `ProjectStore` for MLflow
    - This is a tracking store for the `project://` scheme. It is the same as the `FileStore` in `mlflow` package that can be used in File schema except for the following points.
    - Use uuid instead of "incremental int" when naming new MLflow experiment directory.
        - This makes it possible to store the team's experiments/runs in any code repository.
- A "Serverless" experiment record viewer for use in rich `IPython` environments such as `Jupyter-Notebook` or `Jupyterlab`.


# Usage

## Record your experiments on ProjectStore

```jupyterpython
import mlflow
mlflow.set_tracking_uri('project://./mlruns') # set storage-uri for tracking
experiment_id = mlflow.create_experiment('sample')

with mlflow.start_run(experiment_id=experiment_id) as run:
    mlflow.log_param("p", 1)
    mlflow.log_param("q", 10)
    mlflow.log_param("r", 100)
    mlflow.log_metric('r2', 0.6)
```

## Explore experiments record on your IPython environments

For "rich" `IPython` environments such as `Jupyter-Notebook` or `Jupyterlab`.

```jupyterpython
import flown.api as flown_api
flown_api.list_experiments()
```

For "poor" `IPython` environments such as `Notebook Preview on PyCharm`. 

```jupyterpython
import flown.api as flown_api
flown_api.list_experiments(restricted=True)
```

**Note:** Any interactive function is disabled on this `restricted` mode. Any link does not work.

## Run MLflow Server with ProjectStore

### Using default directory './mlruns' 

```bash
$ flown ui
```

Then you can browse your experiment record via MLflow WEB-UI. ( http://127.0.0.1:5000 )

### Using other directory. 

```bash
$ flown ui --backend-store-uri project://./relational/path/to/dir --default-artifact-root s3://your-bucket/prefix-key
```

Type `flown ui --help` for farther information.



## From your Jupyter-Notebook/Lab

```python code cell

# How to install for development

```bash
$ cd src
$ pip install -e .
```

# License
MIT


# How to register to PyPI / for my private memo :)

1. Update version in `flown/__version__.py`
2. Upload to pypi.

```bash
pip install twine
pip install build
cd src
python -m build 
python -m twine upload --repository pypi dist/*
```
