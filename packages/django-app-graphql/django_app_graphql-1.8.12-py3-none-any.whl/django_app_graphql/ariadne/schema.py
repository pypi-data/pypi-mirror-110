import ariadne
from ariadne import gql, QueryType, MutationType
from django.apps import apps
from django_koldar_utils.functions import file_helpers
from graphql.type.schema import GraphQLSchema


def generate_schema_from_apps() -> GraphQLSchema:
    """
    The function scans your project and apps and fetch all the *.graphql files.

    Then, it builds the schema
    :return:
    """

    files = []

    for app in apps.get_app_configs():
        for graphql_file in file_helpers.get_all_files_ending_with(app.path, "graphql"):
            # load file content
            with open(graphql_file, mode="r", encoding="utf8") as f:
                content = f.read()
            files.append(content)
        # now we add all the schema

    typedefs = gql('\n'.join(files))

    return ariadne.make_executable_schema(typedefs, query, mutation)


