from django.db import models


class Departamento(models.Model):
    """Representa un area organizacional."""

    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=150, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


class Empleado(models.Model):
    """Colaborador asociado a un departamento."""

    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE, related_name="empleados"
    )
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    cargo = models.CharField(max_length=120)
    fecha_contratacion = models.DateField()

    class Meta:
        ordering = ["nombre"]

    def __str__(self) -> str:
        return f"{self.nombre} ({self.cargo})"


class Proyecto(models.Model):
    """Proyecto registrado dentro de un departamento."""

    departamento = models.ForeignKey(
        Departamento, on_delete=models.PROTECT, related_name="proyectos"
    )
    responsable = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proyectos_liderados",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto_estimado = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="MXN"
    )

    class Meta:
        ordering = ["-fecha_inicio", "nombre"]

    def __str__(self) -> str:
        return self.nombre


class Tarea(models.Model):
    """Actividad concreta dentro de un proyecto."""

    ESTADOS = [
        ("planificado", "Planificado"),
        ("en_progreso", "En progreso"),
        ("completado", "Completado"),
    ]
    PRIORIDADES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
    ]

    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name="tareas"
    )
    asignado_a = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name="tareas"
    )
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="planificado")
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default="media")
    fecha_entrega = models.DateField()
    porcentaje_avance = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["fecha_entrega", "titulo"]

    def __str__(self) -> str:
        return f"{self.titulo} - {self.get_estado_display()}"
