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
    unread_responses = serializers.SerializerMethodField(method_name="get_unread_responses")

    def get_unread_responses(self, obj):
        return HelpResponse.objects.filter(subject_id=obj.id, read_at=None).count()

    class Meta:
        model = HelpSubject
        fields = (
                "id",
                "user",
                "subject",
                "messages",
                "responses",
                "created_at",
                "unread_responses",
            )