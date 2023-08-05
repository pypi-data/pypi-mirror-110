from ariadne import gql
from django.apps import apps


def get_schema():
    """
    The function scans your project and apps and fetch all the *.graphql files.

    Then, it builds the schema
    :return:
    """

    files = []

    for app in apps.get_app_configs():
        yield app

    return gql("")


