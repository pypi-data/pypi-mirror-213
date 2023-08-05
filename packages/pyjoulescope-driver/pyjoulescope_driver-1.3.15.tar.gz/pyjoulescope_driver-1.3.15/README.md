<!--
# Copyright 2014-2023 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
-->

[![Windows amd64](https://github.com/jetperch/joulescope_driver/actions/workflows/windows_amd64.yml/badge.svg)](https://github.com/jetperch/joulescope_driver/actions/workflows/windows_amd64.yml)
[![macOS amd64](https://github.com/jetperch/joulescope_driver/actions/workflows/macos_amd64.yml/badge.svg)](https://github.com/jetperch/joulescope_driver/actions/workflows/macos_amd64.yml)
[![Ubuntu Linux amd64](https://github.com/jetperch/joulescope_driver/actions/workflows/linux_amd64.yml/badge.svg)](https://github.com/jetperch/joulescope_driver/actions/workflows/linux_amd64.yml)


# Joulescope Driver

Welcome to the Joulescope™ Driver project.
[Joulescope](https://www.joulescope.com) is an affordable, precision DC energy
analyzer that enables you to build better products.

This user-space C library communicates with Joulescope products to configure 
operation and receive data.  The first-generation driver introduced in 2019 was
written in Python.  While Python proved to be a very flexible language enabling
many user scripts, it was difficult to support other languages.  
This second-generation driver launched in 2022 addresses several issues
with the first-generation python driver including:

1. Improved event-driven API based upon PubSub for easier integration with 
   user interfaces and other complicated software packages.
2. Improved portability for easier language bindings.
3. Improved performance.

For more information, see:

* [source code](https://github.com/jetperch/joulescope_driver)
* [documentation](https://joulescope-driver.readthedocs.io/en/latest/)
* [pypi](https://pypi.org/project/pyjoulescope-driver/)
* [Joulescope](https://www.joulescope.com/) (Joulescope web store)
* [jls](https://github.com/jetperch/jls) (Joulescope file format)
* [forum](https://forum.joulescope.com/)


## Building

Ensure that your computer has a development environment including CMake.  


### Windows

Install cmake and your favorite build toolchain such as 
Visual Studio, mingw64, wsl, ninja.

### macOS

For macOS, install homebrew, then:

    brew install pkgconfig python3


### Ubuntu 22.04 LTS

For Ubuntu:

    sudo apt install cmake build-essential ninja-build

### Common

    cd {your/repos/joulescope_driver}
    mkdir build && cd build
    cmake ..
    cmake --build . && ctest .

This package includes a command-line tool, jsdrv_util:

    jsdrv_util --help
    jsdrv_util scan


## Python bindings

The python bindings are made to work with Python 3.9 and later.  To install
the dependencies:

    cd {your/repos/joulescope_driver}
    pip3 install -U requirements.txt

You should then be able to build the native bindings:

    python3 setup.py build_ext --inplace

On Windows, you may be prompted to install the 
[Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
You may also need to use "python" rather than "python3" on some platforms.

And run the Python tools:

    python3 -m pyjoulescope_driver --help
    python3 -m pyjoulescope_driver scan
    python3 -m pyjoulescope_driver info
    python3 -m pyjoulescope_driver info * --verbose

You may optionally choose to use a Python virtual environment.
