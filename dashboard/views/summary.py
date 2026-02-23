from rest_framework.views import APIView
from rest_framework.response import Response
from users.permissions import IsVendor
from ..service import VendorDashboardService


class VendorSummaryView(APIView):

    permission_classes = [IsVendor]

    def get(self, request, *args, **kwargs):
        data = VendorDashboardService.get_summary(request.user)
        return Response(data)