from django.template.defaulttags import url
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from schema import schema
from .views import LoginView, SignupView, SettingsView, EmailForm, Profile

app_name = 'users'

urlpatterns = [
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    re_path(r"^account/login/$", LoginView.as_view(), name="account_login"),
    re_path(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    re_path(r"^account/settings/$", SettingsView.as_view(), name="account_settings"),
    re_path(r"^account/", include("account.urls")),
    path("confirm_Email/", EmailForm, name="email"),
    path("account/profile/", Profile, name="profile"),
]