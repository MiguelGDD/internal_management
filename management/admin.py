from django.contrib import admin

from . import models


@admin.register(models.Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "creado")
    search_fields = ("nombre", "ubicacion")


@admin.register(models.Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cargo", "departamento", "correo")
    search_fields = ("nombre", "correo", "cargo")
    list_filter = ("departamento",)


@admin.register(models.Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento", "fecha_inicio", "fecha_fin")
    search_fields = ("nombre", "descripcion")
    list_filter = ("departamento",)
    autocomplete_fields = ("responsable",)


@admin.register(models.Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "proyecto",
        "estado",
        "prioridad",
        "fecha_entrega",
        "porcentaje_avance",
    )
    list_filter = ("estado", "prioridad", "proyecto")
    search_fields = ("titulo", "descripcion")
    autocomplete_fields = ("proyecto", "asignado_a")
