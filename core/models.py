import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

import random
import string
from datetime import datetime


class Usuario(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    tipo_doc = models.CharField(max_length=20)
    documento = models.CharField(max_length=11)
    terminos = models.BooleanField(default=False)
    es_administrativo = models.BooleanField(default=False, blank=True)
    tipo_administrativo = models.CharField(max_length=100)
    facultad_administrativo = models.CharField(max_length=100)
    es_egresado = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # se usa timestamp + 5 numeros random para generar los ID
            timestamp = str(int(datetime.now().timestamp()))
            random_numbers = "".join(random.choices(string.digits, k=5))
            self.id = timestamp + random_numbers
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "Usuario"


class InformacionBasicaUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=50, default = "")
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    documento = models.CharField(max_length=11)
    sexo = models.CharField(max_length=20, default = "")
    grupo_etnico = models.CharField(max_length=50,  default = "")
    pais_nacimiento = models.CharField(max_length=100)
    depa_nacimiento = models.CharField(max_length=100, blank=True, null=True)
    mun_nacimiento = models.CharField(max_length=100, blank=True, null=True)    
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado_civil = models.CharField(max_length=50, default = "")
    discapacidad = models.CharField(max_length=100, blank=True, null=True)
    pais_res = models.CharField(max_length=100, default = "")
    depa_res = models.CharField(max_length=100, blank=True, null=True)
    mun_res = models.CharField(max_length=100, blank=True, null=True)
    direccion_residencia = models.CharField(max_length=100, blank=True)
    correo = models.EmailField()    
    correo_alternativo = models.EmailField(blank=True, null=True)
    telefono_principal = models.CharField(max_length=10, blank=True)
    telefono_alternativo = models.CharField(max_length=17, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.primer_apellido}"  # Create your models here.

    class Meta:
        verbose_name = "Info Basica"
        verbose_name_plural = "Compilado Info"
        db_table = "Info Basica"


class ProgramasUPN(models.Model):
    programa = models.CharField(max_length=100)
    tipo_formacion = models.CharField(max_length=100)
    facultad = models.CharField(max_length=100)  # Nombre de la facultad
    titulo_obtenido = models.CharField(max_length=100)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)  # Título que se obtiene al completar el programa

    def __str__(self):
        return f"{self.programa} - {self.titulo_obtenido}"

    class Meta:
        verbose_name = "Programa UPN"
        verbose_name_plural = "Programas UPN"
        db_table = "ProgramasUPN"


class UsuarioProgramasUPN(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    programa_upn = models.ForeignKey(ProgramasUPN, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Usuario Programa UPN"
        verbose_name_plural = "Usuarios Programas UPN"
        db_table = "UsuarioProgramasUPN"


class ProgramasExternos(models.Model):
    tipo_titulo = models.CharField(max_length=100)
    programa_externo = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)  # Nombre de la institución
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_programa} - {self.tipo_titulo} - {self.institucion}"

    class Meta:
        verbose_name = "Programa Externo"
        verbose_name_plural = "Programas Externos"
        db_table = "ProgramasExternos"


class FormacionAcademica(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    programa_upn = models.ForeignKey(
        ProgramasUPN, on_delete=models.CASCADE, null=True, blank=True
    )
    programa_externo = models.ForeignKey(
        ProgramasExternos, on_delete=models.CASCADE, null=True, blank=True
    )
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Formación Académica"
        verbose_name_plural = "Formaciones Académicas"
        db_table = "FormacionAcademica"

