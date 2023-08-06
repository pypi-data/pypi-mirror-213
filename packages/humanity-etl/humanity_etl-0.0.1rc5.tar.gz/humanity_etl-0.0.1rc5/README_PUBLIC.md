# `humanity_etl`

> Replicate data from humanity in databricks

[![pypi](https://img.shields.io/pypi/v/humanity_etl?style=for-the-badge)](https://pypi.org/project/humanity_etl/)

## Usage

### CLI

```bash
python -m humanity_etl --table <table-name>
```

where table-name is one of the following: `timeclocks` or `ALL`.

### API

```python
from humanity_etl.tables.timeclocks import timeclocks

timeclocks()
```

Further configs are set via environment variables:

Further configs are set via environment variables:

- `*_ACCESS_TOKEN`: API access
- `APP_ENV`: <development/production> - debug mode
- `SAMPLE_OUTPUT`: <True/False> - Save dataframes to csv

## DEV

### Create venv

```bash
python -m venv env
```

### Activate venv

- unix

```bash
source env/bin/activate
```

- windows

```bash
env\Scripts\activate.bat
```

### Install Packages

```bash
pip install -r requirements.txt
```

## Test

```bash
make test
```

## Format

```bash
make format
```

```bash
make lint
```
