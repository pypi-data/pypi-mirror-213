pyrdfj2
===================================

Python wrapper on jinja SPARQL templating

Started on 2023-06-09

Setup
-----
Start using this project with poetry


.. code-block:: bash

    $ make init       # install dependencies
    $ make init-dev   # includes the previous + adds dependencies for developers

Build Docs

.. code-block:: bash

    $ make docs



Developers
----------

Run Tests

.. code-block:: bash

    $ make test                                                   # to run all tests
    $ PYTEST_LOGCONF=debug-logconf.yml python tests/test_demo.py  # to run a specific test with specific logging
    $ make test-coverage                                          # to run all tests and check the test coverage


Check the code-style and syntax (flake8, black, isort)

.. code-block:: bash

    $ make check
