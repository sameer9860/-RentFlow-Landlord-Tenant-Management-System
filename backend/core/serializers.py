from rest_framework import serializers


class AuthStatusSerializer(serializers.Serializer):
    is_authenticated = serializers.BooleanField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField(allow_null=True)
