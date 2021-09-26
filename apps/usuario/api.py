from rest_framework.response import Response
from rest_framework.views import APIView, View
from usuario.models import Usuario
from usuario.serializers import UsuarioSerializer

class UserAPIView(APIView):
    def get(self,request):
        users=Usuario.objects.all
        users_serialize = UsuarioSerializer(users, many=True)
        return Response(users_serialize.data)