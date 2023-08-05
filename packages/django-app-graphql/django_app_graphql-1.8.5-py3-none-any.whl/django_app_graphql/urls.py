from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django_app_graphql.conf import settings
import logging

urlpatterns = []

LOG = logging.getLogger(__name__)


def get_default_schema_from_ariadne():
    import ariadne
    from ariadne import gql, QueryType

    typedefs = gql("""
        type Query {
            hello: String!
        }
        """)
    query = QueryType()

    @query.field("hello")
    def resolve_hello(*_):
        return "Hello world!"

    return ariadne.make_executable_schema(typedefs, query)


def get_endpoint_from_ariadne(enable_graphiql: bool):
    from ariadne.contrib.django.views import GraphQLView
    from django_app_graphql.ariadne.schema import get_schema
    import ariadne
    from ariadne import gql, QueryType

    try:
        schema = get_schema()
    except Exception as e:
        LOG.error(e)
        schema = get_default_schema_from_ariadne()

    return GraphQLView.as_view(schema=schema, introspection=enable_graphiql)


def get_endpoint_from_graphene(enable_graphiql: bool):
    from graphene_django.views import GraphQLView
    return GraphQLView.as_view(graphiql=enable_graphiql)


backend = settings.DJANGO_APP_GRAPHQL["BACKEND_TYPE"]
enable_graphiql = settings.DJANGO_APP_GRAPHQL["EXPOSE_GRAPHIQL"]
if backend == "ariadne":
    view = get_endpoint_from_ariadne(enable_graphiql)
elif backend == "graphene":
    view = get_endpoint_from_graphene(enable_graphiql)
else:
    raise ValueError(f"backend must be ariadne or graphene")

urlpatterns.append(path(
    settings.DJANGO_APP_GRAPHQL["GRAPHQL_SERVER_URL"],
    csrf_exempt(view)
))

