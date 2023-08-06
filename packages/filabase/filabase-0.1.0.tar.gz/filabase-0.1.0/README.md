# README #

### What is this repository for? ###

A simple database-like facility for writing json-like structures into text
files. Each structure is written on a separate line.

* Takes a directory path where the files are situated
* If the directory does not exist it is created.
* Splits the records into separate files, according to the record type.

Or

* provides a key-value store with persistence based on the json-store described
above

### How do I get set up? ###

* Summary of set up

  If this gets published on pypi.org, run the following command:
  ```pip install filabase```

  In case it is unfit for pypi:

  - clone the repository;

  - cd into the filabase directory;

  - activate the environment

  - execute:

   ```python3 setup.py sdist bdist_wheel```

  - install using:

      ```pip install ./dist/filabase-<version>-py3-none-any.whl```

* Configuration

    Nothing to configure yet

* Dependencies

    Sole dependency is on pytest for running the tests during development.
    In production, it does not depend on other packages

* Database configuration

    This is basically a database.

* Usage

  Once it is installed import one of the facilities like this:

     from filabase import keyvaluestore

  Or just

     import filabase

* How to run tests

    When in the root directory run:

    ```python3 -m pytest ```

* Deployment instructions


### Contribution guidelines ###

* Writing tests

    Unit tests as well as Integration tests ensuring the proposed feature is
    functional should be included in the pull request.

* Code review
* Other guidelines

### Help needed ###

Obviously I need help with the README markup. Feel free to create a pull
request.

Further, this library is definitely full of bugs. If you feel you can fix any of
them, I'll be glad to accept a pull-request. Or perhaps just report it. I might
have some time to fix it.

### Who do I talk to? ###

* Repo owner or admin

    Nikola Geneshki: ngeneshki at gmail dot com

* Other community or team contact
