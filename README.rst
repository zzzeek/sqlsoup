=======
SQLSoup
=======

SQLSoup provides a convenient way to map Python objects
to relational database tables, with no declarative code
of any kind.   It's built on top of the
`SQLAlchemy <http://www.sqlalchemy.org>`_ ORM and provides a
super-minimalistic interface to an existing database.

Usage is as simple as::

    import sqlsoup
    db = sqlsoup.SQLSoup("postgresql://scott:tiger@localhost/test")

    for user in db.users.all():
        print "user:", user.name

    db.users.filter_by(name="ed").update({"name":"jack"})
    db.commit()

Included for many years as an extension to SQLAlchemy itself, SQLSoup
has been broken out into it's own project as of 2012.   The community is encouraged
to collaborate on Bitbucket with patches and features.

Documentation and status of SQLSoup is at http://readthedocs.org/docs/sqlsoup/.
