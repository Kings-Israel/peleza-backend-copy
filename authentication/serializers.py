from authentication.models import ClientCompany, PelClient
from django.db import models
from django.http import request
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from main.models import user_has_permission


class AuthSerializer(serializers.Serializer):
    client_id = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ClientCompanySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("company_name", "company_industry", "company_country")
        model = ClientCompany


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = PelClient
        fields = ("name", "email")


class UserSerializer(serializers.ModelSerializer):
       
    client_parent_company = ClientCompanySerializer()

    class Meta:
        fields = ("client_id","client_company_id", "client_login_username", "client_password", "status", "client_pin", "client_first_name", "client_last_name", "client_mobile_number", "client_postal_address", "client_postal_code", "client_city", "client_parent_company")
        model = PelClient


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
