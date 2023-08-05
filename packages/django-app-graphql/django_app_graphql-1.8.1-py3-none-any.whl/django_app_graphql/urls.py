from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django_app_graphql.conf import settings

urlpatterns = []

backend = settings.DJANGO_APP_GRAPHQL["BACKEND_TYPE"]
if backend == "ariadne":
    from ariadne.contrib.django.views import GraphQLView
    from .ariadne import schema
    urlpatterns.append(path(settings.DJANGO_APP_GRAPHQL["GRAPHQL_SERVER_URL"],
                            csrf_exempt(GraphQLView.as_view(schema=schema.get_schema()))))
elif backend == "graphene":
    from graphene_django.views import GraphQLView
    urlpatterns.append(path(settings.DJANGO_APP_GRAPHQL["GRAPHQL_SERVER_URL"],
                            csrf_exempt(GraphQLView.as_view(graphiql=settings.DJANGO_APP_GRAPHQL["EXPOSE_GRAPHIQL"]))))
else:
    raise ValueError(f"backend must be ariadne or graphene")

