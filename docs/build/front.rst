============
Front Matter
============

Information about the SQLSoup project.

Project Status
==============

.. admonition:: **SQLSoup is Unmaintained / Unsupported**

   SQLSoup no longer functions with modern versions of SQLAlchemy and the project is currently unmaintained.
   For modern support of ad-hoc models based on 
   database reflection, please refer to the `automap <https://docs.sqlalchemy.org/en/stable/orm/extensions/automap.html>`_ feature
   at: https://docs.sqlalchemy.org/en/stable/orm/extensions/automap.html

   Note that the architectural approach of SQLSoup remains compatible with modern SQLAlchemy versions, so that
   if someone wanted to take over maintenance of the project, it could be made to work again.


Project Homepage
================

SQLSoup's code is hosted at 
https://github.com/zzzeek/sqlsoup/


.. _installation:

Installation
============

Install released versions of SQLSoup from the Python package 
index with `pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::

    pip install sqlsoup

Installation via source distribution is via the ``setup.py`` script::

    python setup.py install

Dependencies
------------

SQLSoup's install process will ensure that `SQLAlchemy <http://www.sqlalchemy.org>`_ 
is installed, in addition to other dependencies.  The 0.7 series of 
SQLAlchemy or greater is recommended.  The 1.4 series of SQLAlchemy and greater are
currently not supported.


Community
=========

SQLSoup was originally written by Jonathan Ellis, and was later 
maintained 
by `Mike Bayer <http://techspot.zzzeek.org>`_.

