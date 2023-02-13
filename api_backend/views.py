from .models import Curso
from .serializers import UserSerializer, CursoSerializer
from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status, views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data.get("password"))
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        for key, value in serializer.validated_data.items():
            setattr(instance, key, value)
        if serializer.validated_data.get("password"):
            instance.set_password(serializer.validated_data.get("password"))
        instance.save()
        return Response(serializer.data)


class CursoView(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class RegistroView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['usuario']
            curso_id = request.data['curso']
            user = User.objects.get(id=user_id)
            curso = Curso.objects.get(id=curso_id)
            curso.estudiantes.add(user)
            curso.save()

        except (User.DoesNotExist, Curso.DoesNotExist):
            return Response({'message': f'No se encontró el usuario o curso especificado'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'Parámetros incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Agregado correctamente'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            user_id = request.data['usuario']
            curso_id = request.data['curso']
            user = User.objects.get(id=user_id)
            curso = Curso.objects.get(id=curso_id)
            curso.estudiantes.remove(user)
            curso.save()

        except (User.DoesNotExist, Curso.DoesNotExist):
            return Response({'message': f'No se encontró el usuario o curso especificado'}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'Parámetros incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Eliminado correctamente'}, status=status.HTTP_200_OK)
