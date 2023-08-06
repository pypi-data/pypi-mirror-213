#! /usr/bin/env python

import pathlib
import re

# make sure the testing is working.
import pytest

import p2g


this_path = pathlib.Path(__file__)
golden_dir = this_path.parent / "golden"

# gold file is there, but broken.
# check creation of got file.

simple_xfail1_got = golden_dir / "test_simple_xfail1.got"
simple_xfail1_nc = golden_dir / "test_simple_xfail1.nc"


@p2g.check_golden()
@pytest.mark.xfail()
def test_simple_xfail1():
    simple_xfail1_nc.write_text("fail")
    p2g.com("A comment")
    CURSOR = p2g.Fixed(addr=100)
    CURSOR.x = 9


def test_native_check_and_remove_golden():
    assert simple_xfail1_got.read_text() == (
        "( A comment )\n( CURSOR.x = 9                  )\n  #100= 9."
    )
    simple_xfail1_nc.unlink()
    simple_xfail1_got.unlink()


p2g.must_be("err")


def test_simple_ok():
    print("WORKING")
    a = 3


# simple fn to output to stdout
def tolist_worker():
    p2g.Fixed(2, addr=100)


# two phases 'cause fixtures don't work on interp functions.
def test_native_tolist():
    got = p2g.walk.compile2g("tolist_worker", __file__, job_name=None, in_pytest=True)

    r = "#100" in got[1]
    assert r


# test what happens when file is no there.
make_golden_path = golden_dir / "test_native_transitory_golden.nc"


# output file not there, so test fails,
# but file is created
@p2g.check_golden()
def test_native_transitory_golden():
    CURSOR = p2g.Fixed(addr=100)
    CURSOR.x = 9


# # so can be tested here.
def test_native_golden_exists():
    assert make_golden_path.exists()
    make_golden_path.unlink()


meta_decorate_seed = golden_dir / "test_decorate_seed.decorator"


def test_native_remove_seed():
    meta_decorate_seed.unlink(missing_ok=True)
    assert not meta_decorate_seed.exists()


# the force inserts an error  in the output
# so the test fails, but generates them
# error output.

meta_decorator_path = golden_dir / "test_native_decorate_seed.decorator"


@p2g.must_be("FORCE")
def test_native_decorate_seed():
    CURSOR = p2g.Fixed(17, addr=100)


def test_native_seed_exists():
    print("GOT ", meta_decorate_seed)
    assert meta_decorator_path.exists()
    meta_decorator_path.unlink()


#    assert False


# expected fail        test_broken()
