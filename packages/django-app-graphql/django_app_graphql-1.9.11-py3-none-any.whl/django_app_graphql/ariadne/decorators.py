from typing import Dict

from ariadne import QueryType, MutationType
from django_koldar_utils.functions import decorators

query = QueryType()
"""
Decorator used to register query resolvers
"""
mutation = MutationType()
"""
Decorator used to register mutation resolvers
"""