from rest_framework import serializers
from main.models.help import FormData, HelpSubject, HelpMessage, HelpResponse

class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormData
        fields = "__all__"

class HelpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpResponse
        fields = (
                "id",
                "response",
                "read_at",
                "created_at",
            )
        
class HelpMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpMessage
        fields = (
                "id",
                "message",
                "created_at",
            )

class HelpSubjectSerializer(serializers.ModelSerializer):
    messages = HelpMessageSerializer(read_only=True, many=True)
    responses = HelpResponseSerializer(read_only=True, many=True)
    
    class Meta:
        model = HelpSubject
        fields = (
                "id",
                "user",
                "subject",
                "messages",
                "responses",
                "created_at",
            )