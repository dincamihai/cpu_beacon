Installation:

.. code-block:: bash

    git clone https://github.com/dincamihai/cpu_beacon.git
    cd cpu_beacon
    apt-get install python-dev
    virtualenv sandbox
    echo "*" > sandbox/.gitignore
    . sandbox/bin/activate
    pip install requirements-test.txt

Run Tests:

.. code-block:: bash

    py.test
