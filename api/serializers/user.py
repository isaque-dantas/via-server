from rest_framework import serializers

from api.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'email': instance.email,
            'role': instance.role,
        }
