from rest_framework import serializers
from .models import User, Curso


class UserSerializer(serializers.ModelSerializer):
    cursos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password', 'id', 'cursos']


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
