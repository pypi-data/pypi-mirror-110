dtool CLI commands for working with tags
========================================

.. image:: https://badge.fury.io/py/dtool-tag.svg
   :target: http://badge.fury.io/py/dtool-tag
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtool-tag.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtool-tag
   :alt: Travis CI build status (Linux)

.. image:: https://ci.appveyor.com/api/projects/status/esk2swpyp4l6wmtl?svg=true
   :target: https://ci.appveyor.com/project/tjelvar-olsson/dtool-tag
   :alt: AppVeyor CI build status (Windows)

.. image:: https://codecov.io/github/jic-dtool/dtool-tag/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtool-tag?branch=master
   :alt: Code Coverage


Installation
------------

::

    $ pip install dtool-tag


Example usage
------------- 


Get a dataset to play with::

    $ LOCAL_DS_URI=$(dtool cp -q http://bit.ly/Ecoli-ref-genome .)


Add a couple of  tags::

    $ dtool tag set $LOCAL_DS_URI e.coli
    $ dtool tag set $LOCAL_DS_URI genome

List the dataset tags::

    $ dtool tag ls $LOCAL_DS_URI
    e.coli
    genome

Delete a tag::

    $ dtool tag delete $LOCAL_DS_URI genome

For more information see the `dtool documentation <https://dtool.readthedocs.io>`_.

Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-create <https://github.com/jic-dtool/dtool-create>`_
- `dtool-overlay <https://github.com/jic-dtool/dtool-overlay>`_
- `dtool-annotation <https://github.com/jic-dtool/dtool-annotation>`_
