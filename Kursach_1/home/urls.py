from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import poster, event, ticket, mes
from graphene_django.views import GraphQLView
from schema import schema

app_name = 'home'
urlpatterns = [
    path('', poster, name='home'),
    path('event/<id>', event, name='event'),
    path('ticket/<id>', ticket, name='ticket'),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('mes/', mes, name="mes")

]