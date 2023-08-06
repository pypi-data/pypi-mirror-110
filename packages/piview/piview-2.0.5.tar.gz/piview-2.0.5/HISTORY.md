# History

## 3.0.0 (TBA)

This will contain some 'breaking' changes.

* All results will be returned as dictionary with reading type and value
* Recreate the testing methods
* Update online documentation
* Deprecate the PiView_AG edition
* Code contains list of TODO elements - showing improvements / new features

## 2.0.3 (2021-05-30)

* Minor edits to code.
* CPU speed returns random value if parameter `random=True` used in call, or -1 when parameter `random=False` (or omitted)
* Temperatures return -273.16ºC when no reading given (absolute zero)
* Keeping documentation edits within this version until next minor update to code

## 2.0.2 (2021-05-28)

* Minor Fixes

## 2.0.1 (2021-05-27)

* Updated Package release.


## 1.0.0 Initial Release
Some enhancements to come - such as return all the attached
storage statistics

Added:

- python version (HOST)
- camera supported / detected (HARDWARE)

## 0.5.0 RAM, Storage, Host

Added the following:

- ram total and free
- storage total and free for 'all disks' in total
- name to Host, this is a temporary version until further investigation done, use the host
  name method in the network section to get host name

To do:

- statistics (total space, free) for each attached storage device


## 0.4.0 Network Features

The following are implemented in this version:

- host name
- interface names
- ip addresses
- mac addresses

Fixed missing self references in classes, removed `get` from function names
Added missing file headers...

## 0.3.0 Host Features

The following have been implemented:

- boot time
- model
- serial number
- uptime
- revision


## 0.2.0 Hardware Features

Added Hardware checking for:

- SPI
- I2C
- BT

Updated [[README]]
Design and added PiView Icon

## 0.1.1 GPU Features

Added:

- GPU temperature

##0.1.0 CPU Features

Added:

- max load across cores
- processor temperature
- processor clock speed

## 0.0.3 Setup fixes

Small fixes to setup.cfg, and a source reformat.

## 0.0.2 Utils

Added Utils to the package. Utils includes:

- format_bytes
- draw_line

## 0.0.1 Initial Version

Blank project, containing:

- starter folder structure
- [[README.md]]
- [[CHANGES.md]]
- [[LICENSE]]
