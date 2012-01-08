=========
Tutorial
=========

SQLSoup provides a convenient way to access existing database
tables without having to declare table or mapper classes ahead
of time. It is built on top of the SQLAlchemy ORM and provides a
super-minimalistic interface to an existing database.

SQLSoup effectively provides a coarse grained, alternative
interface to working with the SQLAlchemy ORM, providing a "self
configuring" interface for extremely rudimental operations. It's
somewhat akin to a "super novice mode" version of the ORM.  While
you can do a lot more with the SQLAlchemy ORM directly, SQLSoup
will have you querying an existing database in just two lines
of code.

SQLSoup is really well suited to quick one-offs, early learning
of SQLAlchemy, and small scripting activities.  It can be used
in larger applications such as web applications as well, but 
here you'll begin to experience diminishing returns; in a substantial
web application, it might be time to just switch to SQLAlchemy's
:ref:`ormtutorial_toplevel`. 

Getting Ready to Connect
=========================

Suppose we have a database with users, books, and loans tables
(corresponding to the PyWebOff dataset, if you're curious).

Creating a SQLSoup gateway is just like creating a SQLAlchemy
engine.   The urls are in the same format as those used by
:func:`sqlalchemy.create_engine`::

    >>> import sqlsoup
    >>> db = sqlsoup.SQLSoup('postgresql://scott:tiger@localhost/test')

or, you can re-use an existing engine::

    >>> db = sqlsoup.SQLSoup(engine)

You can optionally specify a schema within the database for your
SQLSoup::

    >>> db.schema = "myschemaname"

Note that the :class:`.SQLSoup` object doesn't actually connect
to the database until it's first asked to do something.  If the connection
string is incorrect, the error will be raised when SQLSoup first tries
to connect.

See also:

:ref:`engines_toplevel` - SQLAlchemy supported database backends, engine
connect strings, etc.

Loading objects
===============

When using a :class:`.SQLSoup`, you access attributes from it which match
the name of a table in the database.   If your database has a table named
``users``, you'd get to it via an attribute named ``.users``.

Loading objects is as easy as this::

    >>> users = db.users.all()
    >>> users.sort()
    >>> users
    [
        MappedUsers(name=u'Joe Student',email=u'student@example.edu',
                password=u'student',classname=None,admin=0), 
        MappedUsers(name=u'Bhargan Basepair',email=u'basepair@example.edu',
                password=u'basepair',classname=None,admin=1)
    ]

Field access is intuitive::

    >>> users[0].email
    u'student@example.edu'

An alternative to ``db.users`` is to use the :meth:`.SQLSoup.entity` method,
which accepts a string argument.   This is useful if the name of your table has 
special casing or other character considerations:

    >>> my_user_table = db.entity("User_Table")

You can then refer to ``my_user_table`` the same way we refer to ``db.users``
in this tutorial.

Basic Table Usage
=================

The table object proxies out to the SQLAlchemy :class:`sqlalchemy.orm.query.Query`
object.   For example, we can sort with ``order_by()``::

    >>> db.users.order_by(db.users.name).all()
    [
        MappedUsers(name=u'Bhargan Basepair',email=u'basepair@example.edu',
            password=u'basepair',classname=None,admin=1), 
        MappedUsers(name=u'Joe Student',email=u'student@example.edu',
            password=u'student',classname=None,admin=0)
    ]

Of course, you don't want to load all users very often. Let's
add a WHERE clause. Let's also switch the order_by to DESC while
we're at it::

    >>> from sqlalchemy import or_, and_, desc
    >>> where = or_(db.users.name=='Bhargan Basepair', db.users.email=='student@example.edu')
    >>> db.users.filter(where).order_by(desc(db.users.name)).all()
    [
        MappedUsers(name=u'Joe Student',email=u'student@example.edu',
            password=u'student',classname=None,admin=0), 
        MappedUsers(name=u'Bhargan Basepair',email=u'basepair@example.edu',
            password=u'basepair',classname=None,admin=1)
    ]

You can also use .first() (to retrieve only the first object
from a query) or .one() (like .first when you expect exactly one
user -- it will raise an exception if more were returned)::

    >>> db.users.filter(db.users.name=='Bhargan Basepair').one()
    MappedUsers(name=u'Bhargan Basepair',email=u'basepair@example.edu',
            password=u'basepair',classname=None,admin=1)

Since name is the primary key, this is equivalent to

    >>> db.users.get('Bhargan Basepair')
    MappedUsers(name=u'Bhargan Basepair',email=u'basepair@example.edu',
        password=u'basepair',classname=None,admin=1)

This is also equivalent to

    >>> db.users.filter_by(name='Bhargan Basepair').one()
    MappedUsers(name=u'Bhargan Basepair',email=u'basepair@example.edu',
        password=u'basepair',classname=None,admin=1)

filter_by is like filter, but takes kwargs instead of full
clause expressions. This makes it more concise for simple
queries like this, but you can't do complex queries like the
or\_ above or non-equality based comparisons this way.

Full query documentation
------------------------

Get, filter, filter_by, order_by, limit, and the rest of the
query methods are explained in detail in
:ref:`ormtutorial_querying`.

Modifying objects
=================

Modifying objects is intuitive::

    >>> user.email = 'basepair+nospam@example.edu'
    >>> db.commit()

(SQLSoup leverages the sophisticated SQLAlchemy unit-of-work
code, so multiple updates to a single object will be turned into
a single ``UPDATE`` statement when you commit.)

To finish covering the basics, let's insert a new loan, then
delete it::

    >>> book_id = db.books.filter_by(title='Regional Variation in Moss').first().id
    >>> db.loans.insert(book_id=book_id, user_name=user.name)
    MappedLoans(book_id=2,user_name=u'Bhargan Basepair',loan_date=None)

    >>> loan = db.loans.filter_by(book_id=2, user_name='Bhargan Basepair').one()
    >>> db.delete(loan)
    >>> db.commit()

You can also delete rows that have not been loaded as objects.
Let's do our insert/delete cycle once more, this time using the
loans table's delete method. (For SQLAlchemy experts: note that
no flush() call is required since this delete acts at the SQL
level, not at the Mapper level.) The same where-clause
construction rules apply here as to the select methods::

    >>> db.loans.insert(book_id=book_id, user_name=user.name)
    MappedLoans(book_id=2,user_name=u'Bhargan Basepair',loan_date=None)
    >>> db.loans.delete(db.loans.book_id==2)

