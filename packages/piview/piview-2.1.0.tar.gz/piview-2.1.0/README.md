# PiView

![https://pypi.python.org/pypi/piview](https://img.shields.io/pypi/v/piview.svg)
![https://travis-ci.com/AdyGCode/piview](https://img.shields.io/travis/AdyGCode/piview.svg)
![https://piview.readthedocs.io/en/latest/?version=latest](https://readthedocs.org/projects/piview/badge/?version=latest)

### *A Raspberry Pi System Information Package*

<img src="https://raw.githubusercontent.com/AdyGCode/piview/master/PiView.svg" width="96"
height="96" />

PiView provides the details of the Raspberry Pi currently being interrogated.

## General Information

* Free software: Open Software License ("OSL") v. 3.0
* Documentation: https://piview.readthedocs.io.


## Features

PiView provides system information including, but not limited to:

|  Group   | Information                                                           |
|:--------:|-----------------------------------------------------------------------|
| CPU      | max load across cores, temperature, clock speed                       |
| GPU      | temperature                                                           |
| HARDWARE | bluetooth, i2c, spi, camera statuses                                  |
| HOST     | boot time, model, name, revision, serial number, uptime               |
| NETWORK  | host name, interface names, ip addresses, mac addresses               |
| STORAGE  | total disk capacity, free disk capacity, total RAM and free RAM       |

Also includes a small utility library with:

- conversion of bytes into Kilobytes, Megabytes, Gigabytes and up
- create list with a quartet of integer numbers representing the IPv4 Address


## Requirements

This project requires the following package(s):

* `psutils`

Remaining packages are Python 'built-ins'.

## Building

use the setuptools based compile and upload to PyPi:

```shell
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
```

## Credits

A very large thank you to Matt Hawkins upon whose code this package is based: https://www.raspberrypi-spy.co.uk/

The original code may be found at https://github.com/tdamdouni/Raspberry-Pi-DIY-Projects/blob/master/MattHawkinsUK-rpispy-misc/python/mypi.py

Thank you to Sander Huijsen for his contributions and guidance in all things Python.

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.

[Cookiecutter: https://github.com/audreyr/cookiecutter](https://github.com/audreyr/cookiecutter)
[Cookiecutter PyPackage: https://github.com/audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)


## Copyright

Copyright Adrian Gould, 2021-. Licensed under
the Open Software License version 3.0
