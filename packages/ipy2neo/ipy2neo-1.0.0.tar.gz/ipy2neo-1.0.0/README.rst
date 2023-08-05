ipy2neo
=======
.. image:: https://img.shields.io/pypi/v/ipy2neo.svg
   :target: https://pypi.python.org/pypi/ipy2neo
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/dm/ipy2neo
   :target: https://pypi.python.org/pypi/ipy2neo
   :alt: PyPI Downloads

.. image:: https://img.shields.io/github/license/technige/ipy2neo.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: License


**ipy2neo** is a an interactive command line console for working with `Neo4j <https://neo4j.com/>`_ built on top of the `py2neo <https://py2neo.org>`_ library.


Quick Example
-------------

To connect to a local Neo4j instance is straightforward::

    $ ipy2neo --uri neo4j://localhost:7687 --auth neo4j:password
    neo4j@localhost/~ -> CREATE (a:Person {name:'Alice'})-[:KNOWS]->(b:Person {name:'Bob'}) RETURN a, b
     a                           | b
    -----------------------------|---------------------------
     (_0:Person {name: 'Alice'}) | (_1:Person {name: 'Bob'})





Installation
------------

To install ipy2neo, simply use:

.. code-block::

    $ pip install ipy2neo


Requirements
------------
.. image:: https://img.shields.io/pypi/pyversions/ipy2neo.svg
   :target: https://www.python.org/
   :alt: Python versions

.. image:: https://img.shields.io/badge/neo4j-3.4%20%7C%203.5%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%204.3-blue.svg
   :target: https://neo4j.com/
   :alt: Neo4j versions

The following versions of Python and Neo4j (all editions) are supported:

- Python 2.7 / 3.5 / 3.6 / 3.7 / 3.8 / 3.9
- Neo4j 3.4 / 3.5 / 4.0 / 4.1 / 4.2 / 4.3 (the latest point release of each version is recommended)

Note also that ipy2neo is developed and tested under **Linux** using standard CPython distributions.
While other operating systems and Python distributions may work, support for these is not available.
