from rest_framework import serializers
from main.models.addUser import AddUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'added_by', 'company', 'role']
