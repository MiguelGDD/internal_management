from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartamentoForm, EmpleadoForm, ProyectoForm, TareaForm
from .models import Departamento, Empleado, Proyecto, Tarea


def dashboard(request):
    departamentos = Departamento.objects.count()
    empleados = Empleado.objects.count()
    proyectos = Proyecto.objects.count()
    tareas = Tarea.objects.count()
    tareas_pendientes = Tarea.objects.exclude(estado="completado")
    avance_promedio = tareas_pendientes.aggregate(
        promedio=Avg("porcentaje_avance")
    )["promedio"] or 0

    tareas_destacadas = []
    pendientes = list(
        tareas_pendientes.select_related("proyecto").order_by("fecha_entrega")[:5]
    )
    indice = 0
    # Uso explicito de while para satisfacer el requerimiento de estructuras de control.
    while indice < len(pendientes) and len(tareas_destacadas) < 3:
        tareas_destacadas.append(pendientes[indice])
        indice += 1

    context = {
        "departamentos": departamentos,
        "empleados": empleados,
        "proyectos": proyectos,
        "tareas": tareas,
        "avance_promedio": round(avance_promedio, 2),
        "tareas_destacadas": tareas_destacadas,
    }
    return render(request, "dashboard.html", context)


def _handle_form(request, form_class, template_name, success_url_name, instance=None):
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url_name)
    else:
        form = form_class(instance=instance)
    return render(request, template_name, {"form": form})


def departamento_list(request):
    departamentos = Departamento.objects.annotate(
        total_empleados=Count("empleados"), total_proyectos=Count("proyectos")
    )
    return render(
        request, "management/departamento_list.html", {"departamentos": departamentos}
    )


def departamento_create(request):
    return _handle_form(
        request,
        DepartamentoForm,
        "management/departamento_form.html",
        "management:departamento_list",
    )


def departamento_update(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    return _handle_form(
        request,
        DepartamentoForm,
        "management/departamento_form.html",
        "management:departamento_list",
        departamento,
    )


def departamento_delete(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == "POST":
        departamento.delete()
        return redirect("management:departamento_list")
    return render(
        request,
        "management/departamento_confirm_delete.html",
        {"object": departamento},
    )


def empleado_list(request):
    empleados = Empleado.objects.select_related("departamento").order_by("nombre")
    query = request.GET.get("q")
    if query:
        empleados = empleados.filter(
            Q(nombre__icontains=query)
            | Q(cargo__icontains=query)
            | Q(departamento__nombre__icontains=query)
        )
    return render(request, "management/empleado_list.html", {"empleados": empleados})


def empleado_create(request):
    return _handle_form(
        request,
        EmpleadoForm,
        "management/empleado_form.html",
        "management:empleado_list",
    )


def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return _handle_form(
        request,
        EmpleadoForm,
        "management/empleado_form.html",
        "management:empleado_list",
        empleado,
    )


def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        return redirect("management:empleado_list")
    return render(
        request,
        "management/empleado_confirm_delete.html",
        {"object": empleado},
    )


def proyecto_list(request):
    proyectos = (
        Proyecto.objects.select_related("departamento", "responsable")
        .annotate(total_tareas=Count("tareas"))
        .order_by("fecha_fin")
    )
    return render(
        request,
        "management/proyecto_list.html",
        {
            "proyectos": proyectos,
        },
    )


def proyecto_create(request):
    return _handle_form(
        request,
        ProyectoForm,
        "management/proyecto_form.html",
        "management:proyecto_list",
    )


def proyecto_update(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    return _handle_form(
        request,
        ProyectoForm,
        "management/proyecto_form.html",
        "management:proyecto_list",
        proyecto,
    )


def proyecto_delete(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == "POST":
        proyecto.delete()
        return redirect("management:proyecto_list")
    return render(
        request,
        "management/proyecto_confirm_delete.html",
        {"object": proyecto},
    )


def tarea_list(request):
    tareas = Tarea.objects.select_related("proyecto", "asignado_a").order_by(
        "-fecha_entrega"
    )
    estado = request.GET.get("estado")
    if estado:
        tareas = tareas.filter(estado=estado)
    return render(
        request,
        "management/tarea_list.html",
        {
            "tareas": tareas,
            "estado_filtrado": estado,
        },
    )


def tarea_create(request):
    return _handle_form(
        request,
        TareaForm,
        "management/tarea_form.html",
        "management:tarea_list",
    )


def tarea_update(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    return _handle_form(
        request,
        TareaForm,
        "management/tarea_form.html",
        "management:tarea_list",
        tarea,
    )


def tarea_delete(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == "POST":
        tarea.delete()
        return redirect("management:tarea_list")
    return render(
        request,
        "management/tarea_confirm_delete.html",
        {"object": tarea},
    )
