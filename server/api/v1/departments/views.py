from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from server.apps.departments.models import Department
from server.api.v1.departments.serializers import (
    DepartmentSerializer,
    DepartmentCreateSerializer,
    DepartmentDetailSerializer
)
from server.api.v1.employees.serializers import EmployeeCreateSerializer


@extend_schema(tags=['Department'])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentCreateSerializer
        return DepartmentSerializer
    
    def update(self, request: Request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()

            detail_serializer = DepartmentDetailSerializer(
                instance,
                context={'request': request},
            )
            return Response(detail_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()

        depth = int(request.query_params.get('depth', 1))
        depth = min(max(depth, 1), 5)
        include_employees = request.query_params.get('include_employees', 'true').lower() == 'true'

        serializer = DepartmentDetailSerializer(
            instance,
            context={
                'depth': depth,
                'include_employees': include_employees,
                'request': request
            }
        )

        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='employees')
    def add_employee(self, request: Request, pk=None):
        department = self.get_object()
        serializer = EmployeeCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(department=department)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)