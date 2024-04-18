import os

from pytest import fixture

from r2d2_test.integration.infrastructure import R2d2Infrastructure

__all__ = [
    'websocket_url',
    'set_test_environment',
]


@fixture(scope='session')
def websocket_url() -> str:
    return R2d2Infrastructure.get_output(R2d2Infrastructure.R2D2_WEBSOCKET_URL)


@fixture(scope='session', autouse=True)
def set_test_environment() -> None:
    environment_vars = {
        'R2D2_SESSION_TABLE_NAME': R2d2Infrastructure.get_output(R2d2Infrastructure.R2D2_SESSION_TABLE_NAME),
        'R2D2_SESSION_TABLE_REGION': R2d2Infrastructure.get_output(R2d2Infrastructure.R2D2_SESSION_TABLE_REGION),
        'CONNECTIONS_URL': R2d2Infrastructure.get_output(R2d2Infrastructure.R2D2_CONNECTION_URL),
    }

    os.environ.update(
        {
            key: str(value)
            for key, value in environment_vars.items()
        }
    )

    yield

    # Clean up environment variables.
    for key in environment_vars.keys():
        if key in os.environ:
            os.unsetenv(key)
