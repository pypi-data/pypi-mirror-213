[![](https://img.shields.io/pypi/v/hanmatek-psu.svg?maxAge=3600)](https://pypi.org/project/hanmatek-psu/)
[![Latest Release](https://gitlab.com/janoskut/hanmatek-psu/-/badges/release.svg)](https://gitlab.com/janoskut/hanmatek-psu/-/releases)
[![pipeline status](https://gitlab.com/janoskut/hanmatek-psu/badges/main/pipeline.svg)](https://gitlab.com/janoskut/hanmatek-psu/-/commits/main)
[![coverage report](https://gitlab.com/janoskut/hanmatek-psu/badges/main/coverage.svg)](https://gitlab.com/janoskut/hanmatek-psu/-/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



# Hanmatek HM3xxP PSU control library and CLI

Unifying library and CLI for the popular and low-cost digital lab power supplies `HM305P` and
`HM310P`.

The library provides an (almost) complete, easy to use interface to all known functions of the
device. This project is different to the below mentioned ones, in that it provides a minimal,
but complete interface to the device and also keeps the dependencies low.

This project is based on the work done in <https://github.com/notkevinjohn/HM310P>, which uses the
`minimalmodbus` library for device communication. Other related projects were providing
useful register definition and hints:

- <https://github.com/JackDoan/hm305_ctrl/tree/master/hm305>
- <https://github.com/hobbyquaker/hanmatek-hm310p>
- <https://sigrok.org/wiki/ETommens_eTM-xxxxP_Series#Protocol>


## Installation

```py
pip install hanmatek-psu
```

If users are in the `plugdev` user group, Hanmatek devices are accessible via `/dev/ttyUSBx` without
privileges. Adding the following `udev` rule will create a symlink `/dev/ttyHM3xxP` when a Hanmatek
PSU device is plugged in via USB. This symlink is used by default by the `hanmatek-cli` to find
devices:

```sh
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="ttyHM3xxP", MODE="0666", GROUP="plugdev"' | sudo tee "/etc/udev/rules.d/99-hanmatek.rules" > /dev/null
```

## Usage

### CLI Usage

```sh
hanmatek-cli -h
hanmatek-cli --discover             # find devices
hanmatek-cli                        # show default device info
hanmatek-cli --device /dev/ttyUSB0  # specific device
hanmatek-cli voltage:set 3.0        # set voltage
hanmatek-cli current:set 0.1        # set current limit
hanmatek-cli output on
hanmatek-cli current                # read current
hanmatek-cli power                  # read power
hanmatek-cli output off
hanmatek-cli --list                 # list all commands/registers
```

### Library Usage

```py
from hanmatek import HM3xxP

device = HM3xxP("/dev/ttyHM3xxP")
print(device.info())
device.write("voltage:set", 3.0)
device.write("current:set", 3.0)
device.write("output", True)
print(device.read("current"))
print(device.read("power"))
device.write("output", False)
```

## Development

The following tools are used to provide clean and quality software, and made available through a
`tox` configuration: `flake8` for linting, `black` for code formatting and checking, `mypy` for
type checking and `pytest` for unit tests. Use as:

```sh
pip install tox
```

```sh
tox -a       # show test environments
tox          # run all
tox -e test  # run unit tests
tox -e lint  # run lint
tox -e type  # run type checker
```

(we're using [`pyproject-flake8`](https://pypi.org/project/pyproject-flake8), so that the `flake8`
configuration can live in `pyproject.toml` - within `tox` we then run `pflake8` instead of
`flake8`.)
