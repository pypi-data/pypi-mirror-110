from ariadne import QueryType, MutationType

query = QueryType("Query")
"""
Decorator used to register query resolvers
"""
mutation = MutationType("Mutation")
"""
Decorator used to register mutation resolvers
"""