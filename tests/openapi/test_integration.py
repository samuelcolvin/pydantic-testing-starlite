import yaml
from orjson import loads
from pydantic_openapi_schema.utils import construct_open_api_with_schema_class
from starlette.status import HTTP_200_OK

from starlite.app import DEFAULT_OPENAPI_CONFIG
from starlite.enums import OpenAPIMediaType
from starlite.testing import create_test_client
from tests.openapi.utils import PersonController, PetController


def test_openapi_yaml() -> None:
    with create_test_client([PersonController, PetController], openapi_config=DEFAULT_OPENAPI_CONFIG) as client:
        assert client.app.openapi_schema
        openapi_schema = client.app.openapi_schema
        assert openapi_schema.paths
        response = client.get("/schema/openapi.yaml")
        assert response.status_code == HTTP_200_OK
        assert response.headers["content-type"] == OpenAPIMediaType.OPENAPI_YAML.value
        assert yaml.safe_load(response.content) == construct_open_api_with_schema_class(client.app.openapi_schema).dict(
            by_alias=True, exclude_none=True
        )


def test_openapi_json() -> None:
    with create_test_client([PersonController, PetController], openapi_config=DEFAULT_OPENAPI_CONFIG) as client:
        assert client.app.openapi_schema
        openapi_schema = client.app.openapi_schema
        assert openapi_schema.paths
        response = client.get("/schema/openapi.json")
        assert response.status_code == HTTP_200_OK
        assert response.headers["content-type"] == OpenAPIMediaType.OPENAPI_JSON.value
        assert response.json() == loads(
            construct_open_api_with_schema_class(client.app.openapi_schema).json(by_alias=True, exclude_none=True)
        )
