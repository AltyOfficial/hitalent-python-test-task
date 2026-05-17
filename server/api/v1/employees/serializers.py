from rest_framework import serializers

from server.apps.departments.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'hired_at', 'created_at']
        read_only_fields = ['created_at']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'hired_at']
    
    def validate_full_name(self, value: str) -> str:
        return value.strip()
