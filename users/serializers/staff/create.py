from rest_framework import serializers
from ...models import Staff


class StaffCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ['email', 'department', 'employee_id']

    def validate_email(self, value):
        if Staff.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('This staff already exists')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        staff = Staff(**validated_data)
        staff.is_staff = True
        staff.save()
        return staff
