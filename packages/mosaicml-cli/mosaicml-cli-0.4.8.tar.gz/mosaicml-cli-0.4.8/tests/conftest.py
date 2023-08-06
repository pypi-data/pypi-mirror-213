""" Conftest for Fixtures """
# Copyright 2021 MosaicML. All Rights Reserved.

import os

import pytest

from mcli import config

# Add the path of any pytest fixture files you want to make global
pytest_plugins = ['tests.fixtures', 'tests.cli.fixtures']


@pytest.fixture(scope='session', autouse=True)
def tests_setup_and_teardown():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    for env_var in (config.MCLI_MODE_ENV,):
        os.environ.pop(env_var, default=None)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)
