from rest_framework import serializers

from api.models.employee import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'password']

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'email': instance.email
        }
