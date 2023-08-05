# What is this ?

This package provides the following
- `ProjectStore` for MLflow
    - This is a tracking store for the `project://` scheme. It is the same as the `FileStore` in `mlflow` package that can be used in File schema except for the following points.
    - Use uuid instead of "incremental int" when naming new MLflow experiment directory.
        - This makes it possible to store the team's experiments/runs in any code repository.
- A "Serverless" experiment record viewer for use in rich `IPython` environments such as `Jupyter-Notebook` or `Jupyterlab`.


# Usage

## From your Jupyter-Notebook/Lab

```python code cell

# How to install for development

```bash
$ cd src
$ pip install -e .
```

## License
MIT


## memo

```bash
pip install twine
pip install build
cd src
python -m build 
python -m twine upload --repository pypi dist/*
python -m twine upload --repository testpypi dist/*
```
