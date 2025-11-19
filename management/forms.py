from django import forms

from .models import Departamento, Empleado, Proyecto, Tarea


class FechaInput(forms.DateInput):
    input_type = "date"


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ["nombre", "descripcion", "ubicacion"]


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ["nombre", "correo", "cargo", "fecha_contratacion", "departamento"]
        widgets = {
            "fecha_contratacion": FechaInput(),
        }


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            "nombre",
            "descripcion",
            "departamento",
            "responsable",
            "fecha_inicio",
            "fecha_fin",
            "presupuesto_estimado",
        ]
        widgets = {
            "fecha_inicio": FechaInput(),
            "fecha_fin": FechaInput(),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = [
            "titulo",
            "descripcion",
            "proyecto",
            "asignado_a",
            "estado",
            "prioridad",
            "fecha_entrega",
            "porcentaje_avance",
        ]
        widgets = {
            "fecha_entrega": FechaInput(),
        }
