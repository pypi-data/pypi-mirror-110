from typing import Dict

from ariadne import QueryType, MutationType, ObjectType
from django_koldar_utils.functions import decorators

query = ObjectType("Query")
"""
Decorator used to register query resolvers
"""
mutation = MutationType()
"""
Decorator used to register mutation resolvers
"""