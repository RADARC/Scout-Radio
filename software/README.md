# Prerequisites
Linux-only support initially.
First set up PYTHONPATH as appropriate. For example,

```export PYTHONPATH=${HOME}/Scout-Radio/hosttools```

You may find
```alias sr='export PYTHONPATH=${HOME}/Scout-Radio/hosttools'```
in your ~/.bashrc or whatever handy

# To install a blank system

```python sysintall.py```

# To install or update individual components (for example Radio)

```cd Radio```

```python install.py```

# To run a component on target (for example Radio):

```cd Radio```

```python run.py```
