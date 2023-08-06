
.. .. image:: https://readthedocs.org/projects/pyproject_ops/badge/?version=latest
    :target: https://pyproject-ops.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/pyproject_ops-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/pyproject_ops-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/MacHu-GWU/pyproject_ops-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/pyproject_ops-project

.. image:: https://img.shields.io/pypi/v/pyproject_ops.svg
    :target: https://pypi.python.org/pypi/pyproject_ops

.. image:: https://img.shields.io/pypi/l/pyproject_ops.svg
    :target: https://pypi.python.org/pypi/pyproject_ops

.. image:: https://img.shields.io/pypi/pyversions/pyproject_ops.svg
    :target: https://pypi.python.org/pypi/pyproject_ops

.. image:: https://img.shields.io/badge/release_history!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/pyproject_ops-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/pyproject_ops-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://pyproject-ops.readthedocs.io/index.html

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://pyproject-ops.readthedocs.io/py-modindex.html

.. .. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://pyproject-ops.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/pyproject_ops-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/pyproject_ops-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/pyproject_ops-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/pyproject_ops#files


Welcome to ``pyproject_ops`` Documentation
==============================================================================


What is this project?
------------------------------------------------------------------------------
There are many different folder structures for Python project. I have my personal best practice based on Python career experience. This project is an automation tools that can do a lot of common tasks for Python project development life cycle, such as: "create virtualenv", "install dependencies", "run test", "build documentation site", etc ...

A little history about this project:

    I had an automation tool `pygitrepo <https://github.com/MacHu-GWU/pygitrepo-project>`_ for my old development workflow. The pygitrepo is primarily based on setup.py and requirements.txt file. ``pyproject_ops`` still support the old convention, and also support ``pyproject.toml`` + ``poetry``. It helps me to write less code to do Python development workflow automations.


How to Use
------------------------------------------------------------------------------
.. code-block:: bash

    pip install pyproject_ops
    pyops --help


Folder Structure
------------------------------------------------------------------------------
Below is the folder structured used in ``pyproject_ops``. The first item is the relative path from the project root directory. The second item is the attribute name that you can use to access the path in ``pyproject_ops``. The third item is the description of the path.

