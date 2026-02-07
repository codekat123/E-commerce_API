from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ...serializers import StaffCreateSerializer
from ...permissions import IsAdmin

User = get_user_model()

class CreateStaff(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffCreateSerializer
    permission_classes = [IsAuthenticated,IsAdmin]