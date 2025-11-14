import pytest
import sys

@pytest.mark.skipif(sys.platform == "win32")  #Почему без reason Еррор
def test_buggy():
    assert 1 == 2
