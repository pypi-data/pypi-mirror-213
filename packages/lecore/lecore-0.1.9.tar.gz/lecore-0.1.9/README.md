# LE core package

This is package of core python utils for LE containing:
- Looger

## Install

Install or update version
```
pip install lecore
pip install --upgrade lecore
```

## Import

Import package as usual

```python
import lecore
```


# Looger

Class Looger allows for sending debug data into Development Debug Server (DDS) a.k.a. 
Looger. Public instance run on https://looger.jablotron.cz

Create instance when default public endpoint is to be used 

```python
looger = Looger()
```

Set device

```python
looger.set_device(0x111CC1234, 0, None)
```

Send data and log

```python
data = {'data_1': 1, 'data_2': 2}
log = f"Message to log"
looger.send(data, log, 0)
```


# Build [note to myself]

In command line (not venv) run:

Update PIP, build, twine
```
python -m pip install --upgrade build
python -m pip install --upgrade pip
python -m pip install --upgrade twine
```

Run Build
````
py -m build
````


Upload package to pypi.org server

```
py -m twine upload dist/*
```



