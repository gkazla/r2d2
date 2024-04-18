from pytest import ExitCode

# noinspection PyUnresolvedReferences
from r2d2_test.integration.fixtures import *
from r2d2_test.integration.infra_create import inf_create
from r2d2_test.integration.infra_destroy import inf_destroy

MAX_PARALLEL_DEPLOYMENTS = 5


def pytest_sessionstart(session):
    inf_create(MAX_PARALLEL_DEPLOYMENTS)


def pytest_sessionfinish(session, exitstatus):
    if ExitCode(exitstatus) == ExitCode.OK:
        inf_destroy(MAX_PARALLEL_DEPLOYMENTS)
