from django.contrib import admin
from .models import *


class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


# Register your models here.

admin.site.register(Usuario),
admin.site.register(ProgramasUPN),
admin.site.register(InformacionBasicaUsuario),
admin.site.register(UsuarioProgramasUPN),
admin.site.register(ProgramasExternos)
