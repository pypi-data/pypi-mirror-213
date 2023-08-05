import pytest

from ellar.common.constants import NOT_SET
from ellar.core.versioning import UrlPathAPIVersioning, VersioningSchemes as VERSIONING
from ellar.testing import Test

from .operations import mr

tm = Test.create_test_module(routers=(mr,))
app = tm.create_application()
app.enable_versioning(VERSIONING.URL, version_parameter="v")


@pytest.mark.parametrize(
    "path, expected_result",
    [
        ("/version", dict(version="default")),
        ("/v1/version", dict(version="v1")),
        ("/v2/version", dict(version="v2")),
        ("/v3/version", dict(version="v3")),
        ("/1/version", dict(version="v1")),
        ("/2/version", dict(version="v2")),
        ("/3/version", dict(version="v3")),
    ],
)
def test_url_route_versioning(path, expected_result):
    assert isinstance(app.versioning_scheme, UrlPathAPIVersioning)
    client = tm.get_test_client()
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.mark.parametrize(
    "path, default, expected_result",
    [
        # default is 1
        ("/version", "1", dict(version="default")),
        ("/v1/version", "1", dict(version="default")),
        ("/v2/version", "1", dict(version="v2")),
        ("/v3/version", "1", dict(version="v3")),
        # default is 2
        ("/version", "2", dict(version="default")),
        ("/v1/version", "2", dict(version="v1")),
        ("/v2/version", "2", dict(version="default")),
        ("/v3/version", "2", dict(version="v3")),
        # default is 3
        ("/version", "3", dict(version="default")),
        ("/v1/version", "3", dict(version="v1")),
        ("/v2/version", "3", dict(version="v2")),
        ("/v3/version", "3", dict(version="default")),
        # default is None or NOT_SET
        ("/version", NOT_SET, dict(version="default")),
        ("/v1/version", NOT_SET, dict(version="v1")),
        ("/v2/version", NOT_SET, dict(version="v2")),
        ("/v3/version", NOT_SET, dict(version="v3")),
    ],
)
def test_url_route_versioning_with_default_version(path, default, expected_result):
    app.enable_versioning(
        VERSIONING.URL,
        default_version=default,
    )
    client = tm.get_test_client()
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.mark.parametrize(
    "path",
    [
        "/4/version",
        "/v1.0/version",
        "/v2.0/version",
        "/v3.0/version",
        "/1.0/version",
        "/2.0/version",
        "/3.0/version",
    ],
)
def test_url_route_versioning_not_found(path):
    app.enable_versioning(VERSIONING.URL, version_parameter="v")
    client = tm.get_test_client()

    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid version in URL path."}
