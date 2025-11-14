from datetime import time

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default='chrome',
        choices=("chrome", "firefox")
    )


@pytest.fixture
def browser(request):
    return request.config.getoption("--browser")

@pytest.mark.skipif()
def test_slow():
    time.sleep(3)