You can similarly update multiple rows at once. This will change the
book_id to 1 in all loans whose book_id is 2::

    >>> db.loans.filter_by(db.loans.book_id==2).update({'book_id':1})
    >>> db.loans.filter_by(book_id=1).all()
    [MappedLoans(book_id=1,user_name=u'Joe Student',
        loan_date=datetime.datetime(2006, 7, 12, 0, 0))]


Joins
=====

Occasionally, you will want to pull out a lot of data from related
tables all at once.  In this situation, it is far more efficient to
have the database perform the necessary join.  (Here we do not have *a
lot of data* but hopefully the concept is still clear.)  SQLAlchemy is
smart enough to recognize that loans has a foreign key to users, and
uses that as the join condition automatically::

    >>> join1 = db.join(db.users, db.loans, isouter=True)
    >>> join1.filter_by(name='Joe Student').all()
    [
        MappedJoin(name=u'Joe Student',email=u'student@example.edu',
            password=u'student',classname=None,admin=0,book_id=1,
            user_name=u'Joe Student',loan_date=datetime.datetime(2006, 7, 12, 0, 0))
    ]

If you're unfortunate enough to be using MySQL with the default MyISAM
storage engine, you'll have to specify the join condition manually,
since MyISAM does not store foreign keys.  Here's the same join again,
with the join condition explicitly specified::

    >>> db.join(db.users, db.loans, db.users.name==db.loans.user_name, isouter=True)
    <class 'sqlsoup.MappedJoin'>

You can compose arbitrarily complex joins by combining Join objects
with tables or other joins.  Here we combine our first join with the
books table::

    >>> join2 = db.join(join1, db.books)
    >>> join2.all()
    [
        MappedJoin(name=u'Joe Student',email=u'student@example.edu',
            password=u'student',classname=None,admin=0,book_id=1,
            user_name=u'Joe Student',loan_date=datetime.datetime(2006, 7, 12, 0, 0),
            id=1,title=u'Mustards I Have Known',published_year=u'1989',
            authors=u'Jones')
    ]

If you join tables that have an identical column name, wrap your join
with `with_labels`, to disambiguate columns with their table name
(.c is short for .columns)::

    >>> db.with_labels(join1).c.keys()
    [u'users_name', u'users_email', u'users_password', 
        u'users_classname', u'users_admin', u'loans_book_id', 
        u'loans_user_name', u'loans_loan_date']

You can also join directly to a labeled object::

    >>> labeled_loans = db.with_labels(db.loans)
    >>> db.join(db.users, labeled_loans, isouter=True).c.keys()
    [u'name', u'email', u'password', u'classname', 
        u'admin', u'loans_book_id', u'loans_user_name', u'loans_loan_date']


Relationships
=============

You can define relationships between classes using the :meth:`~.TableClassType.relate`
method from any mapped table:

    >>> db.users.relate('loans', db.loans)

These can then be used like a normal SA property:

    >>> db.users.get('Joe Student').loans
    [MappedLoans(book_id=1,user_name=u'Joe Student',
                    loan_date=datetime.datetime(2006, 7, 12, 0, 0))]

    >>> db.users.filter(~db.users.loans.any()).all()
    [MappedUsers(name=u'Bhargan Basepair',
            email='basepair+nospam@example.edu',
            password=u'basepair',classname=None,admin=1)]

