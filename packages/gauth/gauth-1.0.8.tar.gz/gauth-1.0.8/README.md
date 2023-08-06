GAuth
====

Command Line tool to migrate Google Authenticator from phone to desktop.

# How to use it

`pip install gauth` and check the help using `gauth -h`.

## Installation of optional shared system libraries

For reading QR codes with `ZBAR` QR reader, the zbar library must be installed.
If you do not use the `ZBAR` QR reader, you do not need to install the zbar shared library. Note: The `ZBAR` QR reader is the showed for me the best results and is thus default QR Reader.

For a detailed installation documentation of [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar#installation).

### Linux (Debian, Ubuntu, …)

    sudo apt-get install libzbar0

### Linux (OpenSUSE)

    sudo zypper install libzbar0

### Linux (Fedora)

    sudo dnf install zbar

### Linux (Arch Linux)

    pacman -S zbar

### Mac OS X

    brew install zbar

### Windows

#### zbar

The zbar DLLs are included with the Windows Python wheels. However, you might need additionally to install [Visual C++ Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/en-US/download/details.aspx?id=40784). Install `vcredist_x64.exe` if using 64-bit Python, `vcredist_x86.exe` if using 32-bit Python. For more information see [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)

# Release

```
pip install --upgrade twine
python setup.py sdist
twine upload dist/*
```
# YAML example

```
---
keys:
  - Name:    TEST1
    Secret:  1234567
    Issuer:  ABC
    Type:    totp

  - Name:    TEST2
    Secret:  1234455
    Issuer:  CDE
    Type:    totp
```

# Reference

[extract_otp_secrets v2.4.3](https://github.com/scito/extract_otp_secrets)

