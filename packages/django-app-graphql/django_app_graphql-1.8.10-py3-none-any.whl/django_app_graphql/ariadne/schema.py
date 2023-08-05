import ariadne
from ariadne import gql, QueryType
from django.apps import apps
from graphql.type.schema import GraphQLSchema


def generate_schema_from_apps() -> GraphQLSchema:
    """
    The function scans your project and apps and fetch all the *.graphql files.

    Then, it builds the schema
    :return:
    """

    files = []

    for app in apps.get_app_configs():
        #yield app

    typedefs = gql('\n'.join(files))
    query = QueryType()

    return ariadne.make_executable_schema(typedefs, query)


