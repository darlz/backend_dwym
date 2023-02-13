from django.contrib.auth.models import User
from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    estudiantes = models.ManyToManyField(
        User, related_name='cursos', blank=True)
