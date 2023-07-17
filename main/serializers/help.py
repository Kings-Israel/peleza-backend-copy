from rest_framework import serializers
from main.models.help import FormData

class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormData
        fields = "__all__"
