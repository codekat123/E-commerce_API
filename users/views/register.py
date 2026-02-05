from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from serializers import (
    ClientRegisterSerializer,
    VendorRegisterSerializer,
)

serializer_map = {
    'client':ClientRegisterSerializer,
    'vendor':VendorRegisterSerializer
}

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self,request,*args,**kwargs):
        role = request.data.get('role')
        try:
            serializer_class = serializer_map[role]
        except KeyError:
            return Response(
                {'message':'you can either register as customer or merchant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'message':'your account have been activated successfully, please activate your account'
            },
            status=status.HTTP_201_CREATED,
        )