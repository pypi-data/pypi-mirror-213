

# mir-ml-utils

The ML engine for the mir (Marine Inspection by Remote) app.

## Install

You can install the utilities via ```pip```

```
pip install mir-ml-utils
```

For a specific version use

```
pip install mir-ml-utils==x.x.x
```

You can uninstall the project via

```
pip3 uninstall mir-ml-utils
```


## Dependencies

- PyTorch
- Numpy
- Pillow
- matplolib

- sphinx (if you want to build the documentation)

The project also gets benefited from <a href="https://pypi.org/project/easyfsl/">easyfsl</a> and
<a href="https://github.com/sicara/easy-few-shot-learning">easy-few-shot-learning</a>. However,
you don't need to install this as a fork is maintained within mir-engine

### Testing

There are additional dependencies if you want to run the tests

- pytest
- coverage
- flake8

In order to test locally, you can run the

```
local_test_pipeline.sh
```

The script first runs ```flake8``` and then ```pytest``` with coverage. Finally, it produces
a report ```coverage_report.txt```.

## Installation 