- ``.venv``: ``PyProjectOps.dir_venv``, The virtualenv directory.
- ``.venv/bin``: ``PyProjectOps.dir_venv_bin``, The bin folder in virtualenv.
- ``.venv/bin/pip``: ``PyProjectOps.path_venv_bin_pip``, The pip command in virtualenv.
- ``.venv/bin/poetry``: ``PyProjectOps.path_bin_poetry``, The poetry CLI command path.
- ``.venv/bin/pytest``: ``PyProjectOps.path_venv_bin_pytest``, The pytest command in virtualenv.
- ``.venv/bin/python``: ``PyProjectOps.path_venv_bin_python``, The python executable in virtualenv.
- ``.venv/bin/twine``: ``PyProjectOps.path_bin_twine``, The twine CLI command path.
- ``.venv/bin/virtualenv``: ``PyProjectOps.path_bin_virtualenv``, The virtualenv CLI command path.
- ``build``: ``PyProjectOps.dir_build``, The build folder for Python or artifacts build.
- ``build/lambda``: ``PyProjectOps.dir_build_lambda``, The AWS Lambda artifacts build folder.
- ``build/lambda/layer.zip``: ``PyProjectOps.path_build_lambda_layer_zip``, The AWS Lambda layer zip file path.
- ``build/lambda/python``: ``PyProjectOps.dir_build_lambda_python``, The AWS Lambda layer build folder. This folder contains the dependencies.
- ``build/lambda/python/aws``: ``PyProjectOps.path_build_lambda_bin_aws``, This is the AWS CLI executable path in Lambda layer.
- ``build/lambda/source.zip``: ``PyProjectOps.path_build_lambda_source_zip``, The AWS Lambda source code deployment package zip file path.
- ``config``: ``PyProjectOps.dir_config``, The folder that stores the config files.
- ``config/config.json``: ``PyProjectOps.path_config_json``, Path to the JSON file that stores the non-sensitive config.
- ``dist``: ``PyProjectOps.dir_dist``, The dist folder for Python package distribution (.whl file).
- ``docs``: ``PyProjectOps.dir_sphinx_doc``, Sphinx docs folder.
- ``docs/build``: ``PyProjectOps.dir_sphinx_doc_build``, The temp Sphinx doc build folder.
- ``docs/build/html``: ``PyProjectOps.dir_sphinx_doc_build_html``, The built Sphinx doc build HTML folder.
- ``docs/build/html/index.html``: ``PyProjectOps.path_sphinx_doc_build_index_html``, The built Sphinx doc site entry HTML file path.
- ``docs/source``: ``PyProjectOps.dir_sphinx_doc_source``, Sphinx docs source code folder.
- ``docs/source/conf.py``: ``PyProjectOps.dir_sphinx_doc_source_conf_py``, Sphinx docs ``conf.py`` file path.
- ``docs/source/pyproject_ops``: ``PyProjectOps.dir_sphinx_doc_source_python_lib``, The generated Python library API reference Sphinx docs folder.
- ``htmlcov``: ``PyProjectOps.dir_htmlcov``, The code coverage test results HTML output folder.
- ``lambda_app``: ``PyProjectOps.dir_lambda_app``, The AWS Lambda app handler file and Lambda related code directory.
- ``lambda_app/.chalice/config.json``: ``PyProjectOps.path_chalice_config``, The AWS Chalice framework's config file path.
- ``lambda_app/.chalice/deployed``: ``PyProjectOps.dir_lambda_app_deployed``, The generated ``deployed.json`` file for AWS Chalice framework's.
- ``lambda_app/app.py``: ``PyProjectOps.path_lambda_app_py``, The app.py file for AWS Chalice framework.
- ``lambda_app/lambda_function.py``: ``PyProjectOps.path_lambda_function_py``, The lambda_function.py handler file for AWS Lambda, if you are not using
- ``lambda_app/update_chalice_config.py``: ``PyProjectOps.path_lambda_update_chalice_config_script``, Example: ``${dir_project_root}/lambda_app/update_chalice_config.py``
- ``lambda_app/vendor``: ``PyProjectOps.dir_lambda_app_vendor``, The vendor folder for AWS Chalice framework's packaging.
- ``poetry-lock-hash.json``: ``PyProjectOps.path_poetry_lock_hash_json``, The poetry-lock-hash.json file path. It is the cache of the poetry.lock file hash.
- ``poetry.lock``: ``PyProjectOps.path_poetry_lock``, The poetry.lock file path.
- ``pyproject.toml``: ``PyProjectOps.path_pyproject_toml``, The pyproject.toml file path.
- ``pyproject_ops``: ``PyProjectOps.dir_python_lib``, The current Python library directory.
- ``pyproject_ops/_version.py``: ``PyProjectOps.path_version_py``, Path to the ``_version.py`` file where the package version is defined.
- ``requirements-automation.txt``: ``PyProjectOps.path_requirements_automation``, The requirements-automation.txt file path.
- ``requirements-dev.txt``: ``PyProjectOps.path_requirements_dev``, The requirements-dev.txt file path.
- ``requirements-doc.txt``: ``PyProjectOps.path_requirements_doc``, The requirements-doc.txt file path.
- ``requirements-test.txt``: ``PyProjectOps.path_requirements_test``, The requirements-test.txt file path.
- ``requirements.txt``: ``PyProjectOps.path_requirements``, The requirements.txt file path.
- ``tests``: ``PyProjectOps.dir_tests``, Unit test folder.
- ``tests_int``: ``PyProjectOps.dir_tests_int``, Integration test folder.
- ``tests_load``: ``PyProjectOps.dir_tests_load``, Load test folder.


Develop and Release Strategy
------------------------------------------------------------------------------
This project is a "meta" project for other projects, it is very hard to test. I keep using this project in many of my production projects, and continuously improving it. I will merge all the changes manually into this every three months.


.. _install:

Install
------------------------------------------------------------------------------

``pyproject_ops`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install pyproject_ops

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade pyproject_ops