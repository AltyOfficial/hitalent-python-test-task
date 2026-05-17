from rest_framework import serializers

from server.apps.departments.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class DepartmentCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = Department
        fields = ['name', 'parent_id']

    def validate_name(self, value: str) -> str:
        return value.strip()

    def validate(self, attrs):
        parent_id = attrs.get('parent_id')
        if parent_id:
            if not Department.objects.filter(id=parent_id).exists():
                raise serializers.ValidationError({'parent_id': 'Нет подразделения с выбранным id.'})
        return attrs
    

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'hired_at', 'created_at']


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'created_at', 'updated_at']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    employees = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['department', 'employees', 'children']

    def get_department(self, obj: Department):
        return {
            'id': obj.id,
            'name': obj.name,
            'parent': obj.parent_id,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def get_employees(self, obj: Department):
        include_employees = self.context.get('include_employees', True)
        if not include_employees:
            return []
        
        return EmployeeListSerializer(
            obj.employees.all().order_by('-created_at'),
            many=True
        ).data

    def get_children(self, obj: Department):
        depth = self.context.get('depth', 1)
        if depth <= 1:
            return []

        children = obj.children.all()[:20]
        
        return DepartmentDetailSerializer(
            children,
            many=True,
            context={
                'depth': depth - 1,
                'include_employees': self.context.get('include_employees', True)
            }
        ).data
