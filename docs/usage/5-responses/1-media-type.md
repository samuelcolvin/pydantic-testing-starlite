# Media Type

You do not have to specify the `media_type` kwarg in the route handler function if the response should be JSON. But
if you wish to return a response other than JSON, you should specify this value. You can use
the `starlite.enums.MediaType` enum for this purpose:

```python
from starlite import MediaType, get


@get("/resources", media_type=MediaType.TEXT)
def retrieve_resource() -> str:
    return "The rumbling rabbit ran around the rock"
```

The value of the `media_type` kwarg affects both the serialization of response data and the generation of OpenAPI docs.
The above example will cause Starlite to serialize the response as a simple bytes string with a `Content-Type` header
value of `text/plain`. It will also set the corresponding values in the OpenAPI documentation.

MediaType has the following members:

- MediaType.JSON: `application/json`
- MediaType.TEXT: `text/plain`
- MediaType.HTML: `text/html`

You can also set any [IANA referenced](https://www.iana.org/assignments/media-types/media-types.xhtml) media type
string as the `media_type`. While this will still affect the OpenAPI generation as expected, you might need to handle
serialization using either a [custom response](10-custom-responses.md) with serializer or by serializing the value in
the route handler function.

## JSON Responses

As previously mentioned, the default `media_type` is `MediaType.JSON`. which supports the following values:

- dictionaries
- dataclasses from the standard library
- pydantic dataclasses
- pydantic models
- models from libraries that extend pydantic models
- numpy ndarray
- lists containing any of the above elements

Since Starlite uses the excellent (and super-fast!) [orjson](https://github.com/ijl/orjson#numpy) library to handle
JSON (also in requests), you can use the following values as part of your responses without issue:

- all UUIDs
- datetime classes
- numpy primitives and objects (see [orjson docs](https://github.com/ijl/orjson#numpy))

If you need to return other values and would like to extend serialization you can do
this [using Custom Responses](10-custom-responses.md).

## Text Responses

For `MediaType.TEXT`, route handlers should return a **string** or **bytes** value:

```python
from starlite import get, MediaType


@get(path="/health-check", media_type=MediaType.TEXT)
def health_check() -> str:
    return "healthy"
```

## HTML Responses

For `MediaType.HTML`, route handlers should return a **string** or **bytes** value that contains HTML:

```python
from starlite import get, MediaType


@get(path="/page", media_type=MediaType.HTML)
def health_check() -> str:
    return """
    <html>
        <body>
            <div>
                <span>Hello World!</span>
            </div>
        </body>
    </html>
    """
```

<!-- prettier-ignore -->
!!! tip
    It's a good idea to use a [templating engine](15-templating#template-responses) for more complex HTML responses
    and to write the [template](15-templating#template-responses) itself in a separate file rather than a string.
