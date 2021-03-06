import pytest
from mock import MagicMock

from chalice_restful import Api, Resource, authorizer, cors, api_key_required


def test_that_cant_add_resource_class_itself():
    # Arrange.
    api = Api(MagicMock())

    # Act.
    add = lambda: api.add(Resource)

    # Assert.
    with pytest.raises(AssertionError):
        add()


def test_that_cant_add_not_resource_subclass():
    # Arrange.
    class NotResource: ...
    api = Api(MagicMock())

    # Act.
    add = lambda: api.add(NotResource)

    # Assert.
    with pytest.raises(AssertionError):
        add()


def test_that_cant_add_resource_without_route_field():
    # Arrange.
    class NonDecoratedResource(Resource): ...
    api = Api(MagicMock())

    # Act.
    add = lambda: api.add(NonDecoratedResource)

    # Assert.
    with pytest.raises(AssertionError):
        add()


def test_that_cant_add_resource_without_supported_methods():
    # Arrange.
    class SimpleResource(Resource):
        route = '/'

    api = Api(MagicMock())

    # Act.
    add = lambda: api.add(SimpleResource)

    # Assert.
    with pytest.raises(AssertionError):
        add()


def test_that_when_adding_resource_its_endpoints_are_added_to_chalice():
    # Arrange.
    class SimpleResource(Resource):
        route = '/'

        def get(): ...

    app = MagicMock()
    route = MagicMock()
    app.route = MagicMock(return_value=route)
    api = Api(app)

    # Act.
    api.add(SimpleResource)

    # Assert.
    app.route.assert_called_with('/', methods=['GET'])
    route.assert_called_with(SimpleResource.get)


def test_that_when_resource_has_cors_its_endpoints_are_added_with_cors():
    # Arrange.
    @cors
    class SimpleResource(Resource):
        route = '/'

        def get(): ...

    app = MagicMock()
    route = MagicMock()
    app.route = MagicMock(return_value=route)
    api = Api(app)

    # Act.
    api.add(SimpleResource)

    # Assert.
    app.route.assert_called_with('/', methods=['GET'], cors=True)


def test_that_when_resource_requires_api_key_its_endpoints_are_added_with_api_key_required():
    # Arrange.
    @api_key_required
    class SimpleResource(Resource):
        route = '/'

        def get(): ...

    app = MagicMock()
    route = MagicMock()
    app.route = MagicMock(return_value=route)
    api = Api(app)

    # Act.
    api.add(SimpleResource)

    # Assert.
    app.route.assert_called_with('/', methods=['GET'], api_key_required=True)


def test_that_when_resource_is_authorized_its_endpoints_are_added_with_authorizer():
    # Arrange.
    @authorizer('x')
    class SimpleResource(Resource):
        route = '/'

        def get(): ...

    app = MagicMock()
    route = MagicMock()
    app.route = MagicMock(return_value=route)
    api = Api(app)

    # Act.
    api.add(SimpleResource)

    # Assert.
    app.route.assert_called_with('/', methods=['GET'], authorizer='x')


def test_that_when_endpoint_is_authorized_it_is_added_with_authorizer():
    # Arrange.
    class SimpleResource(Resource):
        route = '/'

        @authorizer('x')
        def get(): ...

    app = MagicMock()
    route = MagicMock()
    app.route = MagicMock(return_value=route)
    api = Api(app)

    # Act.
    api.add(SimpleResource)

    # Assert.
    app.route.assert_called_with('/', methods=['GET'], authorizer='x')


def test_that_request_returns_chalice_current_request():
    # Arrange.
    app = MagicMock()
    app.current_request = 'Fake'
    api = Api(app)

    # Act.
    request = api.request

    # Assert.
    assert request == 'Fake'
