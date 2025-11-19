from django.urls import path

from . import views

app_name = "management"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("departamentos/", views.departamento_list, name="departamento_list"),
    path("departamentos/nuevo/", views.departamento_create, name="departamento_create"),
    path(
        "departamentos/<int:pk>/editar/",
        views.departamento_update,
        name="departamento_update",
    ),
    path(
        "departamentos/<int:pk>/eliminar/",
        views.departamento_delete,
        name="departamento_delete",
    ),
    path("empleados/", views.empleado_list, name="empleado_list"),
    path("empleados/nuevo/", views.empleado_create, name="empleado_create"),
    path(
        "empleados/<int:pk>/editar/",
        views.empleado_update,
        name="empleado_update",
    ),
    path(
        "empleados/<int:pk>/eliminar/",
        views.empleado_delete,
        name="empleado_delete",
    ),
    path("proyectos/", views.proyecto_list, name="proyecto_list"),
    path("proyectos/nuevo/", views.proyecto_create, name="proyecto_create"),
    path(
        "proyectos/<int:pk>/editar/",
        views.proyecto_update,
        name="proyecto_update",
    ),
    path(
        "proyectos/<int:pk>/eliminar/",
        views.proyecto_delete,
        name="proyecto_delete",
    ),
    path("tareas/", views.tarea_list, name="tarea_list"),
    path("tareas/nuevo/", views.tarea_create, name="tarea_create"),
    path("tareas/<int:pk>/editar/", views.tarea_update, name="tarea_update"),
    path("tareas/<int:pk>/eliminar/", views.tarea_delete, name="tarea_delete"),
]