:meth:`~.TableClassType.relate` can take any options that the relationship function
accepts in normal mapper definition:

    >>> del db._cache['users']
    >>> db.users.relate('loans', db.loans, order_by=db.loans.loan_date, cascade='all, delete-orphan')

Advanced Use
============

Sessions, Transactions and Application Integration
--------------------------------------------------

.. note::

   Please read and understand this section thoroughly
   before using SQLSoup in any web application.

SQLSoup uses a :class:`sqlalchemy.orm.scoping.ScopedSession` to provide thread-local sessions.
You can get a reference to the current one like this::

    >>> session = db.session

The default session is available at the module level in SQLSoup,
via::

    >>> from sqlsoup import Session

The configuration of this session is ``autoflush=True``,
``autocommit=False``. This means when you work with the SQLSoup
object, you need to call :meth:`.SQLSoup.commit` in order to have
changes persisted. You may also call :meth:`.SQLSoup.rollback` to roll
things back.

Since the SQLSoup object's Session automatically enters into a
transaction as soon as it's used, it is *essential* that you
call :meth:`.SQLSoup.commit` or :meth:`.SQLSoup.rollback` on it when the work within a
thread completes. This means all the guidelines for web
application integration at :ref:`session_lifespan` must be
followed.

The SQLSoup object can have any session or scoped session
configured onto it. This is of key importance when integrating
with existing code or frameworks such as Pylons. If your
application already has a ``Session`` configured, pass it to
your SQLSoup object::

    >>> from myapplication import Session
    >>> db = SQLSoup(session=Session)

If the ``Session`` is configured with ``autocommit=True``, use
``flush()`` instead of ``commit()`` to persist changes - in this
case, the ``Session`` closes out its transaction immediately and
no external management is needed. ``rollback()`` is also not
available. Configuring a new SQLSoup object in "autocommit" mode
looks like::

    >>> from sqlalchemy.orm import scoped_session, sessionmaker
    >>> db = SQLSoup('sqlite://', session=scoped_session(sessionmaker(autoflush=False, expire_on_commit=False, autocommit=True)))


Mapping arbitrary Selectables
-----------------------------

SQLSoup can map any SQLAlchemy :class:`sqlalchemy.sql.expression.Selectable` with the map
method. Let's map an :func:`sqlalchemy.sql.expression.select` object that uses an aggregate
function; we'll use the SQLAlchemy :class:`sqlalchemy.schema.Table` that SQLSoup
introspected as the basis. (Since we're not mapping to a simple
table or join, we need to tell SQLAlchemy how to find the
*primary key* which just needs to be unique within the select,
and not necessarily correspond to a *real* PK in the database.)::

    >>> from sqlalchemy import select, func
    >>> b = db.books._table
    >>> s = select([b.c.published_year, func.count('*').label('n')], from_obj=[b], group_by=[b.c.published_year])
    >>> s = s.alias('years_with_count')
    >>> years_with_count = db.map(s, primary_key=[s.c.published_year])
    >>> years_with_count.filter_by(published_year='1989').all()
    [MappedBooks(published_year=u'1989',n=1)]

Obviously if we just wanted to get a list of counts associated with
book years once, raw SQL is going to be less work. The advantage of
mapping a Select is reusability, both standalone and in Joins. (And if
you go to full SQLAlchemy, you can perform mappings like this directly
to your object models.)

An easy way to save mapped selectables like this is to just hang them on
your db object::

    >>> db.years_with_count = years_with_count

Python is flexible like that!

Raw SQL
-------

SQLSoup works fine with SQLAlchemy's text construct, described
in :ref:`sqlexpression_text`. You can also execute textual SQL
directly using the :meth:`.SQLSoup.execute` method, which corresponds to the
:meth:`sqlalchemy.orm.session.Session.execute` method on the underlying :class:`sqlalchemy.orm.session.Session`. Expressions here
are expressed like :func:`sqlalchemy.sql.expression.text` constructs, using named parameters
with colons::

    >>> rp = db.execute('select name, email from users where name like :name order by name', name='%Bhargan%')
    >>> for name, email in rp.fetchall(): print name, email
    Bhargan Basepair basepair+nospam@example.edu

Or you can get at the current transaction's connection using
:meth:`.SQLSoup.connection`. This is the raw connection object which can
accept any sort of SQL expression or raw SQL string passed to
the database::

    >>> conn = db.connection()
    >>> conn.execute("'select name, email from users where name like ? order by name'", '%Bhargan%')

Dynamic table names
-------------------

You can load a table whose name is specified at runtime with the
:meth:`.SQLSoup.entity` method:

    >>> tablename = 'loans'
    >>> db.entity(tablename) is db.loans
    True

:meth:`.SQLSoup.entity` also takes an optional schema argument. If none is
specified, the default schema is used.
