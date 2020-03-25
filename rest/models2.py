from django.db import models
from django.utils import timezone


class Tabla_test(models.Model):
    columna_uno = models.CharField(max_length=200)
    columna_dos = models.CharField(max_length=200)
    columna_tres = models.CharField(max_length=200)
    columna_cuatro = models.CharField(max_length=200)
# Create your models here.
# modelo usuarios


class user(models.Model):
    firs_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=150)  # email tambien es usuario
    password = models.TextField()  # encriptada
    # tipo 1: usuario comun, tipo 2: auxiliar, tipo 3: administrador
    tipo = models.IntegerField(max_length=1)
    # modelo auxiliares depende de usuarios
    image = models.ImageField(blank=True, null=True)
    ident = models.IntegerField(max_length=12, blank=True, null=True)  # numero de identificacion
    userPhone = models.CharField(max_length=60, blank=True, null=True)
    user_Address = models.TextField(blank=True, null=True)
    birthDay = models.DateField(blank=True, null=True)


class auxi(models.Model):
    id_user = models.ForeignKey('user', on_delete=models.CASCADE)

# modelo administrador depende de usuarios


class admin(models.Model):
    id_user = models.ForeignKey('user', on_delete=models.CASCADE)
    ident = models.IntegerField(max_length=12)  # numero de identificacion
    user_Address = models.TextField()
    birthDay = models.DateField()


class skills(models.Model):
    id_user = models.ForeignKey('user', on_delete=models.CASCADE)
    skill = models.TextField()


class tipo_mod(models.Model):
    id_user = models.ForeignKey('user', on_delete=models.CASCADE)
    modalidad = models.TextField()


class modalidad(models.Model):#Si es empresa o hogar
    nombre = models.CharField(max_length=100)


class tipo_servi(models.Model):#si es clasico, plata, oro
    nombre = models.CharField(max_length=100)


class agendado(models.Model):
    id_user = models.ForeignKey('user', on_delete=models.CASCADE)
    modalidad = models.IntegerField(max_length=1)
    tipo_servi = models.IntegerField(max_length=1)
    hora = models.TimeField()
    id_auxi = models.IntegerField()
    pers_Acargo = models.CharField(max_length=200)
    direccion = models.TextField()
    observaciones = models.TextField()
    lugar = models.CharField(max_length=100)
    estado = models.CharField(max_length=1)#si esta aceptada la orden o no, 0 no aprobado, 1 en espera, 2 aprobada para realizar
    realizado = models.CharField(max_length=1)#0 si aun no se realiza, 1 realizado


class fecha_agenda(models.Model):
    grupo = models.ForeignKey('agendado', on_delete=models.CASCADE)
    fecha = models.DateField()