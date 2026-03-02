from rest_framework import serializers


class ReportFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()