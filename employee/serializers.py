from rest_framework import serializers
from schooladminstration.models import Institution
from .models import Employee

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()  # To include school details in employee serialization

    class Meta:
        model = Employee
        fields = ['id', 'name', 'position', 'salary', 'school']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # Flatten the school field for simplicity
    #     representation['school'] = instance.school.id
    #     return representation

    # def update(self, instance, validated_data):
    #     school_data = validated_data.pop('school', None)
    #     if school_data:
    #         instance.school_id = school_data
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.position = validated_data.get('position', instance.position)
    #     instance.salary = validated_data.get('salary', instance.salary)
    #     instance.save()
    #     return instance
