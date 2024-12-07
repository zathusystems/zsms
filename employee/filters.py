from django_filters import rest_framework as filters
from .models import Employee

class EmployeeFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school', lookup_expr='exact')

    class Meta:
        model = Employee
        fields = ['school']
