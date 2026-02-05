from rest_framework import serializers
from ...models import Staff


class StaffCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ['email','department','employee_id','password']

    def validate_email(self,value):
        if Staff.objects.filter(email_iexact=value).exists():
            raise serializers.ValidationError('this staff already exists')
        return value
    