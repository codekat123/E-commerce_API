from rest_framework.views import APIView
from ..serializers import ReportFilterSerializer
from users.permissions import IsVendor
from ..service import generate_csv_report_sales




class VendorReportAPIView(APIView):
    permission_classes = [IsVendor]

    def get(self, request, *args, **kwargs):
        serializer = ReportFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        return generate_csv_report_sales(
            vendor=request.user,
            start_date=start_date,
            end_date=end_date,
        )