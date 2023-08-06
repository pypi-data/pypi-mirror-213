import pytest

import f3dasm_optimize


def test_add_one():
    assert f3dasm_optimize.add_one(1) == 2