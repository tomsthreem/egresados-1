from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import requests

from .models import *
from .views import *

class RegistroFormulario(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            "username",
            "tipo_doc",
            "documento",
            "nombres",
            "primer_apellido",
            "segundo_apellido",
            "email",
            "terminos",
            "tipo_administrativo",
            "facultad_administrativo",
        ]
    TIPO_DOCUMENTO_OPCIONES = [
        ('', 'Selecciona un Tipo de Documento *'), # Opción por defecto
        ('CC', 'Cedula de Ciudadania'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cedula Extranjeria'),
        ('RC', 'Registro Civil'),
        ('NIT', 'NIT'),
        ('OTRO', 'Otro'),
    ]

    TIPO_ADMINISTRATIVO_OPCIONES = [
        ('', 'Selecciona un tipo administrativo *'),
        ('Funcionario Facultad', 'Funcionario Facultad'),
        ('Administrador Proyectos', 'Administrador Proyectos'),
        ('Funcionario SAE', 'Funcionario SAE'),
        ('Subdirección Sistemas', 'Subdirección Sistemas'),
        ('Otro', 'Otro'),
    ]

    FACULTAD_OPCIONES = [
        ('', 'Selecciona una facultad *'),
        ('Bellas Artes', 'Bellas Artes'),
        ('Ciencia y Tecnología', 'Ciencia y Tecnología'),
        ('Educación', 'Educación'),
        ('Educación Física', 'Educación Física'),
        ('Humanidades', 'Humanidades'),
        ('No pertenece a ninguna facultad', 'No pertenece a ninguna facultad'),
    ]

    tipo_administrativo = forms.ChoiceField(choices=TIPO_ADMINISTRATIVO_OPCIONES, required=False)
    facultad_administrativo = forms.ChoiceField(choices=FACULTAD_OPCIONES, required=False)
    tipo_doc = forms.ChoiceField(choices=TIPO_DOCUMENTO_OPCIONES)

    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name', None) 
        super().__init__(*args, **kwargs)
        print("Inicial - tipo_administrativo required:", self.fields['tipo_administrativo'].required)
        print("Inicial - facultad_administrativo required:", self.fields['facultad_administrativo'].required)   

        for field_name, field in self.fields.items():
            if field_name not in [
                "segundo_apellido",
                "es_administrativo",
                "es_egresado",
            ]:
                field.required = True
        if url_name == "registro-egresado":
            print("Form Egresado")
            self.fields['tipo_administrativo'].required = False
            self.fields['facultad_administrativo'].required = False
        else:
            print("Form Administrativo")
            self.fields['tipo_administrativo'].required = True
            self.fields['facultad_administrativo'].required = True

        print("Inicial2 - tipo_administrativo required:", self.fields['tipo_administrativo'].required)
        print("Inicial2 - facultad_administrativo required:", self.fields['facultad_administrativo'].required)   
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email

    def clean_documento(self):
        documento = self.cleaned_data['documento']
        if Usuario.objects.filter(documento=documento).exists():
            raise ValidationError("Este documento ya está registrado.")
        return documento


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        labels = {"username": "Usuario", "password1": "Contraseña"}
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "password1": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Convertir el nombre de usuario a minúsculas
        return username.lower() if username else ""


class InfoBasicForm(forms.ModelForm):
    class Meta:
        model = InformacionBasicaUsuario

        fields = [
            "nombres",
            "primer_apellido",
            "segundo_apellido",
            "documento",
            "sexo",
            "grupo_etnico",
            "pais_nacimiento",
            "depa_nacimiento",
            "mun_nacimiento",
            "fecha_nacimiento",
            "estado_civil",
            "discapacidad",
            "pais_res",
            "depa_res",
            "mun_res",
            "direccion_residencia",
            "correo",
            "correo_alternativo",
            "telefono_principal",
            "telefono_alternativo",
        ]
        labels = {
            "nombres": "Nombres",
            "primer_apellido": "Primer Apellido",
            "segundo_apellido": "Segundo Apellido",
            "documento": "Documento",
            "sexo": "Sexo",
            "grupo_etnico": "Grupo Étnico",
            "pais_nacimiento": "País de Nacimiento",
            "depa_nacimiento": "Departamento de Nacimiento",
            "mun_nacimiento": "Municipio de Nacimiento",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "estado_civil": "Estado Civil",
            "discapacidad": "Discapacidad",
            "pais_res": "País de Residencia",
            "depa_res": "Departamento de Residencia",
            "mun_res": "Municipio de Residencia",
            "direccion_residencia": "Dirección de Residencia",
            "correo": "Correo",
            "correo_alternativo": "Correo Alternativo",
            "telefono_principal": "Teléfono Principal",
            "telefono_alternativo": "Teléfono Alternativo",
        }
        widgets = {
            "nombres": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "primer_apellido": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "segundo_apellido": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "documento": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),            
            "pais_nacimiento": forms.TextInput(attrs={"class": "form-control"}),
            "depa_nacimiento": forms.TextInput(attrs={"class": "form-control"}),
            "mun_nacimiento": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "data-inputmask-alias":"datetime", "data-inputmask-inputformat":"dd/mm/yyyy", "data-mask":"", "inputmode":"numeric" ,"type":"date"}),
            "pais_res": forms.TextInput(attrs={"class": "form-control"}),
            "depa_res": forms.TextInput(attrs={"class": "form-control"}),
            "mun_res": forms.TextInput(attrs={"class": "form-control"}),
            "direccion_residencia": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "correo_alternativo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono_principal": forms.TextInput(attrs={"class": "form-control"}),
            "telefono_alternativo": forms.TextInput(attrs={"class": "form-control"}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'grupo_etnico': forms.Select(attrs={'class': 'form-control'}),
            'discapacidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        departamentos = kwargs.pop('departamentos', [])
        municipios = kwargs.pop('municipios', [])
        super(InfoBasicForm, self).__init__(*args, **kwargs)

        self.fields['depa_nacimiento'].choices = [(dep, dep) for dep in departamentos]
        self.fields['mun_nacimiento'].choices = [(mun, mun) for mun in municipios]
        self.fields['depa_res'].choices = [(dep, dep) for dep in departamentos]
        self.fields['mun_res'].choices = [(mun, mun) for mun in municipios]
    
    ESTADO_CIVIL_OPCIONES = [
        ('', 'Seleccione una opción'),
        ('casado (a)', 'Casado (a)'),
        ('divorciado (a)', 'Divorciado (a)'),
        ('separado (a)', 'Separado (a)'),
        ('soltero (a)', 'Soltero (a)'),
        ('viudo (a)', 'Viudo (a)'),
        ('unión libre', 'Unión Libre'),
        ('no_definido', 'No Definido'),
    ]

    DISCAPACIDAD_OPCIONES = [
        ('', 'Seleccione una opción'),
        ('auditiva', 'Auditiva'),
        ('fisica', 'Física'),
        ('intelectual', 'Intelectual'),
        ('psicosocial', 'Psicosocial'),
        ('sordoceguera', 'Sordoceguera'),
        ('visual', 'Visual'),
        ('discapacidades_multiples', 'Discapacidades Múltiples'),
        ('ninguna', 'No tengo ninguna discapacidad'),
        ]

    GRUPO_ETNICO_OPCIONES = [
        ('', 'Seleccione una opción'),  # Valor por defecto
        ('indigena', 'Indígena'),
        ('afrocolombiano', 'Afrocolombiano'),
        ('raizal', 'Raizal'),
        ('palenquero', 'Palenquero'),
        ('gitano', 'Gitano'),
        ('mestizo', 'Mestizo'),
        ('ninguna', 'No pertenece a ningún grupo étnico'),
        ('otro', 'Otro'),
        ]
    SEXO_OPCIONES = [
        ('', 'Seleccione una opción'),
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('no_definido', 'No Definido'),
    ]

    with open('core/static/data/Paises_list.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]
    
    # Crea una lista de opciones en formato ('valor', 'etiqueta')
    opciones_paises = [(line.split(',')[0].strip('"'), line.split(',')[0].strip('"')) for line in lines]

    # Agrega una opción vacía al principio si lo deseas
    opciones_paises.insert(0, ('', 'Seleccione un país'))

    grupo_etnico = forms.ChoiceField(choices=GRUPO_ETNICO_OPCIONES, required=True)
    estado_civil = forms.ChoiceField(choices=ESTADO_CIVIL_OPCIONES, required=True)
    discapacidad = forms.ChoiceField(choices=DISCAPACIDAD_OPCIONES, required=True)
    sexo = forms.ChoiceField(choices=SEXO_OPCIONES, required=True)
    pais_nacimiento = forms.ChoiceField(choices=opciones_paises, required=True)
    pais_res = forms.ChoiceField(choices=opciones_paises, required=True)


class UsuarioProgramasUPNForm(forms.ModelForm):
    class Meta:
        model = UsuarioProgramasUPN
        fields = ['usuario', 'programa_upn']

class ProgramasExternosForm(forms.ModelForm):
    class Meta:
        model = ProgramasExternos
        fields = ['tipo_titulo', 'programa_externo', 'institucion', 'usuario']


def cargar_choices_desde_archivo(ruta_archivo):
    with open('core/static/data/programas.txt', 'r',encoding='utf-8') as file:
        lines = file.readlines()
        facultad_choices = set()
        titulo_obtenido_choices = set()
        tipo_formacion_choices = set()

        for line in lines:
            partes = line.strip().split(', ')
            if len(partes) == 4:
                facultad, tipo_formacion, programa, titulo_obtenido = partes
                facultad_choices.add((facultad, facultad))
                titulo_obtenido_choices.add((titulo_obtenido, titulo_obtenido))
                tipo_formacion_choices.add((tipo_formacion, tipo_formacion))

        return {
            "facultad": list(facultad_choices),
            "titulo_obtenido": list(titulo_obtenido_choices),
            "tipo_formacion": list(tipo_formacion_choices),
            "programa": [(programa, f"{programa}") for programa in set(parte[2] for parte in (line.strip().split(', ') for line in lines))]
        }

class ProgramasUPNForm(forms.ModelForm):

    choices = cargar_choices_desde_archivo('core/static/data/programas.txt')
    facultad = forms.ChoiceField(choices=choices['facultad'])
    tipo_formacion = forms.ChoiceField(choices=choices['tipo_formacion'])
    titulo_obtenido = forms.ChoiceField(choices=choices['titulo_obtenido'])
    programa = forms.ChoiceField(choices=choices['programa'])

    class Meta:
        model = ProgramasUPN
        fields = ['programa', 'tipo_formacion', 'facultad', 'titulo_obtenido', 'fecha_inicio', 'fecha_fin']

        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
    # facultad = forms.ChoiceField(choices=FACULTAD_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # tipo_formacion = forms.ChoiceField(choices=TIPO_FORMACION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # programa = forms.ChoiceField(choices=PROGRAMAS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # titulo_obtenido = forms.ChoiceField(choices=TITULO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    # class Meta:
    #     model = ProgramasUPN
    #     fields = ['facultad', 'tipo_formacion', 'programa', 'titulo_obtenido', 'fecha_inicio', 'fecha_fin']
        
    #     labels = {
    #         "facultad": "Facultad",
    #         "tipo_formacion": "Tipo de Formación",
    #         "programa": "Programa",
    #         "titulo_obtenido": "Título Obtenido",
    #         "fecha_inicio": "Fecha de Inicio",
    #         "fecha_fin": "Fecha de Fin",
    #     }

    #     widgets = {
    #         "programa": forms.TextInput(attrs={"class": "form-control"}),
    #         "titulo_obtenido": forms.TextInput(attrs={"class": "form-control"}),
    #         "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    #         "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    #     }


