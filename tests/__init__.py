import re

def eq_(a, b, msg=None):
    """Assert a == b, with repr messaging on failure."""
    assert a == b, msg or "%r != %r" % (a, b)

def ne_(a, b, msg=None):
    """Assert a != b, with repr messaging on failure."""
    assert a != b, msg or "%r == %r" % (a, b)

def assert_raises(except_cls, callable_, *args, **kw):
    try:
        callable_(*args, **kw)
        success = False
    except except_cls:
        success = True

    # assert outside the block so it works for AssertionError too !
    assert success, "Callable did not raise an exception"

def assert_raises_message(except_cls, msg, callable_, *args, **kwargs):
    try:
        callable_(*args, **kwargs)
        assert False, "Callable did not raise an exception"
    except except_cls as e:
        assert re.search(msg, str(e)), "%r !~ %s" % (msg, e)
        print(str(e))
