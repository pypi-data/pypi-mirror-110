import ariadne
from ariadne import gql, QueryType, MutationType
from django.apps import apps
from django_koldar_utils.functions import file_helpers
from graphql.type.schema import GraphQLSchema

from django_app_graphql.ariadne import decorators

import logging

from django_app_graphql.ariadne.AbstractScalarType import AbstractScalarType

LOG = logging.getLogger(__name__)


def generate_schema_from_apps() -> GraphQLSchema:
    """
    The function scans your project and apps and fetch all the *.graphql files.

    Then, it builds the schema
    :return:
    """

    files = []

    for app in apps.get_app_configs():
        LOG.info(f"Inspecting app {app.verbose_name} at {app.path}")
        for graphql_file in file_helpers.get_all_files_ending_with(app.path, "graphql"):
            LOG.info(f"Including graphql file {graphql_file}")
            # load file content
            with open(graphql_file, mode="r", encoding="utf8") as f:
                content = f.read()
            files.append(content)
        # now we add all the schema

    typedefs = gql('\n'.join(files))
    LOG.info(f"number of query resolvers detected: {len(decorators.query._resolvers)}")
    LOG.info(f"number of mutation resolvers detected: {len(decorators.mutation._resolvers)}")

    if len(decorators.query._resolvers) == 0:
        LOG.warning(f"No queries detected. Adding a dummy one")
        typedefs = """
        type Query {
            dummyQuery: Int!
        }
        """ + typedefs

        @decorators.query.field("dummyQuery")
        def resolve_dummyQuery(_, info, **kwargs):
            return 42

    if len(decorators.mutation._resolvers) == 0:
        LOG.warning(f"No mutations detected. Adding a dummy one")
        typedefs = """
        type Mutation {
            dummyMutation: Boolean!
        }
        """ + typedefs

        @decorators.mutation.field("dummyMutation")
        def resolve_dummyMutation(_, info, **kwargs):
            return True

    LOG.info(f"Scalars resolvers detected: {list(map(lambda x: x.name, AbstractScalarType.get_all_registered_scalars()))}")

    return ariadne.make_executable_schema(
        typedefs,
        decorators.query,
        decorators.mutation,
        *AbstractScalarType.get_all_registered_scalars()
    )


