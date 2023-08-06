<h1 align="center">Django Password History</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Lenders-Cooperative/django-password-history)](https://github.com/Lenders-Cooperative/django-password-history/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Lenders-Cooperative/django-password-history/pulls)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>

---

<p align="center"> Django module meant to allow django users to keep a history of their previously used passwords.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Built Using](#built-using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgements)

## About

Django module meant to allow django users to keep a history of their previously used passwords.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The only prerequisite to installing django-password-history is having django 2 installed.
```
Django 2
```

### Installing

The installation process for django password history is very simple. Start by running the following command to install the package.

```
pip install django-password-history
```


End with an example of getting some data out of the system or using it for a little demo.

## 🔧 Running the tests <a name = "tests"></a>

The test suite for this package is a work in progress. The initial sample test can be run by using the following command.

```
coverage run --source django_password_history runtests.py
```


## Usage

In order to use the system you must add django_password_history to your installed apps.

```
INSTALLED_APPS = [
    'django_password_history'
]
```


## Built Using

- [Django](https://www.djangoproject.com/) - Web Framework
- [Cookiecutter Django Package](https://github.com/pydanny/cookiecutter-djangopackage) - Cookie Cutter Django Package

## Authors
- David Graves - Working on behalf of Lender's Cooperative
- [Roderick Smith](https://github.com/rsmith0717) - Working on behalf of Lender's Cooperative


## Acknowledgements

- Inspiration
- References
