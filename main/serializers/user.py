from rest_framework import serializers
from authentication.models import PelClient

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PelClient
        fields = "__all__"
