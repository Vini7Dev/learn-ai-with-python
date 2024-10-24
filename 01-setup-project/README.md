# Virtual Environment

1. Create and activate the Virtual Environment

```shell
# Create a Virtual Environment:

python -m venv venv

python -m venv {{venv-name}}

# Active the environment
### Just place the folder dir below

venv\Scripts\activate

{{venv-name}}\Scripts\activate
```

# Solving importation errors with "\__init__.py"

1. Create a file in the root project nammed "\__init__.py"

2. Install "setuptools" lib

```shell
pip install setuptools
```

3. Create a file in the root project nammed "setup.py" and fill with below content

```py
from setuptools import setup, find_packages

setup(
    name="MyProject",
    packages=find_packages()
)
```

4. Install the packages

```shell
pip install -e {{setup-file-dir}}

pip install -e .
```

# Project Dependencies

1. Create a file **"requirements.txt"**

2. Fill the **"requirements.txt"** with project packages

```txt
numpy==1.2.3
pandas==1.2.3
```

3. Install dependencies

```shell
pip install -r requirements.txt
```
