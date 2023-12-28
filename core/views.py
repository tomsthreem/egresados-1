from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.template import Context
from django.contrib import messages
from django.http import JsonResponse
from .forms import *
from .models import *
from django.core.cache import cache
import csv


def home(request):
    form = InfoBasicForm()
    return render(request, "core/home.html", {"form": form})


def registro(request):
    url_name = request.resolver_match.url_name
    print(url_name)
    # return_url = "core/registro-egresado.html" if url_name == "registro-egresado" else "core/registro-administrativo.html"
    if request.method == "POST":
        form = RegistroFormulario(request.POST, url_name=url_name)
        if form.is_valid():
            print("Formulario Válido")
            usuario = form.save(commit=False)
            usuario.username = usuario.username.lower()
            if url_name == "registro-egresado":
                usuario.es_egresado = True
            else:
                usuario.es_administrativo = True
                form.fields['tipo_administrativo'].required = usuario.es_administrativo
                form.fields['facultad_administrativo'].required = usuario.es_administrativo
            usuario.save()
            auth_login(request, usuario)

            return redirect("perfil", id=request.user.id)  # redireccion
        else:
    
            print("Formulario Inválido")
            for field in form.errors:
                for error in form[field].errors:
                    print(f"Error en campo '{field}': {error}")
                    messages.error(request, f"Error en campo '{field}': {error}")

    else:
        form = RegistroFormulario(url_name=url_name)

    return render(request, "core/" + url_name + ".html", {"registerForm": form, "url_name": url_name})


def inicio(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(" Formulario Válido. ")
            auth_login(request, form.get_user())
            return redirect("perfil", id=request.user.id)
        else:
            messages.error(request, "Verifique sus credenciales")
    else:
        form = CustomAuthenticationForm()
    return render(request, "core/login.html", {"loginForm": form})


def perfil(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    return render(request, "core/perfil.html", {"usuario": usuario})

def obtener_datos_api():
    url = 'https://www.datos.gov.co/resource/gdxc-w37w.json'
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            departamentos, municipios = procesar_datos_api(respuesta.json())
            return departamentos, municipios
    except requests.RequestException:
        pass
    return [], []

def procesar_datos_api(datos):
    departamentos = set()
    municipios = set()
    for item in datos:
        departamentos.add(item['dpto'])
        municipios.add(item['nom_mpio'])
    return list(departamentos), list(municipios)

def leer_datos_csv(ruta_archivo):
    # Claves de caché
    cache_key_departamentos = 'departamentos_data'
    cache_key_municipios = 'municipios_data'

    # Intenta obtener los datos de la caché
    departamentos = cache.get(cache_key_departamentos)
    municipios = cache.get(cache_key_municipios)

    # Si no están en caché, lee del archivo CSV y almacena en caché
    if departamentos is None or municipios is None:
        departamentos = set()
        municipios = set()
        with open(ruta_archivo, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                departamentos.add(row['Nombre Departamento'])
                municipios.add(row['Nombre Municipio'])
        departamentos = sorted(departamentos)
        municipios = sorted(municipios)
        cache.set(cache_key_departamentos, departamentos)
        cache.set(cache_key_municipios, municipios)

    return departamentos, municipios

def cargar_municipios(request):
    departamento = request.GET.get('departamento')
    departamentos_municipios = leer_datos_csv('ruta/a/tu/archivo.csv')
    municipios = departamentos_municipios.get(departamento, [])
    return JsonResponse(municipios, safe=False)

def infoBasica(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    try:
        info_basica = InformacionBasicaUsuario.objects.get(usuario=usuario)
    except InformacionBasicaUsuario.DoesNotExist:
        info_basica = None

    ruta_csv = 'core/static/data/DIVIPOLA-_C_digos_municipios_20231227.csv'
    departamentos, municipios = leer_datos_csv(ruta_csv)

    if request.method == "POST":
        form = InfoBasicForm(request.POST, departamentos=departamentos, municipios=municipios, instance=info_basica)
        if info_basica is None:
            info_basica = form.save(commit=False)
            info_basica.usuario = usuario

        if form.is_valid():
            form.save()
            return render(request, "core/info-basica.html", {"usuario": usuario, "form": form, "form_saved": True})
        else:
            return render(request, "core/info-basica.html", {"usuario": usuario, "form": form, "form_errors": True})
    else:
        data_inicial = {
            "nombres": usuario.nombres,
            "primer_apellido": usuario.primer_apellido,
            "segundo_apellido": usuario.segundo_apellido,
            "documento": usuario.documento,
            "correo": usuario.email,
            
        }
        if info_basica: 
            info_basica.fecha_nacimiento = str(info_basica.fecha_nacimiento)
            
        form = InfoBasicForm(initial=data_inicial, departamentos=departamentos, municipios=municipios, instance=info_basica)

    return render(request, "core/info-basica.html", {"usuario": usuario, "form": form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProgramasUPN
from .forms import ProgramasUPNForm  # Asegúrate de haber creado este formulario

def formacionUPN(request):
    
    form = ProgramasUPNForm(request.POST)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('formacionUPN')  # Reemplaza con tu URL de redirección

    return render(request, "core/formacionUPN.html", {"form": form})

def salir(request):
    auth_logout(request)
    return render(request, "core/salir.html")


def get_programas(request):
    facultad = request.GET.get('facultad')
    tipo_formacion = request.GET.get('tipo_formacion')

    # Filtrar los programas basados en la facultad y el tipo de formación
    programas_filtrados = Programa.objects.filter(
        facultad=facultad, tipo_formacion=tipo_formacion
    )

    # Crear una lista de tuplas (value, text) para la respuesta JSON
    programas = [(programa.id, programa.nombre) for programa in programas_filtrados]

    return JsonResponse({'programas': programas})
