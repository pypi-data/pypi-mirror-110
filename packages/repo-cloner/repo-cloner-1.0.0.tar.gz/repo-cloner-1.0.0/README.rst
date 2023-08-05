repo-cloner
===========

Open source repository cloner.

- Github: https://github.com/danpeczek/repo-cloner

repo-cloner is a python utility to clone multiple repositories at once without bothering
to do it manual. Tool reads the information about your repositories and clone them into current
directory.

+-------------------------+
|       **main**          |
+=========================+
| |Build Status Develop|  |
+-------------------------+

Setup
=====

Currently the tool is available only on test pypi repository.

.. code-block:: bash

    $ pip install -i https://test.pypi.org/simple/ repo-cloner==0.0.4

Now try to run repo-cloner:

.. code-block:: bash

    $ repo-cloner -h
    Usage: repo-cloner [--help][-h][--repo_file][-rf]
    --help, -h: prints this message
    --repo_file, -rf: .yml file with list of repositories to clone

The list of repositories can be passed either:

.. code-block:: bash

    - git@repo1.git
    - https://repo2.git
    - https://repo3.git

or:

.. code-block:: bash

    dir1:
        - git@repo1.git
    dir2:
        dir3:
        - https://repo2.git
        dir4:
        - https://repo3.git

If you will use the second approach then remember:

    * `dir` will be another directory created from the directory from where you are calling the script.
    * You cannot mix structures - list of repositories and other directories cannot lay on the same level e.g:

.. code-block:: bash

    path1:
      - repo1
      - repo2
      - repo3
      - repo4
    - repo5
    - repo6
    - repo7
    path2:
      - repo8
      - repo9
      - repo10

Is not allowed.

License
-------

`MIT LICENSE <./LICENSE>`__

.. |Build Status Develop| image:: https://ci.conan.io/buildStatus/icon?job=ConanTestSuite/develop
   :target: https://api.travis-ci.com/danpeczek/repo-cloner.svg?branch=main